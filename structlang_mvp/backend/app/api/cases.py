"""
案例管理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..models.models import Case
from ..models.schemas import CaseCreate, CaseResponse

router = APIRouter(prefix="/cases", tags=["cases"])


@router.get("/", response_model=List[CaseResponse])
def get_cases(
    topic_id: int = None,
    verified: int = None,
    db: Session = Depends(get_db)
):
    """获取案例列表（可按话题和验证状态过滤）"""
    query = db.query(Case)

    if topic_id is not None:
        query = query.filter(Case.topic_id == topic_id)

    if verified is not None:
        query = query.filter(Case.verified == verified)

    cases = query.order_by(Case.created_at.desc()).all()
    return cases


@router.get("/{case_id}", response_model=CaseResponse)
def get_case(case_id: int, db: Session = Depends(get_db)):
    """获取单个案例"""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")
    return case


@router.post("/", response_model=CaseResponse)
def create_case(case: CaseCreate, db: Session = Depends(get_db)):
    """创建案例（手动标注）"""
    db_case = Case(**case.model_dump())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case


@router.put("/{case_id}/verify", response_model=CaseResponse)
def verify_case(case_id: int, db: Session = Depends(get_db)):
    """验证案例（标记为已人工确认）"""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")

    case.verified = 1
    db.commit()
    db.refresh(case)
    return case
