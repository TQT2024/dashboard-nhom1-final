import streamlit as st
import pandas as pd
import os
from modules.db import load_individual_data
from modules.charts2 import draw_radar_chart
from google import genai
from google.genai.types import HttpOptions

def render_tab_individual():
    try:
        df_profile_all = load_individual_data()
    except Exception as e:
        st.error(f"Lỗi tải thông tin định danh sinh viên: {e}")
        return

    if 'filtered_df' not in st.session_state:
        return
    df_filtered_macro = st.session_state['filtered_df']
    
    allowed_ids = df_filtered_macro['student_id'].astype(str).tolist()
    df_profile_allowed = df_profile_all[df_profile_all['student_id'].astype(str).isin(allowed_ids)]

    if df_profile_allowed.empty:
        st.warning("Không có dữ liệu thỏa mãn tiêu chí bộ lọc.")
        return

    student_options = df_profile_allowed.apply(
        lambda r: f"{r['student_id']} - {r.get('full_name', 'Ẩn danh hóa')}", axis=1
    ).tolist()
    
    selected_option = st.selectbox(
        "Mã số sinh viên phân tích:", options=student_options, key="sb_individual_engine", label_visibility="collapsed"
    )
    
    selected_id = selected_option.split(" - ")[0]
    student_filtered = df_profile_allowed[df_profile_allowed['student_id'].astype(str) == str(selected_id)]
    
    if student_filtered.empty:
        st.error("Không tìm thấy dữ liệu sinh viên.")
        return
        
    student_data = student_filtered.iloc[0]

    col_info, col_chart, col_ai = st.columns([1, 1.3, 1.3])

    with col_info:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#e76f51; margin:0;'>Thông tin hành chính</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:13px; line-height:1.8; background-color:#f8f9fa; padding:12px; border-radius:5px;">
        <b>ID:</b> {student_data['student_id']}<br>
        <b>Họ tên:</b> {student_data.get('full_name', 'Không xác định')}<br>
        <b>Giai đoạn:</b> {student_data.get('year_label', 'Không xác định')}<br>
        <b>Chính sách:</b> {student_data.get('policy_label', 'Không')}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#2a9d8f; margin:15px 0 5px 0;'>Bộ chỉ số năng lực chuẩn hóa</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:12px; line-height:1.7;">
        • Điểm tích lũy GPA: <b>{student_data['gpa_scaled']:.1f}/100</b><br>
        • Năng lực tự lực: <b>{student_data['index_tu_luc_scaled']:.1f}/100</b><br>
        • Hỗ trợ từ cơ sở: <b>{student_data['index_moi_truong_truong_scaled']:.1f}/100</b><br>
        • Môi trường bạn bè: <b>{student_data['index_moi_truong_ban_be_scaled']:.1f}/100</b>
        </div>
        """, unsafe_allow_html=True)

    with col_chart:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#2a9d8f; text-align:center; margin:0;'>Đồ thị đa giác đánh giá tương quan</p>", unsafe_allow_html=True)
        fig_radar = draw_radar_chart(student_data, df_profile_all)
        fig_radar.update_layout(height=350, margin=dict(l=30, r=30, t=30, b=30))
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

    with col_ai:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#2a9d8f; margin:0;'>Phân tích mô hình học thuật (AI)</p>", unsafe_allow_html=True)
        
        ai_clicked = st.button("Trích xuất phân tích tự động", use_container_width=True)
        
        ai_box = st.empty()
        ai_box.markdown("<div style='font-size:13px; color:gray; border:1px dashed #ccc; padding:12px; height:220px; overflow-y:auto;'>Hệ thống ở trạng thái chờ lệnh phân tích.</div>", unsafe_allow_html=True)
        
        if ai_clicked:
            api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
            if not api_key:
                ai_box.markdown(f"<div style='font-size:13px; color:#e76f51; height:220px;'>Chưa cấu hình khóa API. Dữ liệu tĩnh: GPA đạt {student_data['gpa_scaled']:.1f}.</div>", unsafe_allow_html=True)
            else:
                with st.spinner("Đang thực thi thuật toán..."):
                    try:
                        client = genai.Client(api_key=api_key, http_options=HttpOptions(api_version="v1"))
                        
                        prompt = f"Phân tích học thuật: GPA {student_data['gpa_scaled']}/100, Tự lực {student_data['index_tu_luc_scaled']}/100, Môi trường trường {student_data['index_moi_truong_truong_scaled']}/100, Bạn bè {student_data['index_moi_truong_ban_be_scaled']}/100. Đưa ra đánh giá khách quan và đề xuất giải pháp."
                        
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt,
                        )
                        ai_box.markdown(f"<div style='font-size:13px; background-color:#f8f9fa; padding:15px; border-radius:5px; height:220px; overflow-y:auto; border-left:4px solid #2a9d8f; line-height:1.6;'>{response.text}</div>", unsafe_allow_html=True)
                    except Exception as ex:
                        ai_box.markdown(f"<div style='font-size:13px; color:red; height:220px;'>Ngoại lệ xử lý: {ex}</div>", unsafe_allow_html=True)
