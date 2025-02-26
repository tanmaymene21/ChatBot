from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import desc
import uuid
from datetime import datetime

from app.db.database import get_db
from app.bot.graph import process_query
from app.models.product import Product
from app.models.chat import ChatHistory as ChatHistoryModel
from app.api.auth import get_current_user
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatHistory as ChatHistorySchema

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        chat_id = request.chat_id or str(uuid.uuid4())
        response = process_query(request.message)
        
        title = None
        if not request.chat_id:
            title = request.message[:50] + "..." if len(request.message) > 50 else request.message
        
        chat_history = ChatHistoryModel(
            chat_id=chat_id,
            user_id=current_user["id"],
            user_message=request.message,
            bot_response=response,
            title=title
        )
        db.add(chat_history)
        db.commit()
        
        return ChatResponse(response=response, chat_id=chat_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[ChatHistorySchema])
async def get_chat_history(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    latest_chats = (
        db.query(ChatHistoryModel)
        .filter(ChatHistoryModel.user_id == current_user["id"])
        .order_by(desc(ChatHistoryModel.timestamp))
        .all()
    )
    
    chat_history = {}
    for chat in latest_chats:
        if chat.chat_id not in chat_history:
            chat_history[chat.chat_id] = chat
    
    return list(chat_history.values())

@router.get("/chat/{chat_id}", response_model=List[ChatHistorySchema])
async def get_chat_messages(
    chat_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    messages = (
        db.query(ChatHistoryModel)
        .filter(
            ChatHistoryModel.user_id == current_user["id"],
            ChatHistoryModel.chat_id == chat_id
        )
        .order_by(ChatHistoryModel.timestamp)
        .all()
    )
    
    if not messages:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return [ChatHistorySchema.from_orm(msg) for msg in messages]