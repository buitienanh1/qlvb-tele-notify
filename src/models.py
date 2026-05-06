from pydantic import BaseModel, Field
from typing import Optional

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
