from typing import Optional

from sqlmodel import SQLModel, Field
import datetime as dt
from pydantic import AnyUrl, BaseModel


class TextSummaryPayload(BaseModel):
    url: AnyUrl


class TextSummary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(nullable=False)
    summary: Optional[str] = Field(nullable=True, default=None)
    created_at: Optional[dt.datetime] = Field(default_factory=dt.datetime.utcnow)
