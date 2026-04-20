from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from .models import SurveyIn, ReportOut, CommentIn, CommentOut
from .risk import compute_overall_score
from .deepseek_client import call_deepseek
from .db import init_db, get_comments, add_comment

app = FastAPI(title="SmokeFree API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """你是“专业的二手烟健康风险评估专家”。你的目标是基于用户提供的问卷信息（age, exposure_years, hours_per_day, main_environment, environment_enclosed, living_with_smoker, extra_notes）以温暖、专业、有建设性的语气输出评估报告。输出格式请包含人类可读部分，并在最后附上机器可解析 JSON 字段，格式如下：
{
 "overall_score": number,
 "overall_level": "低"|"中"|"高",
 "scene_scores": { "family": number, "work": number, "social": number },
 "recommendations": [string, ...]
}
如果缺少字段，指出不确定性并使用保守估计。"""

# init sqlite DB
init_db()

@app.post("/api/report", response_model=ReportOut)
async def generate_report(survey: SurveyIn):
    # compute scores locally
    scores = compute_overall_score(survey)
    # build user prompt for DeepSeek including survey + local scores
    user_prompt = (
        "请基于以下用户问卷与本地评分生成一份评估报告，按 system 提示的输出规范返回人类可读报告并在最后返回 JSON：\n\n"
        f"问卷: {survey.json()}\n\n本地评分: {json.dumps(scores, ensure_ascii=False)}"
    )
    try:
        ai_resp = await call_deepseek(SYSTEM_PROMPT, user_prompt)
    except Exception as e:
        # fallback: return local score + simple message
        return {
            "overall_score": scores["overall_score"],
            "overall_level": scores["overall_level"],
            "scene_scores": scores["scene_scores"],
            "ai_report": (
                "（AI 服务不可用，已返回本地计算结果）\n\n"
                f"本地评分：{scores}\n\n请在部署环境中设置 DEESEEK_API_KEY/DEESEEK_URL 后重试以获取 AI 报告。"
            ),
        }

    # expect ai_resp like {"choices":[{"message":{"content": "...text..."}}]}
    content = ""
    try:
        content = ai_resp.get("choices", [])[0].get("message", {}).get("content", "")
    except Exception:
        content = str(ai_resp)

    return {
        "overall_score": scores["overall_score"],
        "overall_level": scores["overall_level"],
        "scene_scores": scores["scene_scores"],
        "ai_report": content,
    }

@app.get("/api/comments", response_model=list[CommentOut])
def api_get_comments():
    return get_comments()

@app.post("/api/comments", response_model=CommentOut)
def api_post_comment(comment: CommentIn):
    return add_comment(comment)
