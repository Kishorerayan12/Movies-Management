from typing import Optional
from uuid import UUID, uuid4
from datetime import date


from sqlmodel import SQLModel, Field


class MovieDetails(SQLModel):
    movie_name: str
    genre: Optional[str] = None
    rating: Optional[int] = None

class MovieRlsDetails(MovieDetails):
    theatricl_rls_date: date 
    ott_rls_date: date

class MovieUploadedSuggestion(MovieDetails, table=True):
    __tablename__ = "movies_upload_suggestion"
    id: UUID =  Field(default_factory=uuid4,primary_key=True)
    user_id: Optional[str]
    admin_id: Optional[str]


class MovieUploaded(MovieRlsDetails, table=True):
    __tablename__ = "movies_uploaded"

    id: UUID =  Field(default_factory=uuid4,primary_key=True)
    admin_id: str
