import streamlit as st
import pandas as pd
import os
from modules.db import load_individual_data
from modules.charts2 import draw_radar_chart
# Gọi thư viện SDK mới chuẩn năm 2026
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
        st.warning("⚠️ Không có sinh viên nào thỏa mãn tiêu chí bộ lọc.")
        return

    student_options = df_profile_allowed.apply(
        lambda r: f"{r['student_id']} - {r.get('full_name', 'Ẩn danh hóa')}", axis=1
    ).tolist()
    
    # Rút gọn khoảng cách tiêu đề để đẩy cấu phần lên trên
    selected_option = st.selectbox(
        "Mã số sinh viên phân tích:", options=student_options, key="sb_individual_engine", label_visibility="collapsed"
    )
    
    selected_id = selected_option.split(" - ")[0]
    student_filtered = df_profile_allowed[df_profile_allowed['student_id'].astype(str) == str(selected_id)]
    
    if student_filtered.empty:
        st.error("Không tìm thấy dữ liệu sinh viên.")
        return
        
    student_data = student_filtered.iloc[0]

    # THIẾT KẾ MỚI: Chia 3 cột phủ đều màn hình, khống chế không cho cuộn
    col_info, col_chart, col_ai = st.columns([1, 1.2, 1.3])

    with col_info:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#e76f51; margin:0;'>📋 Lý lịch hành chính</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:12px; line-height:1.6; background-color:#f8f9fa; padding:8px; border-radius:5px;">
        <b>ID:</b> {student_data['student_id']}<br>
        <b>Họ tên:</b> {student_data.get('full_name', 'Chưa rõ')}<br>
        <b>Phân loại:</b> {student_data.get('year_label', 'Chưa rõ')}<br>
        <b>Chính sách:</b> {student_data.get('policy_label', 'Không')}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#2a9d8f; margin:8px 0 0 0;'>🎯 Năng lực chuẩn hóa (Thang 100)</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:11px; line-height:1.5;">
        • Điểm tích lũy GPA: <b>{student_data['gpa_scaled']:.1f}</b><br>
        • Năng lực Tự lực: <b>{student_data['index_tu_luc_scaled']:.1f}</b><br>
        • Hỗ trợ từ Trường: <b>{student_data['index_moi_truong_truong_scaled']:.1f}</b><br>
        • Động lực Bạn bè: <b>{student_data['index_moi_truong_ban_be_scaled']:.1f}</b>
        </div>
        """, unsafe_allow_html=True)

    with col_chart:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#2a9d8f; text-align:center; margin:0;'>🕸️ Radar Tương Quan Năng Lực</p>", unsafe_allow_html=True)
        fig_radar = draw_radar_chart(student_data, df_profile_all)
        # Giảm chiều cao biểu đồ radar xuống 240px để ôm khít màn hình
        fig_radar.update_layout(height=240, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})

    with col_ai:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#2a9d8f; margin:0;'>🤖 Tư vấn Học thuật chuyên sâu</p>", unsafe_allow_html=True)
        
        # Thiết kế nút bấm AI nhỏ gọn tiết kiệm không gian
        ai_clicked = st.button("✨ Gọi trợ lý Gemini 2.5 Flash", use_container_width=True)
        
        # Khung chứa text nhận xét của AI cố định chiều cao, tự sinh thanh cuộn nội bộ nếu quá dài
        ai_box = st.empty()
        ai_box.markdown("<div style='font-size:12px; color:gray; border:1px dashed #ccc; padding:10px; height:180px; overflow-y:auto;'>Nhấn nút phía trên để AI xuất kết quả phân tích...</div>", unsafe_allow_html=True)
        
        if ai_clicked:
            api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
            if not api_key:
                ai_box.markdown(f"<div style='font-size:12px; color:#e76f51; height:180px;'>⚠️ Chưa cấu hình GEMINI_API_KEY. Điểm Tự lực: {student_data['index_tu_luc_scaled']:.1f}/100.</div>", unsafe_allow_html=True)
            else:
                with st.spinner("AI đang tính toán..."):
                    try:
                        # SỬA LỖI: Ép cứng api_version="v1" để triệt tiêu lỗi 404 v1beta của mô hình mới
                        client = genai.Client(api_key=api_key, http_options=HttpOptions(api_version="v1"))
                        
                        prompt = f"Phân tích hồ sơ SV: GPA {student_data['gpa_scaled']}/100, Tự lực {student_data['index_tu_luc_scaled']}/100, Trường {student_data['index_moi_truong_truong_scaled']}/100, Bạn bè {student_data['index_moi_truong_ban_be_scaled']}/100. Trả lời dưới 100 từ gồm: 1 điểm mạnh/yếu nhất và 1 hành động cốt lõi."
                        
                        # Gọi chính xác mô hình gemini-2.5-flash của bạn
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt,
                        )
                        ai_box.markdown(f"<div style='font-size:12px; background-color:#edf2f4; padding:10px; border-radius:5px; height:180px; overflow-y:auto; border-left:4px solid #2a9d8f;'>{response.text}</div>", unsafe_allow_html=True)
                    except Exception as ex:
                        ai_box.markdown(f"<div style='font-size:12px; color:red; height:180px;'>Lỗi hệ thống: {ex}</div>", unsafe_allow_html=True)
