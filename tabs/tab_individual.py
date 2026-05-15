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
        st.warning("Không có dữ liệu thỏa mãn bộ lọc hệ thống.")
        return

    student_options = df_profile_allowed.apply(
        lambda r: f"{r['student_id']} - {r.get('full_name', 'Ẩn danh hóa')}", axis=1
    ).tolist()
    
    selected_option = st.selectbox("Chọn sinh viên để phân tích:", options=student_options)
    selected_id = str(selected_option.split(" - ")[0])
    student_data = df_profile_allowed[df_profile_allowed['student_id'].astype(str) == selected_id].iloc[0]

    st.markdown("<hr style='margin: 10px 0 20px 0;'>", unsafe_allow_html=True)

    # Chia lưới 2 cột: Trái (Dữ liệu + AI) | Phải (Radar)
    col_left, col_right = st.columns([1, 1.5]) 

    with col_left:
        # 1. Khối thông tin định danh
        st.markdown("<p style='font-size:15px; font-weight:bold; color:#e76f51; margin-bottom:5px;'>Hồ sơ sinh viên</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:14px; line-height:1.6; background-color:#f8f9fa; padding:15px; border-radius:5px; border:1px solid #eee;">
        <b>ID:</b> {student_data['student_id']}<br>
        <b>Họ tên:</b> {student_data.get('full_name', 'N/A')}<br>
        <b>Niên khoá:</b> {student_data.get('year_label', 'N/A')}<br>
        <b>Diện chính sách:</b> {student_data.get('policy_label', 'Không')}
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Khối chỉ số năng lực
        st.markdown("<p style='font-size:15px; font-weight:bold; color:#2a9d8f; margin:15px 0 5px 0;'>Chỉ số học tập</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:14px; line-height:1.6; background-color:#f8f9fa; padding:15px; border-radius:5px; border:1px solid #eee;">
        • Điểm tích lũy GPA: <b>{student_data['gpa_scaled']:.1f}</b><br>
        • Năng lực tự học: <b>{student_data['index_tu_luc_scaled']:.1f}</b><br>
        • Hỗ trợ từ trường: <b>{student_data['index_moi_truong_truong_scaled']:.1f}</b><br>
        • Áp lực bạn bè: <b>{student_data['index_moi_truong_ban_be_scaled']:.1f}</b>
        </div>
        """, unsafe_allow_html=True)
        
        # 3. Giải thích phương pháp
        with st.expander("Phương pháp chuẩn hóa"):
            st.markdown("**Mô hình chuyển đổi dữ liệu:**")
            st.latex(r"\text{Index}_{100} = \text{Value}_{Likert} \times 20")
            st.info("""
            Việc tịnh tiến từ thang 5 sang thang 100 giúp đồng bộ hóa các biến số hành vi 
            với kết quả học tập (GPA) để trực quan hóa đa giác Radar chính xác.
            """)

        # 4. KHỐI AI: Đặt ở đây để lấp đầy khoảng trống cột trái
        st.markdown("<p style='font-size:15px; font-weight:bold; color:#2a9d8f; margin:15px 0 5px 0;'>Phân tích cố vấn</p>", unsafe_allow_html=True)
        if st.button("Bắt đầu phân tích hồ sơ", use_container_width=True):
            with st.spinner("Đang phân tích..."):
                # Gọi hàm từ module ai_mentor
                ai_result = generate_advice(student_data)
                # HIỂN THỊ KẾT QUẢ (Đã bỏ icon theo ý em)
                st.info(ai_result) 
        else:
            st.caption("Nhấn nút để phân tích.")

    with col_right:
        # Cột phải tập trung hiển thị Biểu đồ Radar lớn
        st.markdown("<p style='font-size:16px; font-weight:bold; color:#2a9d8f; text-align:center;'>Đối chuẩn đa giác Radar</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_radar_chart(student_data, df_profile_all), use_container_width=True, config={'displayModeBar': False})
