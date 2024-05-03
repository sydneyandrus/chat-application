import os
from sqlmodel import Session, SQLModel, create_engine, select
from datetime import datetime
from uuid import uuid4

from backend.entities import (
  ChatUpdate,
  UserResponse,
  User,
  Message,
  Chat,
  UserUpdate,
  MessageRequest
)

from backend.schema import (
  UserInDB,
  ChatInDB,
  MessageInDB
)

if os.environ.get("DB_LOCATION") == "EFS":
    db_path = "/mnt/efs/pony_express.db"
    echo = False
else:
    db_path = "backend/pony_express.db"
    echo = True

engine = create_engine(
    f"sqlite:///{db_path}",
    echo=echo,
    connect_args={"check_same_thread": False},
)

def create_db_and_tables():
  SQLModel.metadata.create_all(engine)


def get_session():
  with Session(engine) as session:
    yield session


class EntityNotFoundException(Exception):
  def __init__(self, *, entity_name: str, entity_id: int):
    self.entity_name = entity_name
    self.entity_id = entity_id

class RequestValidationException(Exception):
  def __init__(self, *, entity_name: str, entity_id: int):
    self.entity_name = entity_name
    self.entity_id = entity_id
#   -------- chats --------   #

def get_all_chats(session: Session) -> list[Chat]:
  """
  Retrieve all chats from the database.

  :return: ordered list of chats
  """

  return session.exec(select(ChatInDB)).all()

def get_all_chats_by_user(session: Session, user_id: int) -> list[Chat]:
  """
  Retrieve all chats from the database.

  :return: ordered list of chats
  """
  user = session.get(UserInDB, user_id)
  if not user:
    raise EntityNotFoundException(entity_name="User", entity_id=user_id)

  user_chats = []
  for currentChat in session.exec(select(ChatInDB)).all():
    if user in currentChat.users:
      chat = Chat(
        id = currentChat.id,
        name = currentChat.name,
        owner = User(
          id = currentChat.owner.id,
          username = currentChat.owner.username,
          email = currentChat.owner.email,
          created_at = currentChat.owner.created_at
        ),
        created_at = currentChat.created_at
      )
      user_chats.append(chat)
  return user_chats

def get_chat_by_id(session: Session, chat_id: int) -> ChatInDB:
  """
  Retrieve a chat from the database.

  :param chat_id: id of the chat to be retrieved
  :return: the retrieved chat
  :raises EntityNotFoundException: if no such chat id exists
  """

  chat = session.get(ChatInDB, chat_id)

  if chat:
    return chat

  raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def update_chat(session: Session, chat_id: int, chat_update: ChatUpdate) -> ChatInDB:
  """
  Update a chat in the database.

  :param chat_id: id of the chat to be updated
  :param chat_update: attributes to be updated on the chat
  :return: the updated chat
  :raises EntityNotFoundException: if no such chat id exists
  """

  chat = get_chat_by_id(session, chat_id)

  for attr, value in chat_update.model_dump(exclude_unset=True).items():
    setattr(chat, attr, value)

  session.add(chat)
  session.commit()
  session.refresh(chat)
  
  return chat

def delete_chat(session: Session, chat_id: int):
  """
  Delete a chat from the database.

  :param chat_id: the id of the chat to be deleted
  :raises EntityNotFoundException: if no such chat exists
  """

  chat = get_chat_by_id(session, chat_id)
  session.delete(chat)
  session.commit()

def get_messages_by_chat_id(session: Session, chat_id) -> list[Message]:
  """
  Gets messages from the database for a specific chat
  
  :param chat_id: the id of the chat to get messages for
  :raises EntityNotFoundException: if no such chat exists
  """

  chat = get_chat_by_id(session, chat_id)
  return chat.messages

def get_users_by_chat_id(session: Session, chat_id) -> list[int]:
  """
  Gets users from the database for a specific chat
  :param chat_id: the id of the chat to get users for
  :raises EntityNotFoundException: if no such chat exists
  """

  chat = get_chat_by_id(session, chat_id)
  user_list = []
  for user in chat.users:
    user_list.append(user)
  return user_list

def create_message_in_db(chat_id: int, session: Session, user: UserInDB, message_request: MessageRequest) -> Message:
  """
  Adds a new message to the current chat from the current user
  :param chat_id: the id of the chat to create message for
  :param user: current user, who message is from
  :param message_request: contains text of new message
  :return: created message
  :raises EntityNotFoundException: if no such chat exists
  """
  chat = get_chat_by_id(session, chat_id)
  new_message = MessageInDB(
    text = message_request.text,
    chat_id = chat_id,
    user = user,
    user_id = user.id,
    chat = chat
  )
  chat.messages.append(new_message)
  session.add(chat)
  session.commit()
  session.refresh(chat)
  return Message(
    id = new_message.id,
    text = new_message.text,
    chat_id = new_message.chat_id,
    user = new_message.user,
    created_at = new_message.created_at
  )


#   -------- users --------   #


def get_all_users(session: Session) -> list[User]:
  """
  Retrieve all users from the database.

  :return: ordered list of users
  """

  return session.exec(select(UserInDB)).all()


def get_user_by_id(session: Session, user_id: int) -> User:
  """
  Retrieve an user from the database.

  :param user_id: id of the user to be retrieved
  :return: the retrieved user
  """

  user = session.get(UserInDB, user_id)

  if user:
    return user
  
  raise EntityNotFoundException(entity_name="User", entity_id=user_id)

def update_user_in_db(session: Session, user: UserInDB, request: UserUpdate) -> User:
  """
  Update user in database

  :param user: user to update in database
  :param request: update request, with optional username and email fields to update
  :return: the updated user 
  """

  for attr, value in request.model_dump(exclude_unset=True).items():
    setattr(user, attr, value)

  session.add(user)
  session.commit()
  session.refresh(user)
  
  return User(
    id = user.id,
    username = user.username,
    email = user.email, 
    created_at = user.created_at
  )

