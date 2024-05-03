from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel, Field 

class Metadata(BaseModel):
  """Represents metadata for a collection."""
  count: int

class ChatMetadata(BaseModel):
  """Metadata for a chat"""
  message_count: int
  user_count: int

class User(SQLModel):
  """Represents a user in the database."""
  id: int
  username: str
  email: str
  created_at: datetime

class Message(SQLModel):
  """Represents an API response for a message."""
  id: int
  text: str
  chat_id: int
  user: User
  created_at: datetime

class Chat(SQLModel):
  """Represents a chat that could be included in an API response"""

  id: Optional[int] = Field(default=None, primary_key=True)
  name: str
  owner: User
  created_at: Optional[datetime] = Field(default_factory=datetime.now)

# class UserCreate(BaseModel):
#   """Represents parameters for adding new users to the system."""
#   id: int
  
class UserResponse(BaseModel):
  user: User

class ChatResponseFull(BaseModel):
  meta: ChatMetadata
  chat: Chat
  users: Optional[list[User]] = None
  messages: Optional[list[Message]] = None

class ChatResponseNone(BaseModel):
  meta: ChatMetadata
  chat: Chat

class ChatResponseUsers(BaseModel):
  meta: ChatMetadata
  chat: Chat
  users: Optional[list[User]] = None

class ChatResponseMessages(BaseModel):
  meta: ChatMetadata
  chat: Chat
  messages: Optional[list[Message]] = None

class ChatResponse(BaseModel):
  chat: Chat

class MessageResponse(BaseModel):
  message: Message

class ChatUpdate(BaseModel):
  """Represents parameters for updating the name of an existing chat."""
  name: str = None

class UserUpdate(SQLModel):
  username: Optional[str] = Field(default=None, primary_key=True)
  email: Optional[str] = Field(default=None, primary_key=True)

class MessageRequest(BaseModel):
  text: str

class ChatCollection(BaseModel):
  """Represents an API response for a collection of chats."""
  meta: Metadata
  chats: list[Chat]

class UserCollection(BaseModel):
  """Represents an API response for a collection of users."""
  meta: Metadata
  users: list[User]

class MessageCollection(BaseModel):
  """Represents an API response for a collection of messages."""
  meta: Metadata
  messages: list[Message]