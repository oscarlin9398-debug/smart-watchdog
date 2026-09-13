# 新北市校園治理情報平台 (Smart Watchdog)
> **競賽命題：教保機構風險監測：教育局**  
> 新北市學前幼托與 K-12 校園多維治理、食安監測與智慧風險預警平台

---

## 📌 專案簡介 (Project Overview)

本專案「**新北市校園治理情報平台**（Smart Watchdog）」專為**新北市政府教育局「教保機構風險監測」**命題量身打造。平台整合了新北市 **232 所** 幼托園所（公幼、非營利、準公共、私立）以及高國中小學完整學制數據，結合政府開放資料、歷史稽查紀錄、電子採購數據與網路真實評價，打造新一代「以數據驅動、AI 為輔助」之校園與教保安全全景監測系統。

### 🌟 核心特色
1. **全學制覆蓋**：全面收錄新北市幼托園所（111 所）、國民小學（55 所）、國民中學（39 所）及高級中等學校（27 所）。
2. **多維治理指標（5D 指標模型）**：
   - 師生比合規與合格教保人員比率
   - 營養午餐食材檢驗與校園食安稽查
   - 校園安全、防墜設施與遊具檢驗
   - 採購合約審查（應用**班佛定律 Benford's Law** 異常偵測）
   - Google Places 網路公眾評價與情感分析
3. **GIS 地理資訊可視化**：以新北市府為中心，支援 29 個行政區快選與圖層聚類分析。
4. **AI 智慧稽查室**：結合大語言模型生成專業校園治理體檢報告與重點稽查改善建議。
5. **雙校治理對比 (Dual-School Compare)**：雷達圖直觀對比兩所機構指標落差。
6. **全民監督吹哨者機制 (Whistleblower Gateway)**：匿名檢舉與防偽雜湊存證。

---

## 📊 數據及資料運用 (Data & Methodology)

- **教育部全國教保資訊網 API**：幼兒園基本立案、核定人數、收退費標準、處分違規歷史。
- **新北市政府開放資料平台 (NTPC Open Data)**：高國中小校舍、營養午餐合約與食材登錄。
- **政府電子採購網 (e-Procurement)**：學校修繕、團膳午餐招標金額（導入班佛定律檢定防弊）。
- **Google Maps / Places API**：家長真實評價、星級分佈、負評情感分析。
- **全國校園通報與重大安全通報統計模型**。

---

## ☁️ AWS 雲端技術架構 (AWS Architecture)

針對競賽規範之雲端技術架構設計如下：

```text
[ 客戶端瀏覽器 / 行動端 ]
        │
        ▼ (HTTPS)
[ Amazon CloudFront (全球 CDN 加速與防護) ]
        │
        ├─► [ AWS S3 Bucket (靜態網站託管 - React SPA 前端) ]
        │
        ▼ (API 路由 /api/*)
[ Application Load Balancer (ALB) ]
        │
        ▼
[ Amazon ECS (Fargate 無伺服器容器化後端 - FastAPI) ]
        │
        ├─► [ Amazon Aurora PostgreSQL / RDS (結構化學校與稽查資料庫) ]
        ├─► [ Amazon OpenSearch Service (全文檢索與名冊即時過濾) ]
        ├─► [ Amazon Bedrock / Claude (AI 智慧稽查與報告生成模組) ]
        └─► [ Amazon CloudWatch (日誌稽核與異常預警告警) ]
```

---

## 💻 本地快速啟動 (Local Quick Start)

### 1. 前端 (Frontend)
```bash
cd frontend
npm install
npm run dev
# 前端服務將運行於 http://localhost:5173
```

### 2. 後端 (Backend)
```bash
cd backend
pip install fastapi uvicorn pydantic
python -m uvicorn app:app --port 8000
# 後端 API 將運行於 http://localhost:8000
```

---

## 🛠️ 技術棧 (Tech Stack)

- **Frontend**: React 18, Vite, TailwindCSS / Modern Light Theme, Lucide React, Leaflet GIS
- **Backend**: Python 3.12, FastAPI, Uvicorn, Pydantic
- **Data & Analytics**: Pandas, NumPy, Benford's Law Audit Algorithm
- **AI & Cloud**: AWS Bedrock, Cloudflare Tunnel, RESTful APIs

---

## 📄 授權條款 (License)
本專案依 MIT License 開源發布，提供教育與競賽評審參考。
