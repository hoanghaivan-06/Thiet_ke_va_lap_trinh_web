from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, select

from app.database import SessionDep, engine
from app.models import (
    Hero,
    HeroCreate,
    HeroPublic,
    HeroUpdate,
    Team,
    TeamCreate,
    TeamPublic,
    Mission,
    MissionCreate,
    MissionPublic,
    HeroMissionLink,
)
from app import models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


# ==========================================
# 1. TEAM ENDPOINTS (Task 6.1)
# ==========================================


# POST /teams - Bắt lỗi trùng lặp trả về 409 Conflict
@app.post("/teams", response_model=TeamPublic, status_code=status.HTTP_201_CREATED)
def create_team(team_in: TeamCreate, session: SessionDep):
    team = Team.model_validate(team_in)
    session.add(team)
    try:
        session.commit()
        session.refresh(team)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Team name already exists",
        )
    return team


# GET /teams - Lấy danh sách teams
@app.get("/teams", response_model=list[TeamPublic])
def list_teams(session: SessionDep, offset: int = 0, limit: int = Query(default=10, le=100)):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


# GET /teams/{team_id}/heroes - Lấy các heroes trong team qua Relationship
@app.get("/teams/{team_id}/heroes", response_model=list[HeroPublic])
def get_team_heroes(team_id: int, session: SessionDep):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )
    return team.heroes


# ==========================================
# 2. HERO ENDPOINTS (Task 6.2 & Challenge 6.3)
# ==========================================


# POST /heroes - Kiểm tra team_id hợp lệ (404 nếu không tìm thấy team)
@app.post("/heroes", response_model=HeroPublic, status_code=status.HTTP_201_CREATED)
def create_hero(hero_in: HeroCreate, session: SessionDep):
    if hero_in.team_id is not None:
        team = session.get(Team, hero_in.team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
            )

    hero = Hero.model_validate(hero_in)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


# GET /heroes - Tìm kiếm và lọc bằng database WHERE, ILIKE
@app.get("/heroes", response_model=list[HeroPublic])
def list_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    min_age: int | None = None,
    team_id: int | None = None,
    name: str | None = None,
):
    query = select(Hero)
    if min_age is not None:
        query = query.where(Hero.age >= min_age)
    if team_id is not None:
        query = query.where(Hero.team_id == team_id)
    if name is not None:
        query = query.where(Hero.name.ilike(f"%{name}%"))

    query = query.order_by(Hero.id).offset(offset).limit(limit)
    heroes = session.exec(query).all()
    return heroes


# GET /heroes/{hero_id}
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def get_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    return hero


# PATCH /heroes/{hero_id} - Kiểm tra team_id hợp lệ nếu có cập nhật
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero_in: HeroUpdate, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )

    hero_data = hero_in.model_dump(exclude_unset=True)
    if "team_id" in hero_data and hero_data["team_id"] is not None:
        team = session.get(Team, hero_data["team_id"])
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
            )

    hero.sqlmodel_update(hero_data)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


# DELETE /heroes/{hero_id}
@app.delete("/heroes/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found"
        )
    session.delete(hero)
    session.commit()
    return None

# ==========================================
# 3. MISSION ENDPOINTS (Part 7)
# ==========================================

# Tạo mission mới
@app.post("/missions", response_model=MissionPublic, status_code=status.HTTP_201_CREATED)
def create_mission(mission_in: MissionCreate, session: SessionDep):
    mission = Mission.model_validate(mission_in)
    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission

# Gán hero vào mission
@app.post("/heroes/{hero_id}/missions/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_hero_to_mission(hero_id: int, mission_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    mission = session.get(Mission, mission_id)
    if not hero or not mission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero or Mission not found")

    if mission not in hero.missions:
        hero.missions.append(mission)
        session.add(hero)
        session.commit()
    return None

# Lấy danh sách mission của một hero
@app.get("/heroes/{hero_id}/missions", response_model=list[MissionPublic])
def get_hero_missions(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    return hero.missions