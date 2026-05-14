import streamlit as st
import pandas as pd
from modules.database import load_individual_data
from modules.ai_mentor import generate_advice
from modules.charts2 import draw_radar_chart

def render_tab_individual():
    df = load_individual_data()
    if df.empty:
        st.warning("Hệ thống chưa tải được dữ liệu hồ sơ cá nhân. Vui lòng kiểm tra lại SQL View.")
        return

    # Chỉ hiển thị bộ lọc trong Sidebar KHI VÀ CHỈ KHI người dùng đang đứng ở Tab 2
    if st.session_state.get('active_tab') == "Hồ sơ cá nhân sinh viên":
        st.sidebar.markdown("### 🛠️ Bộ lọc tra cứu cá nhân")
        
        # 1. Bộ lọc Năm học trong Sidebar
        year_options = ["Tất cả"] + list(df['year_label'].unique())
        selected_year = st.sidebar.selectbox("1. Hẹp theo Năm học:", options=year_options, index=0)
        
        # 2. Bộ lọc Giới tính trong Sidebar
        gender_options = ["Tất cả"] + list(df['gender_label'].unique())
        selected_gender = st.sidebar.selectbox("2. Hẹp theo Giới tính:", options=gender_options, index=0)

        # Lọc dữ liệu ngầm để thu hẹp tập ID
        df_filtered = df.copy()
        if selected_year != "Tất cả":
            df_filtered = df_filtered[df_filtered['year_label'] == selected_year]
        if selected_gender != "Tất cả":
            df_filtered = df_filtered[df_filtered['gender_label'] == selected_gender]

        # 3. Hộp chọn Mã sinh viên trong Sidebar
        student_list = df_filtered['student_id'].tolist()
        if not student_list:
            st.sidebar.error("Không có sinh viên phù hợp.")
            return
        selected_id = st.sidebar.selectbox("3. Lựa chọn Mã Sinh viên (Student ID):", options=student_list, index=0)
    else:
        # Nếu vô tình đứng ở Tab khác, không hiển thị gì trong Sidebar
        return

    # Trích xuất dữ liệu dòng của sinh viên được chọn
    student_data = df_filtered[df_filtered['student_id'] == selected_id].iloc

    # Thẻ hiển thị định danh cá nhân nằm ngay đầu trang
    st.info(
        f"👤 **Họ và tên:** {student_data['full_name']} | "
        f"📧 **Email:** {student_data['email']} | "
        f"🧬 **Giới tính:** {student_data['gender_label']} | "
        f"📅 **Năm học:** {student_data['year_label']}"
    )

    st.write("") 
    col_chart, col_ai = st.columns([1.1, 1])

    with col_chart:
        st.markdown("<p style='font-size:12px; font-weight: bold; margin-bottom:2px; color:#444;'>So sánh các chỉ số cá nhân với mức Trung bình khóa</p>", unsafe_allow_html=True)
        # Vẽ đa giác Radar khổng lồ phóng khoáng, khóa chặt Modebar xám
        st.plotly_chart(draw_radar_chart(student_data, df), width='stretch', config={'displayModeBar': False})

    with col_ai:
        st.markdown("<p style='font-size:12px; font-weight: bold; margin-bottom:2px; color:#444;'>Nhận xét và Đề xuất</p>", unsafe_allow_html=True)
        
        if 'ai_mentor_cache' not in st.session_state:
            st.session_state['ai_mentor_cache'] = {}
            st.session_state['current_student'] = None

        if st.session_state['current_student'] != selected_id:
            with st.spinner("Hệ thống đang phân tích dữ liệu..."):
                safe_student_info = {
                    'student_id': str(student_data['student_id']),
                    'index_tu_luc_scaled': float(student_data['index_tu_luc_scaled']),
                    'index_moi_truong_truong_scaled': float(student_data['index_moi_truong_truong_scaled']),
                    'index_moi_truong_ban_be_scaled': float(student_data['index_moi_truong_ban_be_scaled']),
                    'gpa_scaled': float(student_data['gpa_scaled'])
                }
                advice = generate_advice(safe_student_info)
                st.session_state['ai_mentor_cache'][selected_id] = advice
                st.session_state['current_student'] = selected_id
                caption_log = "Kết quả phân tích"
        else:
            caption_log = "Kết quả truy xuất"

        current_advice = st.session_state['ai_mentor_cache'].get(selected_id, "Chưa có nhận xét.")
        st.caption(caption_log)
        st.success(current_advice)
        
        st.markdown("<div style='margin-top:-5px; margin-bottom:5px;'><hr style='margin:0; border-top: 1px solid #e2e8f0;'/></div>", unsafe_allow_html=True)
        
        export_df = pd.DataFrame([{"Mã SV": student_data['student_id'], "Họ tên": student_data['full_name'], "GPA Quy đổi": f"{student_data['gpa_scaled']:.1f}/100", "Nhận xét": current_advice}])
        st.download_button(label="📥 Tải báo cáo kết quả học tập cá nhân (.csv)", data=export_df.to_csv(index=False).encode('utf-8-sig'), file_name=f"Bao_cao_SV_{student_data['student_id']}.csv", mime="text/csv")
