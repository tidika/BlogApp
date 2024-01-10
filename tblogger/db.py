from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    # Assuming 'engine' is an instance of SQLAlchemy's Engine
    with engine.connect() as connection:
        # Read the content of the file
        with open('schema.sql', 'r') as f:
            sql_statements = f.read().split(';')

        # Remove empty statements
        sql_statements = [stmt.strip() for stmt in sql_statements if stmt.strip()]

        # Execute each SQL statement within a transaction
        with connection.begin():
            for sql_statement in sql_statements:
                connection.execute(text(sql_statement))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()