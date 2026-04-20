# smokefree

最小可运行的二手烟风险评估前后端骨架（Vite + Vue3 + Vant 前端，FastAPI 后端）。

## 快速运行（本地）

后端：
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# 启动
uvicorn app.main:app --reload --port 8000
```

前端：
```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

后端会在当前目录生成 `smokefree.db`（sqlite），其中包含留言板数据。

## 使用 DeepSeek（切换真实 AI）

目前后端默认在未设置 `DEESEEK_API_KEY` / `DEESEEK_URL` 时使用本地 mock 响应以便开发。
要接入真实 DeepSeek：

1. 在部署环境或本地创建 `.env` 并设置：
```
DEESEEK_API_KEY=你的_key
DEESEEK_URL=https://api.deepseek.example/v1/chat
```

2. 确保 `backend` 启动时这些 env 已生效（docker-compose 或系统 environment）。

## Docker（一键）
在仓库根目录运行：
```bash
# 创建 .env 并填入 DEESEEK_API_KEY/DEESEEK_URL 如果你有
docker-compose up --build
```
这样会在本机暴露 8000 (backend) 与 5173 (frontend)。

## 项目结构（简述）
- backend/: FastAPI 服务（/api/report, /api/comments）
- frontend/: Vite + Vue3 前端（Survey -> Dashboard -> 留言板）
- infra/: Dockerfile + docker-compose

## 后续（Day2/Day3）
- Day2：完善分步问卷、ECharts 图表（已包含基础），增强评分模型并添加历史趋势预测。
- Day3：扩展社区（分页、删改）、知识库页面（后台管理或 markdown 渲染）、UI 统一与配色打磨。

## 注意
- 请勿在前端暴露 DEESEEK_API_KEY。
- 对 AI 返回的 JSON 请在前端渲染前做基础校验；后端已在 mock/real 两种模式下保证返回包含 ai_report 字段。
