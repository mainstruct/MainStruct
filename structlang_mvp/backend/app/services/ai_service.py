"""
AI服务模块
集成Claude API进行结构提取和分析
"""
import json
import anthropic
from typing import Dict, Any
from ..core.config import settings
from ..models.schemas import StructureAnnotation, IntentVector, AnalysisResult


class AIService:
    """AI服务类，封装Claude API调用"""

    def __init__(self):
        """初始化AI服务"""
        self.client = anthropic.Anthropic(
            api_key=settings.anthropic_api_key
        )
        self.model = "claude-sonnet-4-20250514"

    def extract_structure(self, question: str, topic: str) -> AnalysisResult:
        """
        从问题描述中提取结构标注和意图向量

        Args:
            question: 用户的问题描述
            topic: 话题名称

        Returns:
            AnalysisResult对象
        """
        # 构建提示词
        prompt = self._build_extraction_prompt(question, topic)

        try:
            # 调用Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # 解析响应
            response_text = message.content[0].text
            result = self._parse_extraction_response(response_text)

            return result

        except Exception as e:
            raise Exception(f"AI分析失败: {str(e)}")

    def _build_extraction_prompt(self, question: str, topic: str) -> str:
        """
        构建提取提示词

        Args:
            question: 问题描述
            topic: 话题

        Returns:
            提示词字符串
        """
        prompt = f"""你是一个认知结构分析专家，使用StructLang方法论分析人际互动问题。

# StructLang方法论
StructLang通过AQT三维度分析主客体状态：
- A (Action/行动): + 主动, - 被动, ? 未知
- Q (Quality/能力): + 强势, - 弱势, ? 未知
- T (aTtitude/态度): + 积极, - 消极, ? 未知

意图向量包含三个维度（0-10分）：
- 时间（Time）: 紧迫度，0=不急，10=极其紧迫
- 利益（Benefit）: 利益期望，0=无利益诉求，10=重大利益
- 风险（Risk）: 风险承受度，0=零风险容忍，10=可承受高风险

# 话题
{topic}

# 用户问题
{question}

# 任务
请分析这个问题，提取以下信息：

1. 识别主体（提问者）和客体（对方）
2. 分析主体的AQT状态（行动/能力/态度 各+/-/?）
3. 分析客体的AQT状态
4. 评估意图向量（时间/利益/风险 各0-10分）
5. 提供推理依据

请以JSON格式返回结果：
{{
  "subject_structure": "+++",
  "object_structure": "-+-",
  "intent_time": 7,
  "intent_benefit": 8,
  "intent_risk": 5,
  "reasoning": "详细的分析推理过程..."
}}

只返回JSON，不要其他文字。"""

        return prompt

    def _parse_extraction_response(self, response: str) -> AnalysisResult:
        """
        解析AI响应

        Args:
            response: Claude的响应文本

        Returns:
            AnalysisResult对象
        """
        try:
            # 提取JSON部分
            response = response.strip()

            # 如果响应包含markdown代码块，提取其中的JSON
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                response = response[start:end].strip()
            elif "```" in response:
                start = response.find("```") + 3
                end = response.find("```", start)
                response = response[start:end].strip()

            # 解析JSON
            data = json.loads(response)

            # 构建结构键
            structure_key = f"{data['subject_structure']} vs {data['object_structure']}"

            # 创建返回对象
            result = AnalysisResult(
                structure=StructureAnnotation(
                    subject=data["subject_structure"],
                    object=data["object_structure"],
                    structure_key=structure_key
                ),
                intent=IntentVector(
                    time=data["intent_time"],
                    benefit=data["intent_benefit"],
                    risk=data["intent_risk"]
                ),
                reasoning=data.get("reasoning", "")
            )

            return result

        except json.JSONDecodeError as e:
            raise Exception(f"解析AI响应失败: {str(e)}\n响应内容: {response}")
        except KeyError as e:
            raise Exception(f"AI响应缺少必要字段: {str(e)}")

    def generate_strategy_suggestion(
        self,
        question: str,
        structure_key: str,
        existing_strategies: list
    ) -> str:
        """
        基于问题和现有策略，生成新的策略建议

        Args:
            question: 原始问题
            structure_key: 结构键
            existing_strategies: 现有策略列表

        Returns:
            策略建议文本
        """
        strategies_text = "\n".join([
            f"- {s['strategy']} (成功率: {s['success_rate']:.1%})"
            for s in existing_strategies
        ])

        prompt = f"""基于以下信息，提供一个策略建议：

# 问题
{question}

# 结构分析
{structure_key}

# 现有类似策略
{strategies_text if strategies_text else "暂无"}

请提供一个简洁的策略建议（1-2句话），以及可能的风险提示。"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return message.content[0].text.strip()

        except Exception as e:
            return f"策略生成失败: {str(e)}"
