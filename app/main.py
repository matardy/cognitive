from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers.messages import router as messages_router
from routers.conversations import router as conversation_router
from routers.users import router as user_router
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(messages_router, prefix="/chat", tags=["chat"])
app.include_router(user_router, tags=["user"])
app.include_router(conversation_router, prefix="/chat", tags=["chat"])

