from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors  import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select   
from sqlalchemy.ext.asyncio import AsyncSession
from db_engine import engine
from models import User, Chat, Message
from seed import seed_user_if_needed
import random

seed_user_if_needed()

app = FastAPI()

#middleware for cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# ---------------------------- Pydantic Schemas ---------------------------- #
class UserRead(BaseModel):
    id: int
    name: str


class ChatCreate(BaseModel):
    user_id: int


class ChatRead(BaseModel):
    chat_id: int
    user_id: int
    created_at: str


class MessageCreate(BaseModel):
    chat_id: int
    sender: str  # This is going to be either USER or a BOT
    text: str


class MessageRead(BaseModel):
    message_id: int
    chat_id: int
    sender: str
    text: str
    timestamp: str


# ----------------------------Endpoints ---------------------------- #
@app.get("/users/me", response_model=UserRead)
async def get_my_user():
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(User))
            user = result.scalars().first()

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return UserRead(id=user.id, name=user.name)


@app.post("/chats/", response_model=ChatRead)
async def start_chat(chat_data: ChatCreate):
    async with AsyncSession(engine) as session:
        async with session.begin():
            user = await session.get(User, chat_data.user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            chat = Chat(user_id=chat_data.user_id)
            session.add(chat)
        await session.commit()
        await session.refresh(chat)

        return ChatRead(chat_id=chat.chat_id, user_id=chat.user_id, created_at=str(chat.created_at))


@app.post("/messages/", response_model=dict)
async def send_message(message_data: MessageCreate):
    async with AsyncSession(engine) as session:
        async with session.begin():
            #Fetch chat within session
            chat = await session.get(Chat, message_data.chat_id)
            if not chat:
                raise HTTPException(status_code=404, detail="Chat not found")

            #Save user message inside transaction
            message = Message(chat_id=message_data.chat_id, sender=message_data.sender, text=message_data.text)
            session.add(message)

            #Generate bot response
            #In an ideal world this would be where be generate a bot response by understanding the user context. 
            bot_responses = ["Hello!", "How can I help?", "That's interesting!", "Tell me more!", "I'm here to chat!"]
            bot_message = Message(chat_id=message.chat_id, sender="BOT", text=random.choice(bot_responses))
            session.add(bot_message)

        # The transaction automatically commits here after exiting the block
        
        #Refresh objects *after* transaction is committed
        await session.refresh(message)
        await session.refresh(bot_message)

    return {
        "user_message": MessageRead(
            message_id=message.message_id, chat_id=message.chat_id, sender=message.sender, text=message.text, timestamp=str(message.timestamp)
        ),
        "bot_message": MessageRead(
            message_id=bot_message.message_id, chat_id=bot_message.chat_id, sender=bot_message.sender, text=bot_message.text, timestamp=str(bot_message.timestamp)
        ),
    }


@app.get("/chats/{chat_id}/messages/", response_model=list[MessageRead])
async def get_chat_messages(chat_id: int):
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(Message).where(Message.chat_id == chat_id).order_by(Message.timestamp))
            messages = result.scalars().all()

            if not messages:
                raise HTTPException(status_code=404, detail="No messages found for this chat")

            return [
                MessageRead(
                    message_id=msg.message_id, chat_id=msg.chat_id, sender=msg.sender, text=msg.text, timestamp=str(msg.timestamp)
                )
                for msg in messages
            ]


@app.get("/users/{user_id}/chats/", response_model=list[ChatRead])
async def get_user_chats(user_id: int):
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(Chat).where(Chat.user_id == user_id).order_by(Chat.created_at))
            chats = result.scalars().all()

        # if we dont have anything, just return empty array
            if not chats:
                return []

            return [
                ChatRead(chat_id=chat.chat_id, user_id=chat.user_id, created_at=str(chat.created_at))
                for chat in chats
            ]
