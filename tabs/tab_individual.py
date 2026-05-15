import streamlit as st
import os
from modules.db import load_individual_data
from modules.charts2 import draw_radar_chart
from google import genai
from google.genai import types

def render_tab_individual():
    try:
        df_profile_all = load_individual_data()
    except Exception as e:
        st.error(f"Lỗi truy xuất hệ thống: {e}")
        return

    if 'filtered_df' not in st.session_state:
        return
    df_filtered_macro = st.session_state['filtered_df']
    
    allowed_ids = df_filtered_macro['student_id'].astype(str).tolist()
    df_profile_allowed = df_profile_all[df_profile_all['student_id'].astype(str).isin(allowed_ids)]

    if df_profile_allowed.empty:
        st.warning("Không có dữ liệu thỏa mãn bộ lọc.")
        return

    student_options = df_profile_allowed.apply(
        lambda r: f"{r['student_id']} - {r.get('full_name', 'Ẩn danh')}", axis=1
    ).tolist()
    
    selected_option = st.selectbox("Chọn sinh viên:", options=student_options, label_visibility="collapsed")
    selected_id = str(selected_option.split(" - ")[0])
    student_data = df_profile_allowed[df_profile_allowed['student_id'].astype(str) == selected_id].iloc[0]

    # Bố cục hàng 1: Thông tin (Trái) - Biểu đồ (Phải)
    col_left, col_right = st.columns([1, 2])

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
        
        st.markdown("<p style='font-size:15px; font-weight:bold; color:#2a9d8f; margin:15px 0 5px 0;'>Chỉ số năng lực</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:14px; line-height:1.6; background-color:#f0f7f6; padding:15px; border-radius:5px; border:1px solid #d1e7e4;">
        • GPA: <b>{student_data['gpa_scaled']:.1f}</b><br>
        • Tự lực: <b>{student_data['index_tu_luc_scaled']:.1f}</b><br>
        • Trường: <b>{student_data['index_moi_truong_truong_scaled']:.1f}</b><br>
        • Bạn bè: <b>{student_data['index_moi_truong_ban_be_scaled']:.1f}</b>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("<p style='font-size:15px; font-weight:bold; color:#2a9d8f; text-align:center;'>Đối chuẩn đa giác Radar</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_radar_chart(student_data, df_profile_all), use_container_width=True, config={'displayModeBar': False})

    # Bố cục hàng 2: AI Mentor (Tràn ngang)
    st.markdown("<p style='font-size:15px; font-weight:bold; color:#2a9d8f; margin-top:10px;'>Cố vấn học thuật AI</p>", unsafe_allow_html=True)
    
    if st.button("Trích xuất phân tích mô hình", use_container_width=True):
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            st.error("Thiếu API Key.")
        else:
            with st.spinner("Đang biên dịch..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    config = types.GenerateContentConfig(
                        system_instruction=(
                            "Bạn là Cố vấn học tập. Phân tích số liệu và trả về kết quả định dạng danh sách Markdown: "
                            "- **Điểm mạnh:** ... \n- **Hạn chế:** ... \n- **Hành động:** ... \n"
                            "Văn phong học thuật, ngắn gọn, không quá 150 từ."
                        ),
                        temperature=0.2,
                        max_output_tokens=500
                    )
                    
                    prompt = f"Dữ liệu: GPA {student_data['gpa_scaled']}, Tự lực {student_data['index_tu_luc_scaled']}, Trường {student_data['index_moi_truong_truong_scaled']}, Bạn bè {student_data['index_moi_truong_ban_be_scaled']}."
                    
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt, config=config)
                    
                    # Sử dụng st.info để khung tự co dãn theo chữ, không bị cắt
                    st.info(response.text.strip())
                    
                except Exception as ex:
                    # Fallback tĩnh
                    st.warning(f"Lỗi API: {ex}. GPA hiện tại: {student_data['gpa_scaled']:.1f}. Cần tập trung cải thiện chỉ số Tự lực.")
    else:
        st.caption("Nhấn nút trên để xem phân tích chi tiết từ trí tuệ nhân tạo.")
