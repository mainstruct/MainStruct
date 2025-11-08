"""
分析API（核心功能）
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..models.models import Topic, Case
from ..models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    RecommendationItem
)
from ..services.ai_service import AIService
from ..services.algorithm import StructLangAlgorithm

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/", response_model=AnalysisResponse)
def analyze_question(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    分析用户问题的完整流程：
    1. AI提取结构和意图
    2. 匹配相似案例
    3. 推荐策略
    """
    # 验证话题是否存在
    topic = db.query(Topic).filter(Topic.id == request.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="话题不存在")

    try:
        # 1. AI分析提取结构和意图
        ai_service = AIService()
        analysis = ai_service.extract_structure(
            question=request.question,
            topic=topic.name
        )

        # 2. 匹配结构辞（策略）
        patterns = StructLangAlgorithm.match_structure_patterns(
            db=db,
            structure_key=analysis.structure.structure_key,
            topic_id=request.topic_id,
            intent=analysis.intent,
            limit=5
        )

        # 3. 构建推荐列表
        recommendations = []
        for pattern, distance, case_ids in patterns:
            recommendations.append(RecommendationItem(
                pattern_id=pattern.id,
                structure_key=pattern.structure_key,
                strategy=pattern.strategy,
                reasoning=pattern.reasoning or "",
                success_rate=pattern.success_rate,
                risk_warning=pattern.risk_warning,
                intent_distance=round(distance, 2),
                similar_cases=case_ids
            ))

        # 4. 如果没有找到匹配的策略，保存为新案例（待验证）
        if not recommendations:
            # 创建未验证的案例
            new_case = Case(
                topic_id=request.topic_id,
                description=request.question,
                subject_structure=analysis.structure.subject,
                object_structure=analysis.structure.object,
                structure_key=analysis.structure.structure_key,
                intent_time=analysis.intent.time,
                intent_benefit=analysis.intent.benefit,
                intent_risk=analysis.intent.risk,
                outcome="待确认",
                verified=0
            )
            db.add(new_case)
            db.commit()

            message = "未找到匹配的策略，已保存为新案例待人工确认"
        else:
            message = f"找到 {len(recommendations)} 个相关策略"

        return AnalysisResponse(
            analysis=analysis,
            recommendations=recommendations,
            message=message
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/similar-cases/{structure_key}")
def get_similar_cases(
    structure_key: str,
    topic_id: int,
    db: Session = Depends(get_db)
):
    """获取相似案例"""
    cases = db.query(Case).filter(
        Case.structure_key == structure_key,
        Case.topic_id == topic_id,
        Case.verified == 1
    ).limit(10).all()

    return [
        {
            "id": case.id,
            "description": case.description,
            "outcome": case.outcome,
            "intent": {
                "time": case.intent_time,
                "benefit": case.intent_benefit,
                "risk": case.intent_risk
            }
        }
        for case in cases
    ]
