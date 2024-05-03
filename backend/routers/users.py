from typing import Literal
from sqlmodel import Session
from fastapi import APIRouter, Depends

from backend.entities import (
  UserCollection, 
  ChatCollection,
  UserResponse,
  UserUpdate
)

from backend.schema import UserInDB
from backend.auth import get_current_user
from backend import database as db

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("", response_model=UserCollection)
def get_users(
  session: Session = Depends(db.get_session),
  sort: Literal["id"] = "id",
):
  """Get a collection of users."""

  sort_key = lambda user: getattr(user, sort)
  users = db.get_all_users(session)

  return UserCollection(
    meta={"count": len(users)},
    users=sorted(users, key=sort_key),
  )
  
@users_router.get("/me", response_model=UserResponse)
def get_self(user: UserInDB = Depends(get_current_user), session: Session = Depends(db.get_session)):
  """Get current user."""
  return UserResponse(user=user)

@users_router.put("/me", response_model=UserResponse)
def update_self(user_update: UserUpdate, user: UserInDB = Depends(get_current_user), session: Session = Depends(db.get_session)):
  """Update current user."""
  return UserResponse(user = db.update_user_in_db(session, user, user_update))

@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(db.get_session)):
  """Get a user for a given id."""
  return UserResponse(
    user = db.get_user_by_id(session, user_id)
  )

@users_router.get("/{user_id}/chats", response_model=ChatCollection)
def get_user_chats(
  user_id: int, 
  sort: Literal["name"] = "name",
  session: Session = Depends(db.get_session)
):
  """Get a collection of chats for given user id"""
  
  sort_key = lambda chat: getattr(chat, sort)
  chats = db.get_all_chats_by_user(session, user_id)

  # chats = [chat for chat in chats if user_id in chat.user_ids ]

  return ChatCollection(
    meta={"count": len(chats)},
    chats=sorted(chats, key=sort_key),
  )

