from datetime import date
from typing import Literal, Annotated
from sqlmodel import Session
from typing import Union
from fastapi import APIRouter, Depends, Query

from backend.entities import (
  ChatCollection,
  ChatUpdate,
  ChatResponse,
  MessageCollection,
  UserCollection,
  Chat,
  MessageResponse,
  MessageRequest,
  ChatResponseFull,
  ChatResponseNone,
  ChatResponseMessages,
  ChatResponseUsers
)
from backend import database as db
from backend.auth import get_current_user
from backend.schema import UserInDB

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


@chats_router.get("", response_model=ChatCollection)
def get_chats(
  session: Session = Depends(db.get_session),
  sort: Literal["name"] = "name",
):
  """Get a collection of chats."""

  sort_key = lambda chat: getattr(chat, sort)
  chats = db.get_all_chats(session)

  return ChatCollection(
    meta={"count": len(chats)},
    chats=sorted(chats, key=sort_key),
  )

# update with new functionality
@chats_router.get(
  "/{chat_id}",
  response_model=Union[ChatResponseFull, ChatResponseUsers, ChatResponseMessages, ChatResponseNone]
)
def get_chat(chat_id: int, include: Annotated[list[str] | None, Query()] = None, session: Session = Depends(db.get_session)):
  """Get a chat for a given chat id."""
  chat_data = db.get_chat_by_id(session, chat_id)
  response = ChatResponseFull(
    meta = {
      "message_count": len(chat_data.messages),
      "user_count": len(chat_data.users)
    },
    chat = Chat(
      id = chat_data.id,
      name = chat_data.name,
      owner = chat_data.owner, 
      created_at = chat_data.created_at,
    ),
    users = chat_data.users,
    messages = chat_data.messages
    )
  if include is None:
    return ChatResponseNone(
      meta = response.meta,
      chat = response.chat,
    )
  if "messages" in include:
    if "users" in include:
      return response
    else:
      return ChatResponseMessages(
        meta = response.meta,
        chat = response.chat,
        messages = response.messages
      )
  else:
    return ChatResponseUsers(
      meta = response.meta,
      chat = response.chat,
      users = response.users
    )
  

@chats_router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(chat_id: int, chat_update: ChatUpdate, session: Session = Depends(db.get_session)):
  """Update a chat name for a given id."""
  chat_data = db.update_chat(session, chat_id, chat_update)
  return {
    "chat": Chat(
    id = chat_data.id,
    name = chat_data.name,
    owner = chat_data.owner, 
    created_at = chat_data.created_at,)
  }


@chats_router.post("/{chat_id}/messages", status_code=201, response_model=MessageResponse)
def create_message(chat_id: int, 
                   message_request: MessageRequest, 
                   user: UserInDB = Depends(get_current_user), 
                   session: Session = Depends(db.get_session)):
  """Create new message"""
  return MessageResponse(
    message = db.create_message_in_db(chat_id, session, user, message_request)
  )


@chats_router.get("/{chat_id}/messages", response_model=MessageCollection)
def get_chat_messages(
  chat_id: int,
  sort: Literal["created_at"] = "created_at",
  session: Session = Depends(db.get_session),
):
  """Return messages for a given chat id"""

  sort_key = lambda message: getattr(message, sort)
  messages = db.get_messages_by_chat_id(session, chat_id)

  return MessageCollection(
    meta={"count": len(messages)},
    messages=sorted(messages, key=sort_key),
  )

@chats_router.get("/{chat_id}/users", response_model=UserCollection)
def get_chat_users(
  chat_id: int, 
  sort: Literal["id"] = "id",
  session: Session = Depends(db.get_session)
):
  """Return users for a given chat id"""

  sort_key = lambda user: getattr(user, sort)
  users = db.get_users_by_chat_id(session, chat_id)
  
  return UserCollection(
    meta={"count": len(users)},
    users=sorted(users, key=sort_key),
  )
