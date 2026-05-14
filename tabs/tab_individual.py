import streamlit as st
import plotly.express as px
import pandas as pd
from modules.database import load_individual_data
from modules.ai_mentor import generate_advice

def render_tab_individual():
    df = load_individual_data()
    if df.empty:
        st.warning("Hệ thống chưa tải được dữ liệu hồ sơ cá nhân.")
        return

    st.markdown("### Tra cứu Hồ sơ Cá nhân & Khuyến nghị")

    # Bộ lọc sinh viên
    student_list = df['student_id'].tolist()
    selected_id = st.selectbox("Lựa chọn Mã Sinh viên (Student ID):", student_list)

    # Trích xuất dữ liệu dòng của sinh viên được chọn
    student_data = df[df['student_id'] == selected_id].iloc[0]

    # Hiển thị tóm tắt định danh
    st.info(
        f"**Họ và tên:** {student_data['full_name']} | "
        f"**Email:** {student_data['email']} | "
        f"**Giới tính:** {student_data['gender_label']} | "
        f"**Năm học:** {student_data['year_label']}"
    )

    col_chart, col_ai = st.columns([1.2, 1])

    with col_chart:
        st.markdown("**Biểu đồ Năng lực (Đối chiếu Trung bình Khóa)**")
        
        # Lấy giá trị trung bình toàn khóa cho 4 chỉ số cốt lõi
        mean_data = df[['index_tu_luc_scaled', 'index_moi_truong_truong_scaled', 'index_moi_truong_ban_be_scaled', 'gpa_scaled']].mean()
        
        # Chuyển đổi dữ liệu sang định dạng Dọc (Melted Data) cho biểu đồ Radar
        categories = ['Tự lực', 'Hỗ trợ (Trường)', 'Môi trường (Bạn bè)', 'GPA']
        
        radar_df = pd.DataFrame({
            'Chỉ_số': categories * 2,
            'Điểm': [
                student_data['index_tu_luc_scaled'], student_data['index_moi_truong_truong_scaled'], 
                student_data['index_moi_truong_ban_be_scaled'], student_data['gpa_scaled'],
                mean_data['index_tu_luc_scaled'], mean_data['index_moi_truong_truong_scaled'], 
                mean_data['index_moi_truong_ban_be_scaled'], mean_data['gpa_scaled']
            ],
            'Đối_tượng': ['Cá nhân'] * 4 + ['Trung bình khóa'] * 4
        })

        fig_radar = px.line_polar(
            radar_df, 
            r='Điểm', 
            theta='Chỉ_số', 
            color='Đối_tượng', 
            line_close=True,
            range_r=[0, 100],
            color_discrete_map={'Cá nhân': '#1f77b4', 'Trung bình khóa': '#7f7f7f'}
        )
        
        # Hiệu chỉnh nét đứt cho đường trung bình khóa để dễ phân biệt
        fig_radar.update_traces(patch={"line": {"dash": "dot"}}, selector={"name": "Trung bình khóa"})
        fig_radar.update_layout(margin=dict(l=40, r=40, t=20, b=20), legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_ai:
        st.markdown("**AI Mentor (Hệ thống Cố vấn)**")
        
        # Thiết lập cơ sở bộ nhớ đệm cho Session
        if 'current_student' not in st.session_state:
            st.session_state['current_student'] = None
            st.session_state['ai_advice'] = ""

        # Logic: Chỉ gọi API nếu ID được chọn khác với ID đã lưu trong session
        if st.session_state['current_student'] != selected_id:
            with st.spinner("Hệ thống đang tổng hợp dữ liệu và phân tích..."):
                advice = generate_advice(student_data.to_dict())
                st.session_state['ai_advice'] = advice
                st.session_state['current_student'] = selected_id

        # Hiển thị cảnh báo hoặc khuyến nghị bằng st.warning hoặc st.success
        st.success(st.session_state['ai_advice'])