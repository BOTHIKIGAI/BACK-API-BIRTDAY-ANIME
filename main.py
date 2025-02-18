"""
Main module for the BIRTHDAY ANIME API.

This module initializes the FastAPI application and includes the router for handling
requests related to anime episode release dates.
"""

import logging

from fastapi import FastAPI

from app.config.logging import setup_logging
from app.middleware.logging_middleware import log_requests
from app.routers.v1.anime_router import AnimeRouter
from app.routers.v1.author_router import AuthorRouter
from app.routers.v1.birthday_router import BirthdayRouter
from app.routers.v1.episode_router import EpisodeRouter

setup_logging()
logger = logging.getLogger("BIRTHDAY_ANIME")

app = FastAPI(
    title="BIRTHDAY ANIME",
    description="API for the consumption of episode release dates."
)

app.middleware("http")(log_requests)

app.include_router(AuthorRouter, tags=["Author"], prefix='/v1/author')
app.include_router(AnimeRouter, tags=["Anime"], prefix='/v1/anime')
app.include_router(EpisodeRouter, tags=["Episode"], prefix='/v1/episode')
app.include_router(BirthdayRouter, tags=["Birthday"], prefix='/v1/birthday')
