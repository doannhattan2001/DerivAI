import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=API_KEY)
# System prompt for the study assistant
SYSTEM_PROMPT = """
Bạn hãy đóng vai người hỗ trợ học tập toán học theo lý thuyết giàn giáo (scaffolding) của Vygotsky. 
Tôi sẽ đưa cho bạn một bài toán về đạo hàm. 
Nhiệm vụ của bạn là cung cấp gợi ý theo 3 tầng giàn giáo: 
Tầng 1 (gợi ý nhẹ): Nhắc lại khái niệm, công thức chi tiết.
Tầng 2 (gợi ý trung bình): Hướng dẫn từng bước giải cụ thể hơn, nhưng chưa cho lời giải hoàn chỉnh. 
Tầng 3 (gợi ý mạnh): Trình bày lời giải chi tiết, kèm theo giải thích. Bạn hãy hỏi học sinh có cần giúp đỡ không và đưa ra gợi ý lần lượt từng tầng 1 nếu học sinh nói cần sự giúp đỡ thêm.
"""

model = genai.GenerativeModel(
    'gemini-2.5-flash',
    system_instruction=SYSTEM_PROMPT
)

app = FastAPI(title="Study Support Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for development, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Study Support Chatbot API is running"}

# Store chat sessions in memory
chat_sessions = {}

@app.post("/chat")
async def chat(
    text: str = Form(...), 
    file: UploadFile = File(None),
    session_id: str = Form(...)
):
    """
    Chat endpoint receiving text, optional image, and session_id for context.
    """
    try:
        # Get or create chat session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = model.start_chat(history=[])
        
        chat_session = chat_sessions[session_id]

        prompt_parts = [text]
        
        if file:
            # Read image file
            content = await file.read()
            image = Image.open(io.BytesIO(content))
            prompt_parts.append(image)
            
        # Send message to the session (preserves history)
        response = chat_session.send_message(prompt_parts)
        
        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
