import streamlit as st
import plotly.express as px
import pandas as pd
from modules.database import load_individual_data
from modules.ai_mentor import generate_advice

def render_tab_individual():
    df = load_individual_data()
    if df.empty:
        st.warning("Hệ thống chưa tải được dữ liệu hồ sơ cá nhân. Vui lòng kiểm tra lại SQL View.")
        return

    st.markdown("### Tra cứu Hồ sơ Cá nhân & Khuyến nghị")

    student_list = df['student_id'].tolist()
    selected_id = st.selectbox("Lựa chọn Mã Sinh viên (Student ID):", options=student_list, index=0)

    student_data = df[df['student_id'] == selected_id].iloc

    st.info(
        f"👤 **Họ và tên:** {student_data['full_name']} | "
        f"📧 **Email:** {student_data['email']} | "
        f"🧬 **Giới tính:** {student_data['gender_label']} | "
        f"📅 **Năm học:** {student_data['year_label']}"
    )

    col_chart, col_ai = st.columns([1.2, 1])

    with col_chart:
        st.markdown("**Biểu đồ Năng lực (Đối chiếu Trung bình Khóa)**")
        mean_data = df[['index_tu_luc_scaled', 'index_moi_truong_truong_scaled', 'index_moi_truong_ban_be_scaled', 'gpa_scaled']].mean()
        categories = ['Tự lực', 'Hỗ trợ từ Trường', 'Áp lực Bạn bè', 'Kết quả GPA']
        
        radar_df = pd.DataFrame({
            'Chỉ_số': categories * 2,
            'Điểm': [
                float(student_data['index_tu_luc_scaled']), float(student_data['index_moi_truong_truong_scaled']), 
                float(student_data['index_moi_truong_ban_be_scaled']), float(student_data['gpa_scaled']),
                float(mean_data['index_tu_luc_scaled']), float(mean_data['index_moi_truong_truong_scaled']), 
                float(mean_data['index_moi_truong_ban_be_scaled']), float(mean_data['gpa_scaled'])
            ],
            'Đối_tượng': ['Cá nhân'] * 4 + ['Trung bình khóa'] * 4
        })

        fig_radar = px.line_polar(
            radar_df, r='Điểm', theta='Chỉ_số', color='Đối_tượng', line_close=True,
            range_r=, color_discrete_map={'Cá nhân': '#1f77b4', 'Trung bình khóa': '#7f7f7f'}
        )
        fig_radar.update_traces(line=dict(dash="dot", width=2), selector={"name": "Trung bình khóa"})
        fig_radar.update_traces(line=dict(width=3.5), selector={"name": "Cá nhân"})
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, showticklabels=True, tickfont=dict(size=9))),
            margin=dict(l=50, r=50, t=30, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        # SỬA ĐỔI CÚ PHÁP CHUẨN 2026: Dùng width='stretch'
        st.plotly_chart(fig_radar, width='stretch')

    with col_ai:
        st.markdown("**AI Mentor (Hệ thống Cố vấn)**")
        
        # SỬA ĐỔI QUAN TRỌNG: Thay tên biến cache sang 'ai_mentor_cache' tránh xung đột kiểu dữ liệu cũ
        if 'ai_mentor_cache' not in st.session_state:
            st.session_state['ai_mentor_cache'] = {}
            st.session_state['current_student'] = None

        if st.session_state['current_student'] != selected_id:
            with st.spinner("Hệ thống AI đang tổng hợp dữ liệu và phân tích..."):
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
                caption_log = "✨ Kết quả phân tích trực tiếp từ Gemini API (2026)"
        else:
            caption_log = "⚡ Dữ liệu truy xuất tức thì từ bộ nhớ đệm (Session Cache)"

        # Gọi hàm an toàn qua phương thức .get() từ kho lưu trữ mới tạo
        current_advice = st.session_state['ai_mentor_cache'].get(selected_id, "Chưa có nhận xét.")
        st.caption(caption_log)
        st.success(current_advice)
        
        st.markdown("---")
        export_df = pd.DataFrame([{"Mã SV": student_data['student_id'], "Họ tên": student_data['full_name'], "GPA Quy đổi": f"{student_data['gpa_scaled']:.1f}/100", "Nhận xét từ AI": current_advice}])
        st.download_button(label="📥 Tải báo cáo học tập cá nhân tích hợp AI (.csv)", data=export_df.to_csv(index=False).encode('utf-8-sig'), file_name=f"Bao_cao_AI_{student_data['student_id']}.csv", mime="text/csv")
