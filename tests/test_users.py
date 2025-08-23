from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy import create_engine
from app.database import get_db
from app.database import Base
import pytest
# from alembic import command


SQLALCHEMY_DB_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQLALCHEMY_DB_URL)

Testing_SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Base = declarative_base()


# def override_get_db():
#     db = Testing_SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()




# client = TestClient(app)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()




@pytest.fixture
def client(session):
    # run our code before we return our test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db

    # command.upgrade("head")
    yield TestClient(app)
    #run our code after test finishes
    # command.downgrade("base")



def test_root(client):
    response = client.get("/")
    assert response.json().get('message') == 'Hello !'


def test_create_user(client):
    response = client.post("/users", json={"email":"user1@gmail.com", "password":"123456"})
    # print(response.json())
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "user1@gmail.com"
    # assert response.json().get("email") == "user12@gmail.com"
    assert response.status_code == 201
