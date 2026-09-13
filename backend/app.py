# -*- coding: utf-8 -*-
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import os
try:
    from bedrock_service import bedrock_agent
except ImportError:
    from backend.bedrock_service import bedrock_agent

app = FastAPI(
    title="新北市校園治理情報平台 API",
    description="新北市各級學校與教保機構 治理指標評估與預警系統 API (AWS Bedrock 賦能)",
    version="3.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "institutions.json")
try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        INSTITUTIONS = json.load(f)
except Exception as e:
    print(f"Error loading institutions data: {e}")
    INSTITUTIONS = []

@app.get("/")
def read_root():
    ntpc = [i for i in INSTITUTIONS if i.get("city") == "新北市"]
    return {
        "system": "新北市校園治理情報平台 API (NTPC v3.1)",
        "status": "online",
        "cloud_architecture": "AWS us-west-2 (Oregon)",
        "ai_engine": "Amazon Bedrock (Claude 3.5 Sonnet, RPS<=1)",
        "total_institutions": len(INSTITUTIONS),
        "ntpc_institutions": len(ntpc)
    }

@app.get("/api/statistics")
def get_statistics():
    ntpc = [i for i in INSTITUTIONS if i.get("city") == "新北市"]
    total = len(ntpc)
    high = len([i for i in ntpc if i.get("risk_category") == "高風險"])
    medium = len([i for i in ntpc if i.get("risk_category") == "中風險"])
    low = len([i for i in ntpc if i.get("risk_category") == "低風險"])
    total_fines = sum(i.get("total_fines", 0) for i in ntpc)

    return {
        "total_institutions": total,
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "total_fines": total_fines,
        "high_schools": len([i for i in ntpc if "高中" in i.get("type", "") or "高職" in i.get("type", "")]),
        "junior_highs": len([i for i in ntpc if "國中" in i.get("type", "")]),
        "elem_schools": len([i for i in ntpc if "國小" in i.get("type", "")]),
        "preschools": len([i for i in ntpc if "幼兒園" in i.get("type", "")])
    }

@app.get("/api/institutions")
def get_institutions(
    city: str = Query(None, description="縣市"),
    risk: str = Query(None, description="風險等級"),
    keyword: str = Query(None, description="關鍵字搜尋")
):
    results = [i for i in INSTITUTIONS if i.get("city") == "新北市"] if not city else [i for i in INSTITUTIONS if city in i.get("city", "")]

    if risk and risk != "ALL":
        results = [i for i in results if i.get("risk_category") == risk]
    if keyword:
        kw = keyword.lower()
        results = [
            i for i in results
            if kw in i["name"].lower() or kw in i.get("district", "") or kw in i.get("address", "")
        ]

    return results

@app.get("/api/institution/{inst_id}")
def get_institution(inst_id: str):
    inst = next((i for i in INSTITUTIONS if i["id"] == inst_id), None)
    if not inst:
        return {"error": "Institution not found"}
    return inst

class ChatRequest(BaseModel):
    inst_id: Optional[str] = None
    message: str

@app.post("/api/chat")
def chat_with_agent(req: ChatRequest):
    inst = None
    if req.inst_id:
        inst = next((i for i in INSTITUTIONS if i["id"] == req.inst_id), None)

    msg = req.message.lower()

    # 若指定機構且包含稽查或手冊關鍵字，透過 AWS Bedrock 引擎產出
    if inst:
        if any(w in msg for w in ["稽查", "手冊", "清查", "突擊", "報告", "檢查", "處分"]):
            reply = bedrock_agent.generate_inspection_manual(inst, req.message)
        elif "班佛" in msg or "財務" in msg:
            b_score = inst.get("benford", {}).get("fin_risk_score", 20)
            b_status = inst.get("benford", {}).get("benford_status", "合格")
            reply = f"【{inst['name']} 班佛財務分析】\n首位數檢定異常分數：{b_score} 分，狀態：{b_status}。\n建議局端稽查員抽查近六個月大宗食材與代辦費採購標案合約，檢核是否存在人為假帳或刻意拆單規避招標情事。"
        else:
            reply = f"您好！已為您定位【{inst['name']}】。\n該機構綜合治理風險評分：{inst['total_score']} 分（{inst['risk_category']}），累計違規裁處 {inst.get('violation_count', 0)} 次。\n您可以點擊『產生突擊稽查手冊』，AI 將調用 Amazon Bedrock 自動產出即時實地盤查重點清單。"
    else:
        ntpc = [x for x in INSTITUTIONS if x.get("city") == "新北市"]
        high_ntpc = [x for x in ntpc if x.get("risk_category") == "高風險"]
        reply = f"【新北市校園治理 AI 智慧稽查室 (AWS Bedrock Engine)】\n新北市目前列管各級學校與幼托共 {len(ntpc)} 所，其中第一級高風險監控對象共 {len(high_ntpc)} 所（涉及重大師生比超收、黑牌教保員或採購異常）。\n請由地圖或名冊點選任一機構，我將為您以 AWS Bedrock 產出針對該校之專屬現場稽查指示書！"

    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
