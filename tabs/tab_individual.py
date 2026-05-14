import streamlit as st
import pandas as pd
from modules.db import load_individual_data
from modules.charts2 import draw_radar_chart
import google.generativeai as genai

def render_tab_individual():
    try:
        df_profile = load_individual_data()
    except Exception as e:
        st.error(f"Không thể kết nối cơ sở dữ liệu hồ sơ: {e}")
        return

    # SỬA LỖI: Gom bộ lọc tra cứu cá nhân vào vùng nội dung chính của Tab 2 để không ảnh hưởng Tab 1
    st.markdown("##### 👤 Tra cứu thông tin chi tiết sinh viên")
    
    # Tạo danh sách lựa chọn hiển thị trực quan
    student_options = df_profile.apply(lambda r: f"{r['student_id']} - {r.get('full_name', 'Sinh viên ẩn danh')}", axis=1).tolist()
    
    # Sử dụng key duy nhất để tránh xung đột trạng thái giữa các Tab
    selected_option = st.selectbox("Nhập hoặc chọn Sinh viên cần phân tích:", student_options, key="sb_individual_select")
    
    # SỬA LỖI: Trích xuất ID an toàn không gây lỗi ValueError sập giao diện
    selected_id_raw = selected_option.split(" - ")[0]
    
    # Khớp dữ liệu linh hoạt (hỗ trợ cả ID dạng chuỗi 'SV0001' hoặc dạng số)
    student_filtered = df_profile[df_profile['student_id'].astype(str) == str(selected_id_raw)]
    
    if student_filtered.empty:
        st.warning("Không tìm thấy dữ liệu của sinh viên được chọn.")
        return
        
    student_data = student_filtered.iloc[0]

    # Bố cục lưới hiển thị thông tin thành phần
    col_info, col_chart = st.columns([2, 3])

    with col_info:
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#e76f51;'>📋 Hồ sơ lý lịch hành chính</p>", unsafe_allow_html=True)
        st.write(f"**Mã định danh (ID):** {student_data['student_id']}")
        st.write(f"**Họ và tên:** {student_data.get('full_name', 'Chưa cập nhật')}")
        st.write(f"**Giới tính:** {student_data.get('gender_label', 'N/A')}")
        st.write(f"**Giai đoạn học tập:** {student_data.get('year_label', 'N/A')}")
        
        st.markdown("---")
        st.markdown("<p style='font-size:16px; font-weight:bold; color:#2a9d8f;'>🎯 Điểm số năng lực chuẩn hóa (Thang 100)</p>", unsafe_allow_html=True)
        st.write(f"• **Kết quả tích lũy GPA:** {student_data['gpa_scaled']:.1f} / 100")
        st.write(f"• **Chỉ số năng lực Tự lực:** {student_data['index_tu_luc_scaled']:.1f} / 100")
        st.write(f"• **Mức độ hỗ trợ từ Nhà trường:** {student_data['index_moi_truong_truong_scaled']:.1f} / 100")
        st.write(f"• **Áp lực/Động lực từ Bạn bè:** {student_data['index_moi_truong_ban_be_scaled']:.1f} / 100")

    with col_chart:
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#2a9d8f; text-align:center;'>🕸️ Biểu đồ Radar tương quan năng lực toàn diện</p>", unsafe_allow_html=True)
        fig_radar = draw_radar_chart(student_data, df_profile)
        st.plotly_chart(fig_radar, use_container_width=True)

    # Đoạn mã tích hợp Gemini API giữ nguyên phía dưới...
