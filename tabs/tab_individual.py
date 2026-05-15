import streamlit as st
import os
from modules.db import load_individual_data
from modules.charts2 import draw_radar_chart
from modules.ai_mentor import generate_advice

def render_tab_individual():
    try:
        df_profile_all = load_individual_data()
    except Exception as e:
        st.error(f"Lỗi truy xuất hệ thống định danh: {e}")
        return

    if 'filtered_df' not in st.session_state:
        return
    df_filtered_macro = st.session_state['filtered_df']
    
    allowed_ids = df_filtered_macro['student_id'].astype(str).tolist()
    df_profile_allowed = df_profile_all[df_profile_all['student_id'].astype(str).isin(allowed_ids)]

    if df_profile_allowed.empty:
        st.warning("Không có dữ liệu thỏa mãn tiêu chí bộ lọc hệ thống.")
        return

    student_options = df_profile_allowed.apply(
        lambda r: f"{r['student_id']} - {r.get('full_name', 'Ẩn danh hóa')}", axis=1
    ).tolist()
    
    selected_option = st.selectbox("Chọn sinh viên để phân tích chuyên sâu:", options=student_options)
    selected_id = str(selected_option.split(" - ")[0])
    student_data = df_profile_allowed[df_profile_allowed['student_id'].astype(str) == selected_id].iloc[0]

    st.markdown("<hr style='margin: 10px 0 20px 0;'>", unsafe_allow_html=True)

    # ================= HÀNG 1: DỮ LIỆU TĨNH & BIỂU ĐỒ =================
    col_left, col_right = st.columns([1, 1.5]) 

    with col_left:
        st.markdown("<p style='font-size:15px; font-weight:bold; color:#e76f51; margin-bottom:5px;'>Hồ sơ hành chính</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:14px; line-height:1.6; background-color:#f8f9fa; padding:15px; border-radius:5px; border:1px solid #eee;">
        <b>ID:</b> {student_data['student_id']}<br>
        <b>Họ tên:</b> {student_data.get('full_name', 'N/A')}<br>
        <b>Giai đoạn:</b> {student_data.get('year_label', 'N/A')}<br>
        <b>Chính sách:</b> {student_data.get('policy_label', 'Không')}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:15px; font-weight:bold; color:#2a9d8f; margin:15px 0 5px 0;'>Chỉ số năng lực (Thang 100)</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:14px; line-height:1.6; background-color:#f8f9fa; padding:15px; border-radius:5px; border:1px solid #eee;">
        • Điểm tích lũy GPA: <b>{student_data['gpa_scaled']:.1f}</b><br>
        • Năng lực tự lực: <b>{student_data['index_tu_luc_scaled']:.1f}</b><br>
        • Hỗ trợ từ trường: <b>{student_data['index_moi_truong_truong_scaled']:.1f}</b><br>
        • Áp lực bạn bè: <b>{student_data['index_moi_truong_ban_be_scaled']:.1f}</b>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔍 Phương pháp chuẩn hóa chỉ số"):
            st.latex(r"\text{Chỉ số}_{100} = \text{Likert}_{1-5} \times 20")
            st.caption("Dữ liệu được tịnh tiến tuyến tính để đồng bộ không gian đo lường.")

    with col_right:
        st.markdown("<p style='font-size:16px; font-weight:bold; color:#2a9d8f; text-align:center;'>Đối chuẩn đa giác Radar</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_radar_chart(student_data, df_profile_all), use_container_width=True, config={'displayModeBar': False})

    # ================= HÀNG 2: CÔNG CỤ CHUYÊN SÂU (TRÀN TOÀN MÀN HÌNH) =================
    st.markdown("---")
    st.markdown("<p style='font-size:15px; font-weight:bold; color:#2a9d8f; margin-bottom:10px;'>Cố vấn học thuật AI (Gemini Flash)</p>", unsafe_allow_html=True)
    
    if st.button("Kích hoạt Phân tích tự động", use_container_width=True):
        with st.spinner("Đang biên dịch thuật toán phân tích..."):
            # Lời gọi duy nhất đến Backend, giải phóng hoàn toàn gánh nặng cho file UI
            ai_result = generate_advice(student_data)
            
            # Khung st.info bản địa: Hiển thị mượt Markdown, nền xanh chuẩn, tự động co giãn 100%
            st.info(ai_result, icon="💡")
    else:
        st.caption("Nhấn nút để kích hoạt hệ thống AI phân tích dữ liệu sinh viên.")
