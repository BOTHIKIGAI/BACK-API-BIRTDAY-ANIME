"""
This module contains 
"""
from fastapi import APIRouter

router = APIRouter(
    tags=["Dates Animes"],
    prefix='/v1')

@router.get('/{anime}/date/{date}')
def get_date(anime: str, date: str):
    return {anime, date}
