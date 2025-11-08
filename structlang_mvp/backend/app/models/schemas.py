"""
Pydantic模型（用于API请求和响应）
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============ 基础模型 ============

class IntentVector(BaseModel):
    """意图向量"""
    time: int = Field(ge=0, le=10, description="时间维度 0-10")
    benefit: int = Field(ge=0, le=10, description="利益维度 0-10")
    risk: int = Field(ge=0, le=10, description="风险维度 0-10")


class StructureAnnotation(BaseModel):
    """结构标注"""
    subject: str = Field(description="主体结构，如 ++-")
    object: str = Field(description="客体结构，如 -+-")
    structure_key: str = Field(description="完整结构键，如 ++- vs -+-")


# ============ 话题相关 ============

class TopicBase(BaseModel):
    """话题基础模型"""
    name: str
    description: Optional[str] = None


class TopicCreate(TopicBase):
    """创建话题"""
    pass


class TopicResponse(TopicBase):
    """话题响应"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============ 案例相关 ============

class CaseBase(BaseModel):
    """案例基础模型"""
    description: str
    topic_id: int


class CaseCreate(CaseBase):
    """创建案例（手动标注）"""
    subject_structure: str
    object_structure: str
    structure_key: str
    intent_time: int
    intent_benefit: int
    intent_risk: int
    outcome: str
    outcome_description: Optional[str] = None
    verified: int = 1


class CaseResponse(CaseBase):
    """案例响应"""
    id: int
    subject_structure: str
    object_structure: str
    structure_key: str
    intent_time: int
    intent_benefit: int
    intent_risk: int
    outcome: str
    outcome_description: Optional[str]
    verified: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ 结构辞相关 ============

class StructurePatternBase(BaseModel):
    """结构辞基础模型"""
    topic_id: int
    structure_key: str
    strategy: str
    reasoning: Optional[str] = None
    risk_warning: Optional[str] = None


class StructurePatternCreate(StructurePatternBase):
    """创建结构辞"""
    pass


class StructurePatternResponse(StructurePatternBase):
    """结构辞响应"""
    id: int
    success_count: int
    failure_count: int
    success_rate: float
    avg_intent_time: float
    avg_intent_benefit: float
    avg_intent_risk: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ 反馈相关 ============

class FeedbackCreate(BaseModel):
    """创建反馈"""
    pattern_id: int
    case_id: Optional[int] = None
    strategy_used: str
    result: str  # 成功/失败/部分成功
    result_detail: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class FeedbackResponse(FeedbackCreate):
    """反馈响应"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============ 分析请求和响应 ============

class AnalysisRequest(BaseModel):
    """分析请求"""
    question: str = Field(description="用户输入的问题描述")
    topic_id: int = Field(description="所属话题ID")


class AnalysisResult(BaseModel):
    """AI分析结果"""
    structure: StructureAnnotation
    intent: IntentVector
    reasoning: str  # AI的推理过程


class RecommendationItem(BaseModel):
    """推荐项"""
    pattern_id: int
    structure_key: str
    strategy: str
    reasoning: str
    success_rate: float
    risk_warning: Optional[str]
    intent_distance: float  # 意图向量距离
    similar_cases: List[int]  # 相似案例ID列表


class AnalysisResponse(BaseModel):
    """分析响应（完整流程）"""
    analysis: AnalysisResult
    recommendations: List[RecommendationItem]
    message: str


# ============ 模型初始化 ============

class InitializeRequest(BaseModel):
    """初始化请求"""
    include_sample_data: bool = True
