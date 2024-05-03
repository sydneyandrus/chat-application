from datetime import date

from fastapi.testclient import TestClient

from backend.main import app

def test_root():
  test_client = TestClient(app)
  response = test_client.get("/")
  assert response.status_code == 200
  assert response.json() == {'message': 'welcome to chat application'}

def test_get_all_users():
  client = TestClient(app)
  response = client.get("/users")
  assert response.status_code == 200
  
  meta = response.json()["meta"]
  users = response.json()["users"]
  assert meta["count"] == len(users)
  assert users == sorted(users, key=lambda user: user["id"])

def test_create_user():
  client = TestClient(app)
  create_params = {
    "id": "new_user_id"
  }
  response = client.post("users", json=create_params)

  assert response.status_code == 200

  data = response.json()
  assert "user" in data
  user = data["user"]
  for key, value in create_params.items():
    assert user[key] == value
  
  response = client.get(f"/users/new_user_id")
  assert response.status_code == 200
  data = response.json()
  assert "user" in data
  user = data["user"]
  for key, value in create_params.items():
    assert user[key] == value

def test_create_existing_user():
  client = TestClient(app)
  create_params = {
    "id": "sarah"
  }
  response = client.post("users", json=create_params)

  assert response.status_code == 422

  expected_response = {
    "detail": {
      "type": "duplicate_entity",
      "entity_name": "User",
      "entity_id": "sarah"
    }
  }
  assert response.json() == expected_response

def test_get_sarah_user():
  client = TestClient(app)
  response = client.get("/users/sarah")
  assert response.status_code == 200
  
  expected_user = {
    "id": "sarah",
    "created_at": "2006-03-02T22:30:11",
  }
  assert response.json() == {"user": expected_user}

def test_get_nonexistent_user():
  client = TestClient(app)
  response = client.get("/users/fakeuser")
  assert response.status_code == 404

  expected_response = {
    "detail": {
      "type": "entity_not_found",
      "entity_name": "User",
      "entity_id": "fakeuser"
    }
  }
  assert response.json() == expected_response

def test_get_chats_for_user():
  client = TestClient(app)
  response = client.get("/users/sarah/chats")
  assert response.status_code == 200

  meta = response.json()["meta"]
  chats = response.json()["chats"]
  assert meta["count"] == len(chats)
  assert chats == sorted(chats, key=lambda chat: chat["name"])

def test_get_chats_for_nonexistent_user():
  client = TestClient(app)
  response = client.get("/users/fakeuser/chats")
  assert response.status_code == 404

  expected_response = {
    "detail": {
      "type": "entity_not_found",
      "entity_name": "User",
      "entity_id": "fakeuser"
    }
  }
  assert response.json() == expected_response

def test_get_all_chats():
  client = TestClient(app)
  response = client.get("/chats")
  assert response.status_code == 200
  
  meta = response.json()["meta"]
  chats = response.json()["chats"]
  assert meta["count"] == len(chats)
  assert chats == sorted(chats, key=lambda chat: chat["name"])

def test_get_chat_from_id():
  client = TestClient(app)
  response = client.get("/chats/e0ec0881a2c645de842ca5dd0fa7985b")
  assert response.status_code == 200

  expected_response = {
    "chat": {
      "id": "e0ec0881a2c645de842ca5dd0fa7985b",
      "name": "newt",
      "user_ids": [
        "newt",
        "ripley",
      ],
      "owner_id": "ripley",
      "created_at": "2023-12-13T17:26:45"
    }
  }
  assert response.json() == expected_response

def test_get_chat_from_nonexistent_id():
  client = TestClient(app)
  response = client.get("/chats/fakechatid")
  assert response.status_code == 404

  expected_response = {
    "detail": {
      "type": "entity_not_found",
      "entity_name": "Chat",
      "entity_id": "fakechatid"
    }
  }
  assert response.json() == expected_response

def test_chat_name_update():
  update_params = {
    "name": "updated chat name"
  }
  client = TestClient(app)
  response = client.put("/chats/e0ec0881a2c645de842ca5dd0fa7985b", json=update_params)
  assert response.status_code == 200

  expected_response = {
    "chat": {
      "id": "e0ec0881a2c645de842ca5dd0fa7985b",
      "name": "updated chat name",
      "user_ids": [
        "newt",
        "ripley",
      ],
      "owner_id": "ripley",
      "created_at": "2023-12-13T17:26:45"
    }
  }
  assert response.json() == expected_response

  response = client.get("/chats/e0ec0881a2c645de842ca5dd0fa7985b")
  assert response.status_code == 200
  assert response.json() == expected_response

def test_chat_name_update_invalid_id():
  update_params = {
    "name": "updated chat name"
  }
  client = TestClient(app)
  response = client.put("/chats/fakechatid", json=update_params)
  assert response.status_code == 404

  expected_response = {
    "detail": {
      "type": "entity_not_found",
      "entity_name": "Chat",
      "entity_id": "fakechatid"
    }
  }
  assert response.json() == expected_response

def test_chat_delete_by_id():
  client = TestClient(app)
  response = client.delete("/chats/e0ec0881a2c645de842ca5dd0fa7985b")
  assert response.status_code == 204

  client = TestClient(app)
  response = client.get("/chats/e0ec0881a2c645de842ca5dd0fa7985b")
  assert response.status_code == 404

  expected_response = {
    "detail": {
      "type": "entity_not_found",
      "entity_name": "Chat",
      "entity_id": "e0ec0881a2c645de842ca5dd0fa7985b"
    }
  }
  assert response.json() == expected_response

def test_chat_delete_nonexistent_id():
  client = TestClient(app)
  response = client.delete("/chats/fakechatid")
  assert response.status_code == 404

  expected_response = {
    "detail": {
      "type": "entity_not_found",
      "entity_name": "Chat",
      "entity_id": "fakechatid"
    }
  }
  assert response.json() == expected_response

def test_get_messages_for_chat():
  client = TestClient(app)
  response = client.get("/chats/734eeb9ddaec43b2ab6e289a0d472376/messages")
  assert response.status_code == 200

  meta = response.json()["meta"]
  messages = response.json()["messages"]
  assert meta["count"] == len(messages)
  assert messages == sorted(messages, key=lambda message: message["created_at"])

def test_get_messages_for_nonexistent_chat():
  client = TestClient(app)
  response = client.get("/chats/fakechatid/messages")
  assert response.status_code == 404

  expected_response = {
    "detail": {
      "type": "entity_not_found",
      "entity_name": "Chat",
      "entity_id": "fakechatid"
    }
  }
  assert response.json() == expected_response

def test_get_users_for_chat_id():
  client = TestClient(app)
  response = client.get("/chats/734eeb9ddaec43b2ab6e289a0d472376/users")
  assert response.status_code == 200

  expected_response = {
    "meta": {
      "count": 3,
    },
    "users": [
      {
        "id": "bishop",
        "created_at": "2014-04-14T10:49:07"
      }, 
      {
        "id": "burke",
        "created_at": "2018-07-25T10:40:45"
      }, 
      {
        "id": "ripley",
        "created_at": "2008-06-08T14:32:08"
      },
    ]
  }
  meta = response.json()["meta"]
  users = response.json()["users"]
  assert meta["count"] == len(users)
  assert users == sorted(users, key=lambda user: user["id"])
  assert response.json() == expected_response

def test_get_users_for_nonexistent_chat():
  client = TestClient(app)
  response = client.get("/chats/fakechatid/users")
  assert response.status_code == 404

  expected_response = {
    "detail": {
      "type": "entity_not_found",
      "entity_name": "Chat",
      "entity_id": "fakechatid"
    }
  }
  assert response.json() == expected_response