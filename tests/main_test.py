from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from backend.main import app
from backend import database as db

@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    def _get_session_override():
        return session

    app.dependency_overrides[db.get_session] = _get_session_override

    yield TestClient(app)

    app.dependency_overrides.clear()

def test_get_all_users():
  client = TestClient(app)
  response = client.get("/users")
  assert response.status_code == 200
  
  print(response.json())

  meta = response.json()["meta"]
  users = response.json()["users"]
  assert meta["count"] == len(users)
  assert users == sorted(users, key=lambda user: user["id"])

def test_get_user():
  client = TestClient(app)
  response = client.get("/users/1")
  assert response.status_code == 200
  print(response.json())
  
def test_get_user3():
  client = TestClient(app)
  response = client.get("/users/3")
  assert response.status_code == 200
  print(response.json())

def test_get_chat_messages():
  client = TestClient(app)
  response = client.get("/chats/1/messages")
  assert response.status_code == 200
  print(response.json())

def test_get_other_user_chats():
  client = TestClient(app)
  response = client.get("/users/3/chats")
  assert response.status_code == 200
  print(response.json())

def test_get_skynet_users():
  client = TestClient(app)
  response = client.get("/chats/1/users")
  assert response.status_code == 200
  print(response.json())

def test_update_chat_name():
  client = TestClient(app)
  response = client.put("/chats/1", json={"name": "updated name"})
  assert response.status_code == 200
  print(response.json())

def test_get_chat():
  client = TestClient(app)
  response = client.get("/chats/1")
  assert response.status_code == 200
  print(response.json())

def test_registration():
  """POST /auth/registration"""
  client = TestClient(app)
  current_timestamp = int(datetime.now().timestamp())
  registration_params = {
    "username": "new724sere",
    "email": "random7264uy@cool.spot",
    "password": "password",
  }
  response = client.post("/auth/registration", json=registration_params)
  assert response.status_code == 201
  data = response.json()
  user = data["user"]
  assert user is not None

def test_post_new_message():
  """POST /chats/1/messages"""
  client = TestClient(app)
  auth_data = {
    "username": "sarah",
    "password": "sarahpassword",
  }
  response = client.post("/auth/token", data=auth_data)
  assert response.status_code == 200
  token = response.json()["access_token"]

  current_timestamp = int(datetime.now().timestamp())

  response = client.post(
    "/chats/1/messages",
    headers={"Authorization": f"Bearer {token}"},
    json={"text": "new message"},
  )
  assert response.status_code == 201

def test_get_skynet_chat():
  """GET /chats/1"""
  client = TestClient(app)
  response = client.get("/chats/1")
  assert response.status_code == 200
  # assert response.json() == {
  #   "meta": {
  #     "message_count": len(skynet_messages),
  #     "user_count": 2,
  #   },
  #   "chat": skynet_chat,
  # }

def test_get_skynet_chat_users():
  """GET /chats/1?include=users"""
  client = TestClient(app)
  response = client.get("/chats/1?include=users")
  assert response.status_code == 200

def test_get_skynet_chat_messages():
  """GET /chats/1?include=messages"""
  client = TestClient(app)
  response = client.get("/chats/1?include=messages")
  assert response.status_code == 200

def test_get_skynet_chat_users_and_messages():
  """GET /chats/1??include=users&include=messages"""
  client = TestClient(app)
  response = client.get("/chats/1?include=users&include=messages")
  assert response.status_code == 200