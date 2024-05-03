from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from mangum import Mangum

from backend.routers.chats import chats_router
from backend.routers.users import users_router
from backend.auth import auth_router
from backend.database import EntityNotFoundException
from backend.database import RequestValidationException
from backend.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
  create_db_and_tables()
  yield

app = FastAPI(
  title="chat application API",
  description="API for managing chats between users.",
  version="0.1.0",
  lifespan=lifespan,
)

app.include_router(chats_router)
app.include_router(users_router)
app.include_router(auth_router)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.exception_handler(EntityNotFoundException)
def handle_entity_not_found(
  _request: Request,
  exception: EntityNotFoundException,
) -> JSONResponse:
  return JSONResponse(
    status_code=404,
    content={
      "detail": {
        "type": "entity_not_found",
        "entity_name": exception.entity_name,
        "entity_id": exception.entity_id,
      },
    },
  )

@app.exception_handler(RequestValidationException)
def handle_duplicate_entity(
  _request: Request,
  exception: RequestValidationException,
) -> JSONResponse:
  return JSONResponse(
    status_code=422,
    content={
      "detail": {
        "type": "duplicate_entity",
        "entity_name": exception.entity_name,
        "entity_id": exception.entity_id,
      },
    },
  )

@app.get("/", include_in_schema=False)
def root(): 
	return {"message": "welcome to chat application"}

lambda_handler = Mangum(app)