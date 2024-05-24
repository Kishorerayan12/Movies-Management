from fastapi import APIRouter, Depends, HTTPException
from app.tables import MovieDetails, MovieUploaded, MovieUploadedSuggestion, MovieRlsDetails
from fastapi.security import OAuth2PasswordRequestForm
from app.authentication import auth_admin_permission, optional_auth_admin_permission
from sqlmodel import Session
from database import get_session
from sqlmodel import select
from typing import Optional

router = APIRouter()


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Simulate token creation
    if form_data.username == "admin" and form_data.password == "adminpass":
        return {"access_token": "valid_admin_token", "token_type": "bearer"}
    elif form_data.username == "john" and form_data.password == "john123":
        return {"access_token": "valid_john_token", "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

@router.post("/add-movie-suggestion")
def add_movie_suggestion(
    payload: MovieDetails, 
    db: Session = Depends(get_session),
    current_admin: Optional[dict] = 
    Depends(optional_auth_admin_permission(["post"]))
):
    admin_id = None
    if current_admin:
        admin_id = current_admin.get("username")
    
    movie_suggestion = MovieUploadedSuggestion(
        **payload.model_dump(),
        admin_id=admin_id
    )
    db.add(movie_suggestion)
    db.commit()
    return {"message": "Movie suggestion added successfully"}


@router.post("/add-movie")
def add_movie(payload: MovieRlsDetails, db:Session = Depends(get_session),
              admin: Optional[dict] = Depends(auth_admin_permission(["post"]))):
    movie = MovieUploaded(
        **payload.model_dump(),
        admin_id=admin.get("username")
    )
    db.add(movie)
    db.commit()
    return {"message": "Movie added successfully"}

@router.get("/view-movies")
def view_movie(db:Session = Depends(get_session),
              admin: dict = Depends(auth_admin_permission(["view"]))):
    movies = db.exec(select(MovieUploaded)).all()
    return movies