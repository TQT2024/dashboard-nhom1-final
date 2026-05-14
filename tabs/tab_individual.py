import streamlit as st
import pandas as pd
from modules.database import load_individual_data
from modules.ai_mentor import generate_advice
# Gọi chính xác từ module charts2 dành riêng cho Tab Cá nhân
from modules.charts2 import draw_radar_chart

def render_tab_individual():
    df = load_individual_data()
    if df.empty:
        st.warning("Hệ thống chưa tải được dữ liệu hồ sơ cá nhân. Vui lòng kiểm tra lại SQL View.")
        return

    # Nhúng CSS tối giản lề đệm để thắt chặt không gian hiển thị, ép vừa vặn 1 trang
    st.markdown("""
        <style>
        .block-container { padding-top: 1rem; padding-bottom: 1rem; }
        div.stSelectbox { margin-bottom: -10px; }
        .stAlert { padding: 8px 12px; border-radius: 6px; margin-bottom: -10px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("### Tra cứu chi tiết kết quả sinh viên")

    student_list = df['student_id'].tolist()
    selected_id = st.selectbox("Lựa chọn Mã Sinh viên (Student ID):", options=student_list, index=0)

    # ĐÃ SỬA LỖI: Bổ sung chỉ mục [0] vào sau .iloc để định vị chính xác 1 dòng dữ liệu sinh viên
    student_data = df[df['student_id'] == selected_id].iloc[0]

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
                caption_log = "Result"
        else:
            caption_log = "Cache"

        current_advice = st.session_state['ai_mentor_cache'].get(selected_id, "Chưa có nhận xét.")
        st.caption(caption_log)
        st.success(current_advice)
        
        st.markdown("<div style='margin-top:-5px; margin-bottom:5px;'><hr style='margin:0; border-top: 1px solid #e2e8f0;'/></div>", unsafe_allow_html=True)
        
        export_df = pd.DataFrame([{"Mã SV": student_data['student_id'], "Họ tên": student_data['full_name'], "GPA Quy đổi": f"{student_data['gpa_scaled']:.1f}/100", "Nhận xét": current_advice}])
        st.download_button(label="📥 Tải báo cáo kết quả học tập cá nhân (.csv)", data=export_df.to_csv(index=False).encode('utf-8-sig'), file_name=f"Bao_cao_SV_{student_data['student_id']}.csv", mime="text/csv")
