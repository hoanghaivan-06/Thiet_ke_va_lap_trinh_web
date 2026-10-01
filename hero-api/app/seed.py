from sqlmodel import Session, SQLModel, select
from app.database import engine
from app.models import Team, Hero, Mission


def seed_data():
    # 1. Đảm bảo bảng đã được tạo
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # 2. Kiểm tra nếu đã có dữ liệu thì dừng (tránh chèn trùng lặp khi chạy nhiều lần)
        existing_team = session.exec(select(Team)).first()
        if existing_team:
            print("Database already seeded. Skipping...")
            return

        print("Seeding database...")

        # 3. Tạo Missions
        sokovia = Mission(title="Battle of Sokovia")
        endgame = Mission(title="Defeat Thanos")

        # 4. Tạo Teams
        avengers = Team(name="Avengers", headquarters="Avengers Tower")
        xmen = Team(name="X-Men", headquarters="Xavier Institute")

        # 5. Tạo Heroes và gán trực tiếp vào Team & Missions qua Relationship
        tony = Hero(
            name="Tony Stark",
            age=48,
            secret_name="Iron Man",
            team=avengers,
            missions=[sokovia, endgame],
        )
        steve = Hero(
            name="Steve Rogers",
            age=102,
            secret_name="Captain America",
            team=avengers,
            missions=[sokovia, endgame],
        )
        natasha = Hero(
            name="Natasha Romanoff",
            age=35,
            secret_name="Black Widow",
            team=avengers,
            missions=[sokovia, endgame],
        )
        logan = Hero(
            name="Logan",
            age=150,
            secret_name="Wolverine",
            team=xmen,
            missions=[sokovia],
        )
        charles = Hero(
            name="Charles Xavier",
            age=65,
            secret_name="Professor X",
            team=xmen,
            missions=[],
        )

        # 6. Thêm vào session và lưu (commit)
        session.add(avengers)
        session.add(xmen)
        session.add_all([tony, steve, natasha, logan, charles])
        session.commit()

        print("Seeding complete!")


if __name__ == "__main__":
    seed_data()