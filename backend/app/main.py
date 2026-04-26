from fastapi import FastAPI
import logging

from app.core.logging import setup_logging
from app.api.v1.router import router as v1_router

# init logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Training Analyzer")

# API v1 routes
app.include_router(v1_router, prefix="/v1")