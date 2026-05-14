import streamlit as st
import numpy as np
from modules.charts import (
    draw_pie_chart, draw_stacked_bar, draw_line_chart, 
    draw_policy_bar, draw_scatter_plot, draw_density_heatmap
)

# Hàm quét điều kiện toán học (Mapping liên tục sang phân loại)
def get_gpa_label(val):
    if np.isnan(val): return "Không xác định"
    if val < 2.0: return "Yếu"
    elif val < 2.5: return "Trung bình"
    elif val < 3.2: return "Khá"
    elif val < 3.6: return "Giỏi"
    else: return "Xuất sắc"

def get_study_time_label(val):
    if np.isnan(val): return "Không xác định"
    if val < 1.5: return "Dưới 2 giờ"
    elif val < 2.5: return "2 - dưới 4 giờ"
    elif val < 3.5: return "4 - dưới 6 giờ"
    elif val < 4.5: return "6 - dưới 8 giờ"
    else: return "Trên 8 giờ"

def render_tab_general():
    if 'filtered_df' not in st.session_state:
        return
        
    df_filtered = st.session_state['filtered_df']
    total_students = len(df_filtered)

    if total_students == 0:
        st.warning("Không có dữ liệu phù hợp với điều kiện phân tích.")
        return

    avg_gpa = df_filtered['gpa_raw'].mean()
    avg_study = df_filtered['time_studying'].mean()
    
    gpa_lbl = get_gpa_label(avg_gpa)
    study_lbl = get_study_time_label(avg_study)

    # Hiển thị thẻ KPI
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.markdown(f"<div style='text-align:center; border-right:1px solid #eee;'><span style='font-size:11px; color:gray;'>Cỡ mẫu (n)</span><br><b style='font-size:18px; color:#2a9d8f;'>{total_students:,}</b></div>", unsafe_allow_html=True)
    kpi2.markdown(f"<div style='text-align:center; border-right:1px solid #eee;'><span style='font-size:11px; color:gray;'>GPA trung bình</span><br><b style='font-size:18px; color:#2a9d8f;'>{avg_gpa:.2f} (Mức {gpa_lbl})</b></div>", unsafe_allow_html=True)
    kpi3.markdown(f"<div style='text-align:center;'><span style='font-size:11px; color:gray;'>Thời gian tự học trung bình</span><br><b style='font-size:18px; color:#2a9d8f;'>{avg_study:.1f} (~ {study_lbl})</b></div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

    f_text = st.session_state.get('filter_text', '')

    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        st.markdown(f"<p style='font-size:13px; font-weight:bold; color:#2a9d8f; margin:0;'>Phân bố kết quả học tập tổng thể {f_text}</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_pie_chart(df_filtered), use_container_width=True, config={'displayModeBar': False})
    with row1_c2:
        st.markdown(f"<p style='font-size:13px; font-weight:bold; color:#2a9d8f; margin:0;'>Cấu trúc học lực phân theo giới tính {f_text}</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_stacked_bar(df_filtered), use_container_width=True, config={'displayModeBar': False})

    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        st.markdown(f"<p style='font-size:13px; font-weight:bold; color:#2a9d8f; margin:0;'>Xu hướng điểm số trung bình theo giai đoạn {f_text}</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_line_chart(df_filtered), use_container_width=True, config={'displayModeBar': False})
    with row2_c2:
        st.markdown(f"<p style='font-size:13px; font-weight:bold; color:#2a9d8f; margin:0;'>So sánh kết quả theo diện chính sách {f_text}</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_policy_bar(df_filtered), use_container_width=True, config={'displayModeBar': False})

    row3_c1, row3_c2 = st.columns(2)
    with row3_c1:
        st.markdown(f"<p style='font-size:13px; font-weight:bold; color:#2a9d8f; margin:0;'>Phân tán mật độ: Hành vi tự học và Kết quả {f_text}</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_scatter_plot(df_filtered), use_container_width=True, config={'displayModeBar': False})
    with row3_c2:
        st.markdown(f"<p style='font-size:13px; font-weight:bold; color:#2a9d8f; margin:0;'>Ma trận tương quan: Hành vi tự học và Kết quả {f_text}</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_density_heatmap(df_filtered), use_container_width=True, config={'displayModeBar': False})
