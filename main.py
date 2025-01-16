"""
Main module for the BIRTHDAY ANIME API.

This module initializes the FastAPI application and includes the router for handling
requests related to anime episode release dates.
"""

from fastapi import FastAPI
from app.router.v1.author_router import AuthorRouter
from app.router.v1.anime_router import AnimeRouter
from app.router.v1.episode_router import EpisodeRouter

app = FastAPI(
    title="BIRTHDAY ANIME",
    description="API for the consumption of episode release dates.")

app.include_router(AuthorRouter, tags=["Author"], prefix='/v1/author')
app.include_router(AnimeRouter, tags=["Anime"], prefix='/v1/anime')
app.include_router(EpisodeRouter, tags=["Episode"], prefix='/v1/episode')
