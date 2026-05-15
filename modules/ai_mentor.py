import streamlit as st
from google import genai
from google.genai import types

def generate_advice(student_info):
    """
    Module xử lý logic AI độc lập (Backend).
    Tách biệt hoàn toàn khỏi tầng giao diện (Frontend) để đảm bảo hiệu suất.
    """
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            return "**Lỗi hệ thống:** Chưa cấu hình GEMINI_API_KEY trong secrets."
            
        client = genai.Client(api_key=api_key)
        
        system_instruction = (
            "Bạn là chuyên gia phân tích dữ liệu giáo dục đại học. "
            "Đánh giá năng lực sinh viên dựa trên 4 chỉ số chuẩn hóa (thang 100). "
            "Trả lời ngắn gọn, trực diện bằng định dạng Markdown. Bắt buộc trình bày theo 3 ý chính: "
            "- **Điểm mạnh nổi bật:** [Phân tích 1 câu]\n"
            "- **Hạn chế cốt lõi:** [Phân tích 1 câu]\n"
            "- **Giải pháp hành động:** [Đề xuất 1 câu]"
        )
        
        user_prompt = (
            f"Mã sinh viên: {student_info['student_id']}\n"
            f"GPA: {student_info['gpa_scaled']:.1f}/100\n"
            f"Tự lực: {student_info['index_tu_luc_scaled']:.1f}/100\n"
            f"Hỗ trợ từ trường: {student_info['index_moi_truong_truong_scaled']:.1f}/100\n"
            f"Môi trường bạn bè: {student_info['index_moi_truong_ban_be_scaled']:.1f}/100"
        )

        advice_config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            max_output_tokens=1024, 
            temperature=0.2 
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=advice_config 
        )
        
        return response.text.strip()
        
    except Exception as e:
        return _fallback_advice(student_info['gpa_scaled'], student_info['index_tu_luc_scaled'], str(e))

def _fallback_advice(gpa_scaled, tu_luc_scaled, error_msg):
    """Hệ thống dự phòng dựa trên luật tĩnh (Rule-based Fallback)"""
    gpa = float(gpa_scaled)
    tu_luc = float(tu_luc_scaled)
    
    if gpa < 50 and tu_luc < 50:
        return f"**CẢNH BÁO (Dự phòng):** API gián đoạn ({error_msg}). Chỉ số GPA ({gpa:.1f}) và Tự lực ({tu_luc:.1f}) đều ở mức thấp. Yêu cầu sinh viên rà soát lại phương pháp học tập."
    else:
        return f"**THÔNG TIN (Dự phòng):** API gián đoạn ({error_msg}). Năng lực học tập duy trì ở mức ổn định với GPA {gpa:.1f}. Tiếp tục phát huy phương pháp tự học hiện tại."
