# DerivAI
DerivAI: Learning Derivatives with AI Assistance
=======
# Study Support Chatbot (DerivAI)

Một ứng dụng Chatbot hỗ trợ học tập sử dụng Gemini API, FastAPI (Backend) và Streamlit (Frontend).

## Cấu trúc dự án
- `backend/`: Mã nguồn server (FastAPI).
- `frontend/`: Mã nguồn giao diện (Streamlit).
- `requirements.txt`: Các thư viện cần thiết.
## Yêu cầu
- Python 3.9 trở lên.
- Google Gemini API Key.

## Cài đặt

1.  **Cài đặt thư viện:**
    Mở terminal tại thư mục gốc của dự án và chạy:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Cấu hình API Key:**
    - Vào thư mục `backend`.
    - Tạo hoặc mở file `.env`.
    - Thêm dòng: `GEMINI_API_KEY=your_actual_api_key_here`

## Cách chạy ứng dụng

### 1. Chạy Backend
Mở terminal tại thư mục gốc và chạy:
```bash
cd backend
uvicorn main:app --reload
```
Server sẽ chạy tại: `http://localhost:8000`

### 2. Chạy Frontend
Mở một terminal **mới** tại thư mục gốc và chạy:
```bash
streamlit run frontend/app.py
```
Ứng dụng sẽ mở tại: `http://localhost:8501`

## Tính năng
- Chat hỏi đáp thông thường.
- Hỗ trợ gửi ảnh bài tập.
- Hệ thống "Giàn giáo" (Scaffolding) hỗ trợ giải bài từng bước.
