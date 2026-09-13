# -*- coding: utf-8 -*-
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI(
    title="小小守護員 Smart Watchdog API",
    description="全國幼兒教保及托育機構 智慧風險稽查與預警系統 API",
    version="2.0.0"
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
def root():
    return {
        "system": "小小守護員 Smart Watchdog",
        "version": "2.0.0",
        "status": "online",
        "total_institutions": len(INSTITUTIONS)
    }

@app.get("/api/statistics")
def get_statistics():
    total = len(INSTITUTIONS)
    high = sum(1 for i in INSTITUTIONS if i["risk_category"] == "高風險")
    medium = sum(1 for i in INSTITUTIONS if i["risk_category"] == "中風險")
    low = sum(1 for i in INSTITUTIONS if i["risk_category"] == "低風險")
    total_fines = sum(i.get("total_fines", 0) for i in INSTITUTIONS)
    total_violations = sum(i.get("violation_count", 0) for i in INSTITUTIONS)

    return {
        "total": total,
        "high": high,
        "medium": medium,
        "low": low,
        "total_fines": total_fines,
        "total_violations": total_violations
    }

@app.get("/api/institutions")
def list_institutions(
    city: str = Query(None, description="篩選縣市"),
    risk: str = Query(None, description="篩選風險類別"),
    keyword: str = Query(None, description="關鍵字搜尋")
):
    results = INSTITUTIONS

    if city and city != "ALL":
        results = [i for i in results if city in i["city"]]
    if risk and risk != "ALL":
        results = [i for i in results if i["risk_category"] == risk]
    if keyword:
        kw = keyword.lower()
        results = [
            i for i in results 
            if kw in i["name"].lower() or kw in i["district"] or kw in i["address"]
        ]

    return results

@app.get("/api/institution/{inst_id}")
def get_institution(inst_id: str):
    inst = next((i for i in INSTITUTIONS if i["id"] == inst_id), None)
    if not inst:
        return {"error": "Institution not found"}
    return inst

class ChatRequest(BaseModel):
    inst_id: str
    message: str

@app.post("/api/chat")
def chat_with_agent(req: ChatRequest):
    inst = next((i for i in INSTITUTIONS if i["id"] == req.inst_id), None)
    if not inst:
        return {"reply": "查無此機構資料，請確認機構編號。"}

    msg = req.message.lower()
    if "稽查" in msg or "突擊" in msg or "清單" in msg:
        reply = f"【{inst['name']} 突擊稽查指示】\n1. 現場清查在園幼兒人數，比對核定容量 {inst['approved_capacity']} 人。\n2. 調閱最近 30 日監視器錄影，排除死角。\n3. 比對教職員合格證書與投保名冊。\n4. 查驗廚房食品留樣 48 小時合規性。"
    elif "財務" in msg or "班佛" in msg:
        reply = f"【{inst['name']} 班佛財務分析】\n異常指標：{inst['benford']['fin_risk_score']} 分，狀態：{inst['benford']['benford_status']}。\n建議調閱近六個月對外收款單據與收費備查項目是否相符。"
    else:
        reply = f"已收到針對 {inst['name']} 的諮詢。該機構目前風險總分為 {inst['total_score']} 分（{inst['risk_category']}），累計裁罰 {inst['violation_count']} 次。建議參照五維雷達圖評估其照顧安全。"

    return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)