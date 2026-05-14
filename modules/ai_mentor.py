import streamlit as st
from google import genai
from google.genai import types

def generate_advice(student_info):
    """
    Hàm gọi Gemini API tạo lời khuyên học thuật cá nhân hóa dựa trên dữ liệu.
    Tích hợp cơ chế Fallback (Dự phòng ngầm) bằng hàm Rule-based nếu lỗi hệ thống.
    """
    try:
        # Lấy API Key an toàn từ secrets.toml hoặc cấu hình nâng cao trên Cloud
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)
        
        # Thiết lập System Instruction nghiêm ngặt chống AI ảo tưởng
        system_instruction = (
            "Bạn là hệ thống cố vấn học tập đại học chuyên nghiệp dựa trên dữ liệu. "
            "Chỉ sử dụng 4 chỉ số (Thang 100) sau đây để nhận xét. Tuyệt đối không tự suy diễn thông tin nằm ngoài số liệu. "
            "Không trả về định dạng Markdown phức tạp làm vỡ giao diện. Trả lời tối đa 4 dòng, văn phong học thuật, trực diện. "
            "Cấu trúc bắt buộc: 1 câu tổng quan, 1 câu điểm mạnh, 1 câu điểm yếu, 1 câu đề xuất hành động thực tế giai đoạn nước rút."
        )
        
        # Định dạng chuỗi Prompt chứa dữ liệu đa biến của sinh viên
        user_prompt = (
            f"Mã sinh viên: {student_info['student_id']}\n"
            f"- Năng lực tự lực (X): {student_info['index_tu_luc_scaled']:.1f}/100\n"
            f"- Hỗ trợ từ trường (Y): {student_info['index_moi_truong_truong_scaled']:.1f}/100\n"
            f"- Môi trường bạn bè (Z): {student_info['index_moi_truong_ban_be_scaled']:.1f}/100\n"
            f"- GPA quy đổi (W): {student_info['gpa_scaled']:.1f}/100\n\n"
            "Hãy phân tích và đưa ra lời khuyên theo đúng cấu trúc yêu cầu."
        )

        # Gọi mô hình với bộ nhớ đệm mở rộng (800 Tokens) cho tiếng Việt Unicode
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                max_output_tokens=800
            )
        )
        return response.text
        
    except Exception:
        # Kích hoạt tầng dự phòng (Fallback) nếu mất kết nối internet hoặc hết quota API
        return _fallback_advice(student_info['gpa_scaled'])

def _fallback_advice(gpa_scaled):
    """Hệ chuyên gia luật tĩnh (Rule-based Fallback) bảo vệ hệ thống không bị sập trang lúc demo"""
    if gpa_scaled >= 80:
        return "Kết quả xuất sắc. Duy trì năng lực tự học hiện tại; cân nhắc tham gia các đề tài nghiên cứu khoa học chuyên sâu."
    elif gpa_scaled >= 60:
        return "Học lực khá. Có tiềm năng nhưng cần quản lý thời gian tự học tốt hơn để bứt phá lên nhóm giỏi."
    else:
        return "CẢNH BÁO: Kết quả học tập đáng báo động. Yêu cầu sinh viên rà soát lại phương pháp học tập và chủ động tìm kiếm sự hỗ trợ từ Cố vấn học tập."
