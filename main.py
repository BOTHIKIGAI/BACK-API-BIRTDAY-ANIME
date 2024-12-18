"""
Main module for the BIRTHDAY ANIME API.

This module initializes the FastAPI application and includes the router for handling
requests related to anime episode release dates.
"""

from fastapi import FastAPI
from app.router.v1.author_router import AuthorRouter
from app.router.v1.anime_router import AnimeRouter

app = FastAPI(
    title="BIRTHDAY ANIME",
    description="API for the consumption of episode release dates.")

app.include_router(AuthorRouter, tags=["Author"], prefix='/v1/authors')
app.include_router(AnimeRouter, tags=["Anime"], prefix='/v1/anime')
