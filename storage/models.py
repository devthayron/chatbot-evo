from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from storage.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True, nullable=False, index=True)
    push_name = Column(String, nullable=True)

    messages = relationship(
        "Message",
        back_populates="conversation",
        order_by="Message.timestamp",
        cascade="all, delete-orphan",
    )


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        # Evita duplicar a mesma mensagem 
        UniqueConstraint(
            "conversation_id", "role", "content", "timestamp",
            name="uq_message_dedup",
        ),
    )

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False, index=True)

    conversation = relationship("Conversation", back_populates="messages")