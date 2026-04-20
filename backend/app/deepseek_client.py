import os
import httpx
import asyncio
import json

DEESEEK_API_KEY = os.getenv("DEESEEK_API_KEY", "")
DEESEEK_URL = os.getenv("DEESEEK_URL", "").rstrip("/")
TIMEOUT = int(os.getenv("DEESEEK_TIMEOUT", "20"))

async def call_real_deepseek(system_prompt: str, user_prompt: str):
    url = DEESEEK_URL or "https://api.deepseek.example/v1/chat"
    headers = {"Authorization": f"Bearer {DEESEEK_API_KEY}", "Content-Type":"application/json"}
    payload = {
        "model": "gpt-deepseek-1",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 800
    }
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        r = await client.post(url, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()

async def call_deepseek(system_prompt: str, user_prompt: str):
    # If DEESEEK_API_KEY unset -> return mock (helpful for local dev)
    if not DEESEEK_API_KEY or not DEESEEK_URL:
        # generate a mock response that includes the expected JSON block at the end
        mock_json = {
            "overall_score": 62.5,
            "overall_level": "中",
            "scene_scores": {"family": 70.0, "work": 55.0, "social": 40.0},
            "recommendations": [
                "每天开窗通风 15 分钟，至少 3 次",
                "减少与吸烟者的近距离接触，尤其在室内",
                "若有呼吸不适，向全科/呼吸科就医咨询",
                "家庭内禁止室内吸烟，并使用空气净化器",
                "定期进行肺功能或体检监测"
            ]
        }
        text = (
            "总体评估：中等风险，评分 62.5/100。\n\n"
            "风险要点：\n- 暴露年限增加了长期风险。\n- 每日暴露时长较高，且环境较为密闭，导致浓度累积。\n\n"
            "场景分解：家庭 70/100（主要原因：与吸烟者同住/室内吸烟）、工作 55/100、社交 40/100。\n\n"
            "建议：\n- 开窗通风 15 分钟，每日 3 次；\n- 避免在家中吸烟；\n- 若有持续咳嗽或呼吸问题，尽早就医；\n- 考虑使用室内空气净化器并保持清洁；\n- 与家人讨论制定无烟家庭规则。\n\n参考：世界卫生组织相关二手烟危害总结。\n\n"
            + json.dumps(mock_json, ensure_ascii=False, indent=2)
        )
        # mimic DeepSeek response structure
        await asyncio.sleep(0.1)
        return {"choices": [{"message": {"content": text}}]}
    else:
        return await call_real_deepseek(system_prompt, user_prompt)
