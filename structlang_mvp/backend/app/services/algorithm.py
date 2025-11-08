"""
核心算法模块
包含意图向量距离计算、结构匹配等核心算法
"""
import math
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from ..models.models import Case, StructurePattern
from ..models.schemas import IntentVector


class StructLangAlgorithm:
    """StructLang核心算法类"""

    @staticmethod
    def calculate_intent_distance(
        intent1: IntentVector,
        intent2: IntentVector
    ) -> float:
        """
        计算两个意图向量之间的欧氏距离

        公式: d = sqrt((t1-t2)² + (b1-b2)² + (r1-r2)²)

        Args:
            intent1: 第一个意图向量
            intent2: 第二个意图向量

        Returns:
            距离值（浮点数）
        """
        distance = math.sqrt(
            (intent1.time - intent2.time) ** 2 +
            (intent1.benefit - intent2.benefit) ** 2 +
            (intent1.risk - intent2.risk) ** 2
        )
        return distance

    @staticmethod
    def calculate_intent_distance_from_values(
        t1: int, b1: int, r1: int,
        t2: float, b2: float, r2: float
    ) -> float:
        """
        从原始值计算意图距离

        Args:
            t1, b1, r1: 第一个意图向量的时间、利益、风险
            t2, b2, r2: 第二个意图向量的时间、利益、风险

        Returns:
            距离值
        """
        distance = math.sqrt(
            (t1 - t2) ** 2 +
            (b1 - b2) ** 2 +
            (r1 - r2) ** 2
        )
        return distance

    @staticmethod
    def match_structure_patterns(
        db: Session,
        structure_key: str,
        topic_id: int,
        intent: IntentVector,
        limit: int = 5
    ) -> List[Tuple[StructurePattern, float, List[int]]]:
        """
        匹配结构辞（策略）

        1. 首先查找完全相同的结构键
        2. 计算意图向量距离
        3. 按距离排序
        4. 返回最相似的N个模式

        Args:
            db: 数据库会话
            structure_key: 结构键
            topic_id: 话题ID
            intent: 意图向量
            limit: 返回结果数量限制

        Returns:
            列表，每项包含 (StructurePattern, 意图距离, 相似案例ID列表)
        """
        # 查找相同结构键的所有模式
        patterns = db.query(StructurePattern).filter(
            StructurePattern.structure_key == structure_key,
            StructurePattern.topic_id == topic_id
        ).all()

        if not patterns:
            return []

        # 计算每个模式的意图距离
        results = []
        for pattern in patterns:
            distance = StructLangAlgorithm.calculate_intent_distance_from_values(
                intent.time, intent.benefit, intent.risk,
                pattern.avg_intent_time,
                pattern.avg_intent_benefit,
                pattern.avg_intent_risk
            )

            # 查找相似案例
            similar_cases = db.query(Case).filter(
                Case.structure_key == structure_key,
                Case.topic_id == topic_id,
                Case.verified == 1
            ).limit(3).all()

            case_ids = [case.id for case in similar_cases]

            results.append((pattern, distance, case_ids))

        # 按距离排序
        results.sort(key=lambda x: x[1])

        # 返回前N个
        return results[:limit]

    @staticmethod
    def find_similar_cases(
        db: Session,
        structure_key: str,
        topic_id: int,
        intent: IntentVector,
        limit: int = 10
    ) -> List[Tuple[Case, float]]:
        """
        查找相似案例

        Args:
            db: 数据库会话
            structure_key: 结构键
            topic_id: 话题ID
            intent: 意图向量
            limit: 返回结果数量

        Returns:
            列表，每项包含 (Case, 意图距离)
        """
        # 查找相同结构键的案例
        cases = db.query(Case).filter(
            Case.structure_key == structure_key,
            Case.topic_id == topic_id,
            Case.verified == 1
        ).all()

        if not cases:
            return []

        # 计算意图距离
        results = []
        for case in cases:
            distance = StructLangAlgorithm.calculate_intent_distance_from_values(
                intent.time, intent.benefit, intent.risk,
                float(case.intent_time),
                float(case.intent_benefit),
                float(case.intent_risk)
            )
            results.append((case, distance))

        # 按距离排序
        results.sort(key=lambda x: x[1])

        return results[:limit]

    @staticmethod
    def update_pattern_weights(
        db: Session,
        pattern_id: int,
        success: bool,
        success_increment: float = 0.05,
        failure_decrement: float = 0.03
    ):
        """
        更新结构辞权重

        根据反馈结果更新成功率和统计数据

        Args:
            db: 数据库会话
            pattern_id: 结构辞ID
            success: 是否成功
            success_increment: 成功时的权重增量
            failure_decrement: 失败时的权重减量
        """
        pattern = db.query(StructurePattern).filter(
            StructurePattern.id == pattern_id
        ).first()

        if not pattern:
            return

        # 更新统计数据
        if success:
            pattern.success_count += 1
        else:
            pattern.failure_count += 1

        # 重新计算成功率
        total_count = pattern.success_count + pattern.failure_count
        if total_count > 0:
            pattern.success_rate = pattern.success_count / total_count

        db.commit()

    @staticmethod
    def parse_structure_key(structure_key: str) -> Tuple[str, str]:
        """
        解析结构键

        Args:
            structure_key: 如 "++- vs -+-"

        Returns:
            (主体结构, 客体结构)
        """
        parts = structure_key.split(" vs ")
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()
        return "", ""

    @staticmethod
    def validate_aqt_structure(structure: str) -> bool:
        """
        验证AQT结构格式

        Args:
            structure: 如 "++-, "-+-", "??+"

        Returns:
            是否有效
        """
        if len(structure) != 3:
            return False

        valid_chars = {'+', '-', '?'}
        return all(c in valid_chars for c in structure)

    @staticmethod
    def build_structure_key(subject: str, obj: str) -> str:
        """
        构建结构键

        Args:
            subject: 主体结构
            obj: 客体结构

        Returns:
            结构键字符串
        """
        return f"{subject} vs {obj}"
