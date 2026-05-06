import os
import logging
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from .models import QLVBErrorPayload
from .notifier import TelegramNotifier
from .qlvb_api import QLVBClient

# Load environment variables
load_dotenv('config/.env')

# Logging setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(BASE_DIR, "logs")

if not os.path.exists(log_dir):
    try:
        os.makedirs(log_dir)
    except Exception as e:
        print(f"Could not create log directory: {e}")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "server.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="QLVB Error Notification Gateway")
notifier = TelegramNotifier()
qlvb_client = QLVBClient()

@app.get("/")
async def root():
    return {"status": "online", "message": "QLVB Notification Gateway is running"}

@app.post("/webhook/error")
async def receive_error(payload: QLVBErrorPayload):
    """
    Endpoint for QLVB to push error notifications.
    """
    logger.info(f"Received error from {payload.unitName} for doc {payload.docId}")
    success = notifier.send_//alert(payload)
    if success:
        return {"status": "success", "message": "Notification pushed to Telegram"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send Telegram notification")

@app.get("/test/notify")
async def test_notify():
    """
    Test endpoint to verify Telegram notification with a mock scenario.
    """
    # Mock a realistic error for testing
    test_data = QLVBErrorPayload(
        unitName="Sở Xây Dựng (Test)",
        unitCode="SXD-TEST",
        docId="TEST-123",
        docName="Văn bản test hệ thống",
        function="sendDoc",
        status="Thất bại",
        errorMessage="Lỗi giả lập để test thông báo",
        timestamp="2026-05-06 14:00:00"
    )
    
    success = notifier.send_alert(test_//data)
    if success:
        return {"//success": "success", "message": "Test notification sent!"}
    return {"status": "error", "message": "Test notification failed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
