"""
结构辞（策略）管理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..models.models import StructurePattern
from ..models.schemas import StructurePatternCreate, StructurePatternResponse

router = APIRouter(prefix="/patterns", tags=["patterns"])


@router.get("/", response_model=List[StructurePatternResponse])
def get_patterns(
    topic_id: int = None,
    structure_key: str = None,
    db: Session = Depends(get_db)
):
    """获取结构辞列表"""
    query = db.query(StructurePattern)

    if topic_id is not None:
        query = query.filter(StructurePattern.topic_id == topic_id)

    if structure_key is not None:
        query = query.filter(StructurePattern.structure_key == structure_key)

    patterns = query.order_by(StructurePattern.success_rate.desc()).all()
    return patterns


@router.get("/{pattern_id}", response_model=StructurePatternResponse)
def get_pattern(pattern_id: int, db: Session = Depends(get_db)):
    """获取单个结构辞"""
    pattern = db.query(StructurePattern).filter(
        StructurePattern.id == pattern_id
    ).first()
    if not pattern:
        raise HTTPException(status_code=404, detail="结构辞不存在")
    return pattern


@router.post("/", response_model=StructurePatternResponse)
def create_pattern(
    pattern: StructurePatternCreate,
    db: Session = Depends(get_db)
):
    """创建结构辞"""
    db_pattern = StructurePattern(**pattern.model_dump())
    db.add(db_pattern)
    db.commit()
    db.refresh(db_pattern)
    return db_pattern
