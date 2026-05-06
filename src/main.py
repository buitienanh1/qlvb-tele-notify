import os
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv
import requests
import logging
from datetime import datetime

# Load environment variables
load_dotenv('config/.env')

# Logging setup
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_dir}/server.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(title="QLVB Error Notification Gateway")

# --- Models ---
class QLVBErrorPayload(BaseModel):
    """The expected JSON structure from QLVB API"""
    unitName: str = Field(..., description="Tên đơn vị")
    unitCode: Optional[str] = Field(None, description="Mã đơn vị")
    docId: str = Field(..., description="Mã văn bản")
    docName: str = Field(..., description="Tên văn bản")
    function: str = Field(..., description="Hàm bị lỗi (sendDoc/recvStatus)")
    status: str = Field(..., description="Trạng thái (ví dụ: Thất bại)")
    errorMessage: str = Field(..., description="Chi tiết lỗi")
    timestamp: Optional[str] = Field(None, description="Thời gian xảy ra lỗi")

# --- Telegram Service ---
class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

    def send_alert(self, data: QLVBErrorPayload):
        if not self.token or not self.chat_id:
            logger.error("Telegram configuration missing in .env")
            return False

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        
        # Formatting the message based on our previous agreement
        now = datetime.now().strftime("%H:%M:%S")
        message = (
            f"⚠️ <b>CẢNH BÁO LỖI HỆ THỐNG QLVB</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🏢 <b>Đơn vị:</b> {data.unitName} ({data.unitCode or 'N/A'})\n"
            f"📄 <b>Văn bản:</b> {data.docId} - {data.docName}\n"
            f"⚙️ <b>Chức năng:</b> <code>{data.function}</code>\n"
            f"❌ <b>Lỗi:</b> {data.status} - {data.errorMessage}\n"
            f"⏰ <b>Thời gian:</b> {data.timestamp or now}"
        )
        
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {e}")
            return False

notifier = TelegramNotifier()

# --- Endpoints ---

@app.get("/")
async def root():
    return {"status": "online", "message": "QLVB Notification Gateway is running"}

@app.post("/webhook/error")
async def receive_error(payload: QLVBErrorPayload):
    """
    Endpoint for QLVB to push error notifications.
    """
    logger.info(f"Received error from {payload.unitName} for doc {payload.docId}")
    
    # Send to Telegram
    success = notifier.send_alert(payload)
    
    if success:
        return {"status": "success", "message": "Notification pushed to Telegram"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send Telegram notification")

@app.post("/test/notify")
async def test_notify():
    """
    Test endpoint to verify Telegram notification without needing QLVB.
    """
    test_data = QLVBErrorPayload(
        unitName="Sở Xây Dựng (Test)",
        unitCode="SXD-TEST",
        docId="TEST-123",
        docName="Văn bản test hệ thống",
        function="sendDoc",
        status="Thất bại",
        errorMessage="Lỗi giả lập để test thông báo",
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    success = notifier.send_alert(test_data)
    if success:
        return {"status": "success", "message": "Test notification sent!"}
    return {"status": "error", "message": "Test notification failed"}

if __name__ == "__main__":
    import uvicorn
    # Run the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
