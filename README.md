# Cytomine Upload Tool (Python)

這是一個簡單的 Python 工具，用來將影像上傳至 Cytomine 平台。適用於自動化任務、批次上傳流程。

📚 參考 API 文檔：https://doc.cytomine.com/dev-guide/faq/upload-python

---

## 🔧 使用參數

| 參數名稱       | 說明 |
|----------------|------|
| `host`         | Cytomine 網址，例如 `http://your-cytomine-host` |
| `upload_host`  | 上傳用網址，通常是 `host:8083`，可從 docker image 的 core 設定內查詢 |
| `public_key`   | 登入 Cytomine 網頁後，在帳號設定頁面可找到 |
| `private_key`  | 同上，與 public key 搭配使用以驗證 API 請求 |
| `storage_id`   | 可透過 API 取得（使用 `/api/storage.json`） |
| `project_id`   | （可選）指定上傳後自動歸入的專案 ID |
| `filepath`     | 欲上傳的檔案路徑（可支援單一或多個） |

---

## 🧪 範例使用方式

```bash
python upload.py \
  --host http://localhost \
  --upload_host http://localhost:8083 \
  --public_key YOUR_PUBLIC_KEY \
  --private_key YOUR_PRIVATE_KEY \
  --storage_id 123 \
  --project_id 456 \
  --filepath /path/to/your/file.tif
```

如未指定 `project_id`，影像會上傳至使用者預設空間，但不會自動掛入專案。

---

## 🛠 進階應用
- 批次上傳：可將此腳本結合 `for` 迴圈或資料夾掃描
- 與 pipeline 整合：可用於 AI 預測前置步驟（如上傳切片）

---

歡迎 Fork 或 PR 改善功能 🎉
