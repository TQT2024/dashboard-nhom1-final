import streamlit as st
import pandas as pd
import os
from modules.db import load_individual_data
from modules.charts2 import draw_radar_chart
import google.generativeai as genai

def render_tab_individual():
    # 1. Triệu hồi dữ liệu thuộc tính cá nhân từ cơ sở dữ liệu hồ sơ
    try:
        df_profile_all = load_individual_data()
    except Exception as e:
        st.error(f"Lỗi tải thông tin định danh sinh viên: {e}")
        return

    # Lấy tập dữ liệu vĩ mô hiện tại từ Sidebar để ép danh sách sinh viên co giãn theo
    if 'filtered_df' not in st.session_state:
        return
    df_filtered_macro = st.session_state['filtered_df']
    
    # Thực hiện lọc thác nước: Chỉ lấy những sinh viên có ID nằm trong danh sách bộ lọc vĩ mô
    allowed_ids = df_filtered_macro['student_id'].astype(str).tolist()
    df_profile_allowed = df_profile_all[df_profile_all['student_id'].astype(str).isin(allowed_ids)]

    st.markdown("##### 👤 Tra cứu và phân tích hồ sơ chi tiết sinh viên")

    if df_profile_allowed.empty:
        st.warning("⚠️ Không có sinh viên nào thỏa mãn tiêu chí bộ lọc diện rộng đã chọn ở Sidebar.")
        return

    # 2. Xây dựng thanh chọn sinh viên phụ thuộc hạ nguồn (Cascading)
    student_options = df_profile_allowed.apply(
        lambda r: f"{r['student_id']} - {r.get('full_name', 'Ẩn danh hóa')}", axis=1
    ).tolist()
    
    selected_option = st.selectbox(
        "Lựa chọn Mã số sinh viên cần kết xuất hồ sơ học thuật:", 
        options=student_options, 
        key="sb_individual_engine"
    )
    
    # Tách chuỗi lấy mã định danh nguyên bản dạng String an toàn
    selected_id = selected_option.split(" - ")[0]
    
    # Trích xuất bản ghi thông tin của sinh viên duy nhất được chọn
    student_data = df_profile_allowed[df_profile_allowed['student_id'].astype(str) == selected_id].iloc[0]

    # 3. Phân bổ bố cục giao diện trực quan
    col_info, col_chart = st.columns([2, 3])

    with col_info:
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#e76f51; margin-bottom:10px;'>📋 Lý lịch hành chính</p>", unsafe_allow_html=True)
        st.write(f"**Mã định danh (ID):** {student_data['student_id']}")
        st.write(f"**Họ và tên:** {student_data.get('full_name', 'Nguyễn Văn A (Faker)')}")
        st.write(f"**Giới tính:** {student_data.get('gender_label', 'Chưa phân loại')}")
        st.write(f"**Giai đoạn đào tạo:** {student_data.get('year_label', 'Chưa rõ')}")
        st.write(f"**Diện chính sách:** {student_data.get('policy_label', 'Không')}")
        
        st.markdown("---")
        st.markdown("<p style='font-size:16px; font-weight:bold; color:#2a9d8f; margin-bottom:10px;'>🎯 Chỉ số năng lực quy đổi (Thang điểm 100)</p>", unsafe_allow_html=True)
        st.write(f"• **Điểm kết quả GPA:** {student_data['gpa_scaled']:.1f} pts")
        st.write(f"• **Năng lực Tự lực học tập:** {student_data['index_tu_luc_scaled']:.1f} pts")
        st.write(f"• **Đánh giá Môi trường trường học:** {student_data['index_moi_truong_truong_scaled']:.1f} pts")
        st.write(f"• **Áp lực & Động lực bạn bè:** {student_data['index_moi_truong_ban_be_scaled']:.1f} pts")

    with col_chart:
        st.markdown("<p style='font-size:18px; font-weight:bold; color:#2a9d8f; text-align:center; margin-bottom:10px;'>🕸️ Biểu đồ tương quan năng lực toàn diện</p>", unsafe_allow_html=True)
        fig_radar = draw_radar_chart(student_data, df_profile_all)
        st.plotly_chart(fig_radar, use_container_width=True)

    # 4. Tích hợp Trợ lý Trí tuệ nhân tạo Gemini API 2026 [INDEX, 13]
    st.markdown("---")
    st.markdown("<p style='font-size:18px; font-weight:bold; color:#2a9d8f;'>🤖 Trợ lý AI Gemini - Tư vấn & Định hướng Học thuật cá nhân</p>", unsafe_allow_html=True)
    
    if st.button("✨ Khởi tạo phân tích định hướng chuyên sâu từ Gemini AI"):
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            st.warning("⚠️ Chưa cấu hình mã bảo mật `GEMINI_API_KEY` trong Secrets.")
            st.info(f"💡 **Phân tích nhanh:** Sinh viên sở hữu điểm Tự lực đạt {student_data['index_tu_luc_scaled']:.1f}/100. Hãy duy trì tốt cường độ tự học hiện tại để bứt phá kết quả GPA.")
        else:
            with st.spinner("Gemini đang phân tích dữ liệu..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    
                    prompt = f"""
                    Bạn là một cố vấn học tập cao cấp giàu kinh nghiệm. Hãy phân tích hồ sơ sinh viên sau dựa trên dữ liệu khảo sát thực tế:
                    - Điểm GPA chuẩn hóa: {student_data['gpa_scaled']}/100
                    - Chỉ số năng lực Tự lực: {student_data['index_tu_luc_scaled']}/100
                    - Đánh giá môi trường nhà trường: {student_data['index_moi_truong_truong_scaled']}/100
                    - Áp lực và động lực từ bạn bè: {student_data['index_moi_truong_ban_be_scaled']}/100
                    
                    Yêu cầu cấu trúc phản hồi ngắn gọn dưới 150 từ, ngôn ngữ chuyên nghiệp:
                    1. Đánh giá ngắn gọn điểm mạnh, điểm yếu nổi bật nhất dựa trên độ chênh lệch chỉ số.
                    2. Đưa ra 2 hành động cụ thể giúp sinh viên tối ưu hóa lộ trình học tập hoặc phát triển sau tốt nghiệp.
                    """
                    response = model.generate_content(prompt)
                    st.success("Nhận xét học thuật chuyên sâu từ AI:")
                    st.markdown(response.text)
                except Exception as ex:
                    st.error(f"Lỗi cổng kết nối Gemini API: {ex}")
