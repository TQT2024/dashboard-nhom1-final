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
    
    selected_option = st.selectbox("Chọn sinh viên để phân tích chuyên sâu:", options=student_options)
    selected_id = str(selected_option.split(" - ")[0])
    student_data = df_profile_allowed[df_profile_allowed['student_id'].astype(str) == selected_id].iloc[0]

    st.markdown("<hr style='margin: 10px 0 20px 0;'>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2])

    # ================= CỘT TRÁI: DỮ LIỆU TĨNH + AI =================
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
        
        with st.expander("Phương pháp chuẩn hóa chỉ số"):
            st.latex(r"\text{Chỉ số}_{100} = \text{Likert}_{1-5} \times 20")

        # ĐÃ DI DỜI KHỐI AI SANG CỘT TRÁI ĐỂ LẤP KHOẢNG TRỐNG
        st.markdown("<p style='font-size:15px; font-weight:bold; color:#2a9d8f; margin:15px 0 5px 0;'>Cố vấn học thuật AI</p>", unsafe_allow_html=True)
        
        if st.button("Tạo báo cáo tự động", use_container_width=True):
            api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
            if not api_key:
                st.error("Chưa cấu hình API Key.")
            else:
                with st.spinner("Đang xử lý thuật toán phân tích..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        config = types.GenerateContentConfig(
                            system_instruction=(
                                "Bạn là chuyên gia phân tích dữ liệu giáo dục. Đánh giá dựa trên 4 chỉ số (Thang 100). "
                                "Tuyệt đối KHÔNG dùng định dạng Markdown (không dùng dấu gạch ngang hay dấu sao). "
                                "Chỉ trả về nội dung bằng mã HTML thuần túy theo đúng cấu trúc sau: "
                                "<b>Điểm mạnh nổi bật:</b> [Viết 1 câu trọn vẹn]<br><br>"
                                "<b>Hạn chế cốt lõi:</b> [Viết 1 câu trọn vẹn]<br><br>"
                                "<b>Giải pháp hành động:</b> [Viết 1 câu trọn vẹn]"
                            ),
                            temperature=0.2,
                            max_output_tokens=500
                        )
                        
                        prompt = f"GPA: {student_data['gpa_scaled']}, Tự lực: {student_data['index_tu_luc_scaled']}, Trường: {student_data['index_moi_truong_truong_scaled']}, Bạn bè: {student_data['index_moi_truong_ban_be_scaled']}."
                        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt, config=config)
                        
                        # Khung Auto-expand, đồng bộ màu Xanh Mint, hiển thị 100% nội dung HTML
                        custom_box = f"""
                        <div style="background-color: #f0f7f6; padding: 15px; border-radius: 5px; border-left: 4px solid #2a9d8f; font-size: 14px; line-height: 1.6; color: #222;">
                            {response.text.strip()}
                        </div>
                        """
                        st.markdown(custom_box, unsafe_allow_html=True)
                        
                    except Exception as ex:
                        fallback_box = f"""
                        <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffeeba; font-size: 14px; line-height: 1.6; color: #856404;">
                            <b>Cảnh báo (Fallback):</b> API gián đoạn ({ex}).<br><br>
                            Hệ thống ghi nhận GPA hiện tại: {student_data['gpa_scaled']:.1f}.<br>
                            Đề xuất: Tập trung cải thiện các chỉ số có tỷ trọng thấp.
                        </div>
                        """
                        st.markdown(fallback_box, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: #fafafa; padding: 15px; border-radius: 5px; border: 1px dashed #ccc; font-size: 13px; color: gray; text-align: center;">
                Nhấn nút để AI phân tích.
            </div>
            """, unsafe_allow_html=True)

    # ================= CỘT PHẢI: TRỰC QUAN HÓA =================
    with col_right:
        st.markdown("<p style='font-size:16px; font-weight:bold; color:#2a9d8f; text-align:center;'>Đối chuẩn đa giác Radar</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_radar_chart(student_data, df_profile_all), use_container_width=True, config={'displayModeBar': False})
