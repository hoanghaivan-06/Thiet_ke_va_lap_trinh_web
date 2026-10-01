import os
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine

# 1. Đọc DATABASE_URL từ biến môi trường, fallback về SQLite nếu chưa đặt
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./app.db")

# 2. Cấu hình connect_args riêng cho SQLite nếu cần
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

# 3. Tạo engine với echo=True để theo dõi các câu lệnh SQL sinh ra
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

# 4. Tạo dependency get_session và type alias SessionDep
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]