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
    
    selected_option = st.selectbox(
        "Mã số sinh viên phân tích:", options=student_options, key="sb_individual_engine", label_visibility="collapsed"
    )
    
    selected_id = str(selected_option.split(" - ")[0])
    student_filtered = df_profile_allowed[df_profile_allowed['student_id'].astype(str) == selected_id]
    
    if student_filtered.empty:
        st.error("Lỗi trích xuất hồ sơ.")
        return
        
    student_data = student_filtered.iloc[0]

    # Phân bổ lưới Hàng 1: Hai cột
    col_info, col_chart = st.columns([1, 1.5])

    with col_info:
        st.markdown("<p style='font-size:15px; font-weight:bold; color:#e76f51; margin:0;'>Thông tin hành chính</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:14px; line-height:1.8; background-color:#f8f9fa; padding:15px; border-radius:5px;">
        <b>ID:</b> {student_data['student_id']}<br>
        <b>Họ tên:</b> {student_data.get('full_name', 'Không xác định')}<br>
        <b>Giai đoạn:</b> {student_data.get('year_label', 'Không xác định')}<br>
        <b>Chính sách:</b> {student_data.get('policy_label', 'Không')}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:15px; font-weight:bold; color:#2a9d8f; margin:20px 0 5px 0;'>Bộ chỉ số chuẩn hóa</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:14px; line-height:1.8;">
        • Điểm tích lũy GPA: <b>{student_data['gpa_scaled']:.1f}/100</b><br>
        • Năng lực tự lực: <b>{student_data['index_tu_luc_scaled']:.1f}/100</b><br>
        • Hỗ trợ cơ sở: <b>{student_data['index_moi_truong_truong_scaled']:.1f}/100</b><br>
        • Môi trường bạn bè: <b>{student_data['index_moi_truong_ban_be_scaled']:.1f}/100</b>
        </div>
        """, unsafe_allow_html=True)

    with col_chart:
        st.markdown("<p style='font-size:15px; font-weight:bold; color:#2a9d8f; text-align:center; margin:0;'>Đối chuẩn Đa giác Radar</p>", unsafe_allow_html=True)
        fig_radar = draw_radar_chart(student_data, df_profile_all)
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

    # Phân bổ lưới Hàng 2: Trợ lý AI tràn toàn bộ chiều rộng
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:15px; font-weight:bold; color:#2a9d8f; margin:0;'>Cố vấn Mô hình (AI)</p>", unsafe_allow_html=True)
    
    ai_clicked = st.button("Kích hoạt trích xuất", use_container_width=True)
    ai_box = st.empty()
    ai_box.markdown("<div style='font-size:14px; color:gray; border:1px dashed #ccc; padding:15px;'>Hệ thống ở trạng thái chờ lệnh phân tích.</div>", unsafe_allow_html=True)
    
    if ai_clicked:
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            ai_box.markdown(f"<div style='font-size:14px; color:#e76f51;'>Chưa cấu hình khóa API. Dữ liệu tĩnh: GPA đạt {student_data['gpa_scaled']:.1f}.</div>", unsafe_allow_html=True)
        else:
            with st.spinner("Đang thực thi biên dịch thuật toán..."):
                try:
                    # Loại bỏ HttpOptions, SDK sẽ tự động xử lý định tuyến chính xác
                    client = genai.Client(api_key=api_key)
                    
                    system_instruction = (
                        "Bạn là Cố vấn học tập tại Đại học. Phân tích số liệu và trả về kết quả tuân thủ nghiêm ngặt định dạng 3 phần: "
                        "1. Điểm mạnh nổi bật. 2. Hạn chế cốt lõi. 3. Giải pháp hành động nước rút. "
                        "Yêu cầu: Tổng khối lượng văn bản không vượt quá 120 từ. Sử dụng văn phong dễ hiểu, khách quan."
                    )
                    
                    prompt = (
                        f"Phân tích hệ số sinh viên {student_data['student_id']}: GPA {student_data['gpa_scaled']}/100, "
                        f"Tự lực {student_data['index_tu_luc_scaled']}/100, Hỗ trợ trường {student_data['index_moi_truong_truong_scaled']}/100, "
                        f"Bạn bè {student_data['index_moi_truong_ban_be_scaled']}/100."
                    )
                    
                    # Bọc cấu hình vào types.GenerateContentConfig
                    advice_config = types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        max_output_tokens=300,
                        temperature=0.2
                    )
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=advice_config
                    )
                    ai_box.markdown(f"<div style='font-size:14px; background-color:#f8f9fa; padding:15px; border-radius:5px; border-left:4px solid #2a9d8f; line-height:1.6;'>{response.text.strip()}</div>", unsafe_allow_html=True)
                
                except Exception as ex:
                    # Fallback Rules khi API gián đoạn
                    gpa = float(student_data['gpa_scaled'])
                    tu_luc = float(student_data['index_tu_luc_scaled'])
                    
                    if gpa < 50 and tu_luc < 50:
                        fallback_html = f"""<div style='font-size:14px; background-color:#fff3cd; color:#856404; padding:15px; border-radius:5px; border-left:4px solid #ffeeba;'>
                        <b>CẢNH BÁO (Fallback Mode):</b> Máy chủ API gián đoạn ({ex}).<br>
                        Hệ thống ghi nhận chỉ số GPA ({gpa:.1f}) và Năng lực tự lực ({tu_luc:.1f}) đều dưới mức trung bình. Đề xuất sinh viên liên hệ Cố vấn học tập để thiết lập lộ trình cải thiện ngay lập tức.</div>"""
                    else:
                        fallback_html = f"""<div style='font-size:14px; background-color:#e2e3e5; color:#383d41; padding:15px; border-radius:5px; border-left:4px solid #d6d8db;'>
                        <b>THÔNG TIN (Fallback Mode):</b> Máy chủ API gián đoạn ({ex}).<br>
                        Năng lực học tập duy trì ở mức ổn định. Tiếp tục phát huy phương pháp tự học hiện tại và tận dụng tối đa hệ sinh thái hỗ trợ từ nhà trường.</div>"""
                    
                    ai_box.markdown(fallback_html, unsafe_allow_html=True)
