import streamlit as st
import numpy as np
from modules.charts import (
    draw_pie_chart, draw_line_chart, draw_density_heatmap,
    draw_scatter_plot, draw_stacked_bar, draw_treemap
)

def get_gpa_label(val):
    if np.isnan(val): return "N/A"
    if val < 2.0: return "Yếu"
    elif val < 2.5: return "Trung bình"
    elif val < 3.2: return "Khá"
    elif val < 3.6: return "Giỏi"
    else: return "Xuất sắc"

def get_study_label(val):
    if np.isnan(val): return "N/A"
    if val < 1.5: return "Dưới 2 giờ"
    elif val < 2.5: return "2 - dưới 4 giờ"
    elif val < 3.5: return "4 - dưới 6 giờ"
    elif val < 4.5: return "6 - dưới 8 giờ"
    else: return "Trên 8 giờ"

def render_tab_general():
    if 'filtered_df' not in st.session_state: return
    df_filtered = st.session_state['filtered_df']
    
    total_students = len(df_filtered)
    if total_students == 0:
        st.warning("Không có dữ liệu phù hợp với bộ lọc.")
        return

    avg_gpa = df_filtered['gpa_raw'].mean()
    avg_study = df_filtered['time_studying'].mean()

    # Khối 1: Header định danh & KPI
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.markdown(f"<div style='text-align:center; border-right:1px solid #eee;'><span style='font-size:11px; color:gray;'>Cỡ mẫu (n)</span><br><b style='font-size:18px; color:#2a9d8f;'>{total_students:,}</b></div>", unsafe_allow_html=True)
    kpi2.markdown(f"<div style='text-align:center; border-right:1px solid #eee;'><span style='font-size:11px; color:gray;'>GPA quy đổi</span><br><b style='font-size:18px; color:#2a9d8f;'>{avg_gpa:.2f} ({get_gpa_label(avg_gpa)})</b></div>", unsafe_allow_html=True)
    kpi3.markdown(f"<div style='text-align:center;'><span style='font-size:11px; color:gray;'>Thời gian tự học</span><br><b style='font-size:18px; color:#2a9d8f;'>{avg_study:.1f} ({get_study_label(avg_study)})</b></div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

    f_suffix = st.session_state.get('filter_suffix', '')
    
    # Ẩn thanh công cụ Plotly
    chart_config = {'displayModeBar': False}

    # Khối 2: Thực trạng (Tầng 1 - What)
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown(f"<p style='font-size:12px; font-weight:bold; color:#2a9d8f; margin:0;'>1. Cấu trúc học lực {f_suffix}</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_pie_chart(df_filtered), use_container_width=True, config=chart_config)
    with r1c2:
        st.markdown(f"<p style='font-size:12px; font-weight:bold; color:#2a9d8f; margin:0;'>2. Xu hướng GPA theo khóa {f_suffix}</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_line_chart(df_filtered), use_container_width=True, config=chart_config)

    # Khối 3: Nhân tố tự thân (Tầng 2 - Why Internal)
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.markdown(f"<p style='font-size:12px; font-weight:bold; color:#2a9d8f; margin:0;'>3. Tương quan: Tự học & Học lực {f_suffix}</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_density_heatmap(df_filtered), use_container_width=True, config=chart_config)
    with r2c2:
        st.markdown(f"<p style='font-size:12px; font-weight:bold; color:#2a9d8f; margin:0;'>4. Phân tán: Năng lực tự lực & GPA {f_suffix}</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_scatter_plot(df_filtered), use_container_width=True, config=chart_config)

    # Khối 4: Nhân tố ngoại cảnh (Tầng 3 - Why External)
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        st.markdown(f"<p style='font-size:12px; font-weight:bold; color:#2a9d8f; margin:0;'>5. Cấu trúc học lực theo giới tính {f_suffix}</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_stacked_bar(df_filtered), use_container_width=True, config=chart_config)
    with r3c2:
        st.markdown(f"<p style='font-size:12px; font-weight:bold; color:#2a9d8f; margin:0;'>6. Phân cấp: Hỗ trợ từ trường & Học lực {f_suffix}</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_treemap(df_filtered), use_container_width=True, config=chart_config)
