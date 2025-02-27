from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users" 

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    # Relationship to link User with Chats
    chats = relationship("Chat", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"


class Chat(Base):
    __tablename__ = "chats"

    chat_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Relationship to link Chat to User and Messages
    user = relationship("User", back_populates="chats")
    messages = relationship("Message", back_populates="chat")

    def __repr__(self) -> str:
        return f"Chat(chat_id={self.chat_id!r}, user_id={self.user_id!r}, created_at={self.created_at!r})"


class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("chats.chat_id"), nullable=False)
    sender: Mapped[str] = mapped_column(String(10), nullable=False)  # "user" or "bot"
    text: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Relationship to link Message to Chat
    chat = relationship("Chat", back_populates="messages")

    def __repr__(self) -> str:
        return f"Message(id={self.message_id!r}, chat_id={self.chat_id!r}, sender={self.sender!r}, text={self.text!r}, timestamp={self.timestamp!r})"
