# StructLang MVP 快速开始

10分钟内启动并运行 StructLang 认知结构分析系统！

## 📋 前置要求

- Python 3.8 或更高版本
- Anthropic API Key（从 https://console.anthropic.com 获取）

## 🚀 5 步快速启动

### 步骤 1：安装依赖

```bash
cd structlang_mvp
pip install -r requirements.txt
```

### 步骤 2：配置 API Key

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，添加你的 API Key
# 使用任何文本编辑器打开 .env
# 将 your_api_key_here 替换为你的实际 API Key
```

`.env` 文件内容示例：
```bash
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DATABASE_URL=sqlite:///./data/structlang.db
FRONTEND_PORT=8501
API_BASE_URL=http://localhost:8000
```

### 步骤 3：初始化数据库

```bash
python scripts/init_data.py
```

这将创建：
- ✅ 3 个话题（职场晋升、消费维权、商业谈判）
- ✅ 30 个标注案例
- ✅ 8 个结构辞策略

### 步骤 4：启动后端服务

**新开一个终端**，运行：

```bash
cd structlang_mvp
./scripts/start_backend.sh
```

或者手动启动：
```bash
cd structlang_mvp/backend
uvicorn app.main:app --reload
```

看到类似输出表示成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 步骤 5：启动前端界面

**再开一个新终端**，运行：

```bash
cd structlang_mvp
./scripts/start_frontend.sh
```

或者手动启动：
```bash
cd structlang_mvp/frontend
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501

## 🎉 开始使用

### 第一次分析

1. 在前端选择话题："职场晋升"
2. 输入问题描述，例如：
   ```
   我在公司工作3年，业绩优秀，想申请晋升为高级工程师。
   跟老板提过两次，他总说"再看看"，态度很模糊。
   ```
3. 点击"开始分析"
4. 查看 AI 分析的结构、意图和策略推荐
5. 尝试提交反馈

### 探索其他功能

- **案例管理**：查看和验证系统中的案例
- **系统统计**：查看数据概览
- **API 文档**：访问 http://localhost:8000/docs

## 🔧 故障排查

### 问题：pip install 失败

**解决方案**：
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像（如果在中国）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题：API Key 错误

**错误信息**：`Authentication failed` 或 `Invalid API key`

**解决方案**：
1. 检查 `.env` 文件中的 API Key 是否正确
2. 确保 API Key 以 `sk-ant-` 开头
3. 确认 API Key 有效且有余额

### 问题：端口被占用

**错误信息**：`Address already in use`

**解决方案**：
```bash
# 方案1: 更改端口
# 编辑 .env 文件，修改 BACKEND_PORT 或 FRONTEND_PORT

# 方案2: 杀死占用端口的进程（Linux/Mac）
lsof -ti:8000 | xargs kill -9  # 后端端口
lsof -ti:8501 | xargs kill -9  # 前端端口

# Windows
netstat -ano | findstr :8000
taskkill /PID <进程ID> /F
```

### 问题：数据库初始化失败

**解决方案**：
```bash
# 删除旧数据库
rm -rf data/structlang.db

# 重新初始化
python scripts/init_data.py
```

### 问题：前端无法连接后端

**解决方案**：
1. 确认后端正在运行（访问 http://localhost:8000/health）
2. 检查 `.env` 中的 `API_BASE_URL` 是否正确
3. 检查防火墙设置

## 📚 下一步

- 📖 阅读 [完整文档](README.md)
- 📝 查看 [使用指南](USAGE_GUIDE.md)
- 🔍 浏览案例库，理解 StructLang 方法论
- 💡 尝试分析你自己遇到的实际问题

## 💬 获取帮助

- 查看项目 README.md
- 检查 API 文档：http://localhost:8000/docs
- 提交 GitHub Issue

---

祝你使用愉快！StructLang 让认知结构分析变得简单智能。
