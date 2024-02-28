from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import logging
from config.logger_config import setup_logger

from app.api.v1.inference_api import router as inference_router
from app.api.v1.websocket_api import websocket_endpoint


# Initialize FastAPI application
app = FastAPI()
setup_logger()
logger = logging.getLogger()

origins =["*"]

# Middleware settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST API 라우터 추가
app.include_router(inference_router, prefix="/api/v1")

# 웹소켓 경로 추가
@app.websocket("/real-time/transcribe")
async def websocket_route(websocket: WebSocket):
    await websocket_endpoint(websocket)