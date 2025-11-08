"""
FastAPI主应用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .core.database import init_db
from .api import topics, cases, patterns, analysis, feedbacks

# 创建应用实例
app = FastAPI(
    title="StructLang认知结构分析系统",
    description="基于StructLang方法论的AI辅助认知结构分析MVP系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(topics.router)
app.include_router(cases.router)
app.include_router(patterns.router)
app.include_router(analysis.router)
app.include_router(feedbacks.router)


@app.on_event("startup")
async def startup_event():
    """启动时初始化数据库"""
    # 确保data目录存在
    os.makedirs("data", exist_ok=True)
    # 初始化数据库
    init_db()


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "StructLang认知结构分析系统API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}
