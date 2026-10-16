from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 驱动 + 数据库
DATABASE_URL = "sqlite:///./data/app.db"

# 引擎：方言翻译+连接池管理
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# 会话类：用于构建单次会话，Session -> Engine（连接池+方言）-> 驱动 -> Sqlite/MySQL/PostgreSQL
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# 类继承：ORM(表 <---> 类)的基
class Base(DeclarativeBase):
    pass

# 基于生成器的依赖
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()