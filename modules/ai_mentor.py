import streamlit as st
from google import genai
from google.genai import types

def generate_advice(student_info):
    """
    Hàm gọi Gemini API tạo lời khuyên học thuật cá nhân hóa dựa trên dữ liệu.
    Đã sửa lỗi bỏ qua cấu hình cấu trúc token và giăng bẫy prompt nghiêm ngặt.
    """
    try:
        # Lấy API Key an toàn từ secrets.toml
        api_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=api_key)
        
        # Thêm câu lệnh ép buộc AI kết thúc bằng dấu chấm câu đầy đủ, không bỏ lửng
        system_instruction = (
            "Bạn là hệ thống cố vấn học tập đại học chuyên nghiệp dựa trên dữ liệu. "
            "Chỉ sử dụng 4 chỉ số (Thang 100) sau đây để nhận xét. Tuyệt đối không tự suy diễn thông tin nằm ngoài số liệu. "
            "Không trả về định dạng Markdown phức tạp làm vỡ giao diện. Trả lời tối đa 4 dòng, văn phong học thuật, trực diện. "
            "Cấu trúc bắt buộc: 1 câu tổng quan, 1 câu điểm mạnh, 1 câu điểm yếu, 1 câu đề xuất hành động thực tế giai đoạn nước rút. "
            "QUY TẮC TỐI THƯỢNG: Phải viết các câu ngắn gọn và bắt buộc kết thúc bằng một dấu chấm câu hoàn chỉnh. Không được viết dông dài, không để chữ bị cắt cụt."
        )
        
        user_prompt = (
            f"Mã sinh viên: {student_info['student_id']}\n"
            f"- Năng lực tự lực (X): {student_info['index_tu_luc_scaled']:.1f}/100\n"
            f"- Hỗ trợ từ trường (Y): {student_info['index_moi_truong_truong_scaled']:.1f}/100\n"
            f"- Môi trường bạn bè (Z): {student_info['index_moi_truong_ban_be_scaled']:.1f}/100\n"
            f"- GPA quy đổi (W): {student_info['gpa_scaled']:.1f}/100\n\n"
            "Hãy phân tích và đưa ra lời khuyên theo đúng cấu trúc yêu cầu."
        )

        # ĐỒNG BỘ CẤU TRÚC GỌI CONFIG CHUẨN XÁC CỦA NĂM 2026
        # Khởi tạo đối tượng config riêng biệt để đảm bảo mô hình nạp thành công vào bộ nhớ
        advice_config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            max_output_tokens=1024, # Nâng hẳn lên 1024 để đảm bảo không gian biên dịch Unicode tiếng Việt
            temperature=0.2 # Hạ thấp độ sáng tạo để AI tập trung viết ngắn, trực diện, không nói lan man
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=advice_config # Nạp cấu hình đã định nghĩa
        )
        
        # Xử lý hậu kỳ chuỗi văn bản nhận được để đảm bảo tính thẩm mỹ UI
        result_text = response.text.strip()
        return result_text
        
    except Exception:
        # Kích hoạt tầng dự phòng (Fallback) nếu mất kết nối hoặc lỗi API
        return _fallback_advice(student_info['gpa_scaled'])

def _fallback_advice(gpa_scaled):
    if gpa_scaled >= 80:
        return "Kết quả xuất sắc. Duy trì năng lực tự học hiện tại; cân nhắc tham gia các đề tài nghiên cứu khoa học chuyên sâu."
    elif gpa_scaled >= 60:
        return "Học lực khá. Có tiềm năng nhưng cần quản lý thời gian tự học tốt hơn để bứt phá lên nhóm giỏi."
    else:
        return "CẢNH BÁO: Kết quả học tập đáng báo động. Yêu cầu sinh viên rà soát lại phương pháp học tập và chủ động tìm kiếm sự hỗ trợ từ Cố vấn học tập."
