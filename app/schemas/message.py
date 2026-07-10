from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    number: str
    content: str
    push_name: Optional[str] = None