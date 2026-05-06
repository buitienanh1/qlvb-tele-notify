import os
import requests
import logging
from typing import List, Dict, Any
from .models import QLVBErrorPayload

logger = logging.getLogger(__name__)

class QLVBClient:
    def __init__(self):
        self.base_url = os.getenv('QLVB_API_URL', 'https://api.qlvb.gov.vn/api')
        self.api_key = os.getenv('QLVB_API_KEY', '')

    def call_api(self, endpoint: str, params: Dict[str, Any] = None):
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        
        try:
            if params:
                response = requests.post(url, json=params, headers=headers, timeout=10)
            else:
                response = requests.get(url, headers=headers, timeout=10)
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API call to {endpoint} failed: {e}")
            return None

    def get_latest_errors(self, function_name: str) -> List[Dict[str, Any]]:
        """
        Fetches the latest logs for a specific function to check for errors.
        """
        # This is where the actual API call to QLVB would go
        # For now, we keep the mock logic for testing
        return [
            {
                "unitName": "Phòng Tổ chức - Cán bộ",
                "unitCode": "H29.0.162",
                "docId": "VB-2026-001",
                "docName": "Tờ trình xin phê duyệt kinh phí đào tạo",
                "function": function_name,
                "status": "Thất bại",
                "errorMessage": "Lỗi kết nối Socket: Timeout (60s)",
                "timestamp": "2026-05-06 13:00:00"
            }
        ]
