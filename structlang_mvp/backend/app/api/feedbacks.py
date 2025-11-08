"""
反馈管理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..models.models import Feedback, StructurePattern
from ..models.schemas import FeedbackCreate, FeedbackResponse
from ..services.algorithm import StructLangAlgorithm

router = APIRouter(prefix="/feedbacks", tags=["feedbacks"])


@router.post("/", response_model=FeedbackResponse)
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
):
    """
    创建反馈并更新策略权重
    """
    # 验证策略是否存在
    pattern = db.query(StructurePattern).filter(
        StructurePattern.id == feedback.pattern_id
    ).first()
    if not pattern:
        raise HTTPException(status_code=404, detail="策略不存在")

    # 创建反馈记录
    db_feedback = Feedback(**feedback.model_dump())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)

    # 更新策略权重
    success = feedback.result in ["成功", "部分成功"]
    StructLangAlgorithm.update_pattern_weights(
        db=db,
        pattern_id=feedback.pattern_id,
        success=success
    )

    return db_feedback


@router.get("/", response_model=List[FeedbackResponse])
def get_feedbacks(
    pattern_id: int = None,
    db: Session = Depends(get_db)
):
    """获取反馈列表"""
    query = db.query(Feedback)

    if pattern_id is not None:
        query = query.filter(Feedback.pattern_id == pattern_id)

    feedbacks = query.order_by(Feedback.created_at.desc()).all()
    return feedbacks
