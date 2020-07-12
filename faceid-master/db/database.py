from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # only for SQLite
# )

db = {
    'user'     : 'face',
    'password' : 'Face1234',
    'host'     : 'localhost',
    'port'     : 3306,
    'database' : 'faceid'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8mb4"

engine = create_engine(DB_URL, convert_unicode=False, pool_size=30, pool_recycle=500, max_overflow=30)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()