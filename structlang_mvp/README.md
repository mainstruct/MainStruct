# StructLang 认知结构分析系统 MVP

基于 StructLang 方法论的 AI 辅助认知结构分析系统，通过分析人际互动中的主客体结构和意图向量，提供基于案例的策略推荐。

## 🎯 核心功能

1. **智能结构提取**：AI 自动分析问题，提取主体/客体的 AQT 状态
2. **意图向量分析**：评估时间、利益、风险三维度（0-10 分）
3. **案例匹配**：基于结构键和意图距离匹配相似案例
4. **策略推荐**：推荐历史成功策略，显示成功率和风险提示
5. **反馈学习**：收集用户反馈，动态更新策略权重

## 📊 StructLang 方法论

### AQT 三维度分析

- **A (Action/行动)**：+ 主动，- 被动，? 未知
- **Q (Quality/能力)**：+ 强势，- 弱势，? 未知
- **T (aTtitude/态度)**：+ 积极，- 消极，? 未知

### 意图向量

- **时间（Time）**：紧迫度，0=不急，10=极其紧迫
- **利益（Benefit）**：利益期望，0=无利益诉求，10=重大利益
- **风险（Risk）**：风险承受度，0=零风险容忍，10=可承受高风险

### 核心算法

**意图距离计算**：
```
d = sqrt((t1-t2)² + (b1-b2)² + (r1-r2)²)
```

**权重更新规则**：
- 成功：权重 +0.05
- 失败：权重 -0.03

## 🏗️ 技术架构

### 技术栈

- **后端**：FastAPI + SQLAlchemy + SQLite
- **AI**：Claude API (claude-sonnet-4)
- **前端**：Streamlit
- **Python**: 3.8+

### 项目结构

```
structlang_mvp/
├── backend/
│   └── app/
│       ├── api/              # API路由
│       │   ├── topics.py     # 话题管理
│       │   ├── cases.py      # 案例管理
│       │   ├── patterns.py   # 结构辞管理
│       │   ├── analysis.py   # 分析接口
│       │   └── feedbacks.py  # 反馈接口
│       ├── core/             # 核心配置
│       │   ├── config.py     # 应用配置
│       │   └── database.py   # 数据库连接
│       ├── models/           # 数据模型
│       │   ├── models.py     # SQLAlchemy模型
│       │   └── schemas.py    # Pydantic模型
│       ├── services/         # 业务逻辑
│       │   ├── ai_service.py # Claude API集成
│       │   └── algorithm.py  # 核心算法
│       └── main.py           # 应用入口
├── frontend/
│   └── app.py                # Streamlit前端
├── scripts/
│   ├── init_data.py          # 数据初始化
│   ├── start_backend.sh      # 启动后端
│   └── start_frontend.sh     # 启动前端
├── data/                     # 数据库文件
├── requirements.txt          # 依赖列表
├── .env.example              # 环境变量模板
└── README.md                 # 项目文档
```

### 数据库设计

**topics（话题）**
- id, name, description, created_at

**cases（案例）**
- id, topic_id, description
- subject_structure, object_structure, structure_key
- intent_time, intent_benefit, intent_risk
- outcome, outcome_description, verified

**structure_patterns（结构辞/策略库）**
- id, topic_id, structure_key
- strategy, reasoning, risk_warning
- success_count, failure_count, success_rate
- avg_intent_time, avg_intent_benefit, avg_intent_risk

**feedbacks（反馈）**
- id, pattern_id, case_id
- strategy_used, result, result_detail
- rating, comment

## 🚀 快速开始

### 1. 环境准备

**安装依赖**：
```bash
cd structlang_mvp
pip install -r requirements.txt
```

**配置环境变量**：
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 ANTHROPIC_API_KEY
```

### 2. 初始化数据

```bash
python scripts/init_data.py
```

这将创建：
- 3 个话题（职场晋升、消费维权、商业谈判）
- 30 个标注案例
- 8 个结构辞（策略模式）

### 3. 启动服务

**方式一：使用脚本（推荐）**

```bash
# 终端1：启动后端
./scripts/start_backend.sh

# 终端2：启动前端
./scripts/start_frontend.sh
```

**方式二：手动启动**

```bash
# 终端1：启动后端
cd backend
uvicorn app.main:app --reload

# 终端2：启动前端
cd frontend
streamlit run app.py
```

### 4. 访问应用

- **前端界面**：http://localhost:8501
- **后端API文档**：http://localhost:8000/docs
- **健康检查**：http://localhost:8000/health

## 📖 使用指南

### 问题分析流程

1. **选择话题**：从下拉菜单选择问题所属话题
2. **输入问题**：详细描述你遇到的情况
3. **AI 分析**：系统自动提取结构和意图
4. **查看推荐**：获得策略推荐和成功率
5. **提交反馈**：使用后反馈结果，帮助系统学习

### 案例管理

- **查看案例**：按话题和验证状态筛选
- **验证案例**：确认 AI 标注的准确性
- **案例积累**：系统自动保存未匹配的新案例

### 系统统计

查看话题数量、案例分布等统计信息

## 🔧 API 接口

### 核心接口

**分析问题**
```http
POST /analysis/
Content-Type: application/json

{
  "question": "我想申请晋升，但老板态度模糊...",
  "topic_id": 1
}
```

**提交反馈**
```http
POST /feedbacks/
Content-Type: application/json

{
  "pattern_id": 1,
  "strategy_used": "主动展示成果...",
  "result": "成功",
  "rating": 5
}
```

**获取话题列表**
```http
GET /topics/
```

**获取案例列表**
```http
GET /cases/?topic_id=1&verified=1
```

完整 API 文档：访问 http://localhost:8000/docs

## 📊 MVP 范围

### 已实现

✅ 3 个话题领域
✅ 30 个手动标注初始案例
✅ AI 辅助结构提取
✅ 基于结构键的策略匹配
✅ 意图向量距离计算
✅ 反馈收集和权重更新
✅ Streamlit 交互界面

### 未来扩展

- [ ] 更多话题领域
- [ ] 结构模糊匹配（相似但非完全相同的结构）
- [ ] 案例推理链可视化
- [ ] 用户账户系统
- [ ] 策略效果追踪
- [ ] 批量导入案例
- [ ] 导出分析报告

## 🛠️ 开发指南

### 添加新话题

1. 在数据库中添加话题记录
2. 准备至少 10 个标注案例
3. 创建初始结构辞

### 自定义算法

编辑 `backend/app/services/algorithm.py`：
- 修改意图距离计算公式
- 调整权重更新参数
- 实现新的匹配策略

### 扩展 AI 提示词

编辑 `backend/app/services/ai_service.py` 中的 `_build_extraction_prompt` 方法

## ⚠️ 注意事项

1. **API Key 安全**：不要将 `.env` 文件提交到版本控制
2. **数据备份**：定期备份 `data/structlang.db` 数据库文件
3. **案例质量**：人工验证对系统准确性至关重要
4. **成本控制**：每次分析都会调用 Claude API，注意使用量

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 发起 Pull Request

## 📄 许可证

MIT License

## 📮 联系方式

如有问题或建议，请提交 Issue。

---

**StructLang MVP v1.0.0** - 让认知结构分析变得简单智能
