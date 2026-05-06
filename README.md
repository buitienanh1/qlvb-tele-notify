# Dự án: Thông báo lỗi trên Telegram thông qua API QLVB

## 🎯 Mục tiêu
Xây dựng hệ thống tự động theo dõi lỗi hoặc trạng thái từ API của phần mềm Quản lý văn bản (QLVB) và gửi thông báo tức thời đến Telegram.

## 📁 Cấu trúc thư mục
- `src/`: Chứa mã nguồn chính của ứng dụng.
- `config/`: Chứa các file cấu hình.
- `logs/`: Lưu trữ nhật ký hoạt động.
- `.env`: Lưu trữ thông tin bảo mật (Token API, Chat ID).

## 🚀 Luồng hoạt động (Dự kiến)
1. Gọi API QLVB để kiểm tra trạng thái/lỗi.
2. Phân tích dữ liệu trả về.
3. Nếu phát hiện lỗi, định dạng nội dung thông báo.
4. Gửi thông báo đến Telegram thông qua Telegram Bot API.
