"""
数据库模型定义
"""
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Topic(Base):
    """话题表"""
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    cases = relationship("Case", back_populates="topic")


class Case(Base):
    """案例表"""
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    description = Column(Text, nullable=False)

    # 结构标注
    subject_structure = Column(String(50))  # 主体结构，如 "++-"
    object_structure = Column(String(50))   # 客体结构，如 "-+-"
    structure_key = Column(String(100), index=True)  # 完整结构键，如 "++- vs -+-"

    # 意图向量 (JSON格式字符串)
    intent_time = Column(Integer)      # 时间维度 0-10
    intent_benefit = Column(Integer)   # 利益维度 0-10
    intent_risk = Column(Integer)      # 风险维度 0-10

    # 跳变结果
    outcome = Column(String(50))  # 结果：成功/失败/部分成功
    outcome_description = Column(Text)

    # 元数据
    verified = Column(Integer, default=0)  # 是否已人工验证: 0=未验证, 1=已验证
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    topic = relationship("Topic", back_populates="cases")


class StructurePattern(Base):
    """结构辞表（策略库）"""
    __tablename__ = "structure_patterns"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    structure_key = Column(String(100), nullable=False, index=True)  # 结构键

    # 策略内容
    strategy = Column(Text, nullable=False)  # 推荐策略
    reasoning = Column(Text)  # 推理依据

    # 统计数据
    success_count = Column(Integer, default=0)  # 成功次数
    failure_count = Column(Integer, default=0)  # 失败次数
    success_rate = Column(Float, default=0.0)   # 成功率

    # 风险提示
    risk_warning = Column(Text)

    # 平均意图向量（用于相似度计算）
    avg_intent_time = Column(Float, default=0.0)
    avg_intent_benefit = Column(Float, default=0.0)
    avg_intent_risk = Column(Float, default=0.0)

    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    topic = relationship("Topic")


class Feedback(Base):
    """用户反馈表"""
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    pattern_id = Column(Integer, ForeignKey("structure_patterns.id"), nullable=False)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=True)  # 关联的案例（如果有）

    # 反馈内容
    strategy_used = Column(Text, nullable=False)  # 使用的策略
    result = Column(String(50), nullable=False)   # 实际结果：成功/失败/部分成功
    result_detail = Column(Text)  # 结果详情

    # 用户评价
    rating = Column(Integer)  # 1-5分评价
    comment = Column(Text)    # 用户评论

    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    pattern = relationship("StructurePattern")
    case = relationship("Case")
