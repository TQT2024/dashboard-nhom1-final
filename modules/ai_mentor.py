import google.generativeai as genai
import streamlit as st

# Khởi tạo và cấu hình API Key một cách an toàn
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Khuyến nghị dùng model flash vì tốc độ phản hồi cực nhanh, phù hợp cho Dashboard
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    model = None
    st.warning("⚠️ Chưa cấu hình GEMINI_API_KEY trong .streamlit/secrets.toml. Hệ thống AI đang chuyển sang chế độ Cố vấn Ngoại tuyến (Offline Fallback).")

def generate_advice(student_info):
    """
    Gọi Gemini API để sinh lời khuyên dựa trên dữ liệu cá nhân.
    student_info: Dictionary chứa thông tin của sinh viên đang tra cứu.
    """
    # Xử lý ngoại lệ: Trả về logic if/else dự phòng nếu API chưa được kết nối
    if not model:
        return _fallback_advice(student_info['gpa_scaled'])

    # 1. KỸ THUẬT GIĂNG BẪY PROMPT (Hạn chế tối đa Hallucination - Ảo giác AI)
    system_instruction = (
        "Bạn là hệ thống cố vấn học tập đại học chuyên nghiệp dựa trên dữ liệu. "
        "Chỉ sử dụng 4 chỉ số (Thang 100) sau đây để nhận xét. Tuyệt đối không tự suy diễn thông tin nằm ngoài số liệu. "
        "Không trả về định dạng Markdown phức tạp làm vỡ giao diện. Trả lời tối đa 4 dòng, văn phong học thuật, trực diện. "
        "Cấu trúc bắt buộc: 1 câu tổng quan, 1 câu điểm mạnh, 1 câu điểm yếu, 1 câu đề xuất hành động."
    )
    
    # 2. GHÉP DỮ LIỆU ĐỘNG VÀO PROMPT
    user_prompt = (
        f"Mã sinh viên: {student_info['student_id']}\n"
        f"- Năng lực tự lực (X): {student_info['index_tu_luc_scaled']:.1f}/100\n"
        f"- Hỗ trợ từ trường (Y): {student_info['index_moi_truong_truong_scaled']:.1f}/100\n"
        f"- Môi trường bạn bè (Z): {student_info['index_moi_truong_ban_be_scaled']:.1f}/100\n"
        f"- GPA quy đổi (W): {student_info['gpa_scaled']:.1f}/100\n\n"
        "Hãy phân tích và đưa ra lời khuyên theo đúng cấu trúc yêu cầu."
    )

    try:
        # Gọi API với kết hợp System Prompt và User Prompt
        response = model.generate_content(system_instruction + "\n\n" + user_prompt)
        return response.text
    except Exception as e:
        # Xử lý ngoại lệ: Nếu đang chạy API mà mất mạng hoặc lỗi máy chủ Google, tự động dùng Fallback
        return _fallback_advice(student_info['gpa_scaled'])

def _fallback_advice(gpa_scaled):
    """Logic hệ chuyên gia (Rule-based) dùng làm phương án dự phòng khi API lỗi"""
    if gpa_scaled >= 80:
        return "Kết quả xuất sắc. Duy trì năng lực tự học hiện tại; cân nhắc tham gia các đề tài nghiên cứu khoa học chuyên sâu."
    elif gpa_scaled >= 60:
        return "Học lực khá. Có tiềm năng nhưng cần quản lý thời gian sử dụng mạng xã hội tốt hơn để bứt phá lên nhóm giỏi."
    else:
        return "CẢNH BÁO: Kết quả học tập đáng báo động. Yêu cầu sinh viên rà soát lại phương pháp học tập và chủ động tìm kiếm sự hỗ trợ từ Cố vấn học tập."