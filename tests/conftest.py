from fastapi.testclient import TestClient
from app.main import app
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base,get_db
from app.config import settings
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    print('^^^^^^^after running^^^^^^^^')
    Base.metadata.create_all(bind=engine)
    print('^^^^^^^before running^^^^^^^^')
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email":"thuy@gmail.com","password":"nguyenthuy0308"}
    res = client.post('/users/',json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def test_posts(session,test_user):
    posts_data = [
        {"title": "Test post 1", "content": "This is post 1", "owner_id": test_user['id']},
        {"title": "Test post 2", "content": "This is post 2", "owner_id": test_user['id']},
        {"title": "Test post 3", "content": "This is post 3", "owner_id": test_user['id']}
    ]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model,posts_data)
    posts = list(post_map)
    
    session.add_all(posts)
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts
