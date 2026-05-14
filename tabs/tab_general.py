import streamlit as st
from modules.charts import (
    draw_pie_chart, draw_stacked_bar, draw_line_chart, 
    draw_policy_bar, draw_scatter_plot, draw_density_heatmap
)

def render_tab_general():
    if 'filtered_df' not in st.session_state:
        return
        
    df_filtered = st.session_state['filtered_df']
    total_students = len(df_filtered)

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.markdown(f"<div style='text-align:center; border-right:1px solid #eee;'><span style='font-size:11px; color:gray;'>Cỡ mẫu (n)</span><br><b style='font-size:18px; color:#2a9d8f;'>{total_students:,}</b></div>", unsafe_allow_html=True)
    kpi2.markdown(f"<div style='text-align:center; border-right:1px solid #eee;'><span style='font-size:11px; color:gray;'>GPA trung bình</span><br><b style='font-size:18px; color:#2a9d8f;'>{df_filtered['gpa_raw'].mean():.2f} / 5.00</b></div>", unsafe_allow_html=True)
    kpi3.markdown(f"<div style='text-align:center;'><span style='font-size:11px; color:gray;'>Mức độ tự học trung bình</span><br><b style='font-size:18px; color:#2a9d8f;'>{df_filtered['time_studying'].mean():.1f} / 5.0</b></div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

    if total_students == 0:
        st.info("Không có dữ liệu phù hợp với điều kiện phân tích.")
        return

    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        st.markdown("<p style='font-size:13px; font-weight:bold; color:#2a9d8f; margin:0;'>Phân bố kết quả học tập tổng thể</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_pie_chart(df_filtered), use_container_width=True, config={'displayModeBar': False})
    with row1_c2:
        st.markdown("<p style='font-size:13px; font-weight:bold; color:#2a9d8f; margin:0;'>Cấu trúc học lực phân theo giới tính</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_stacked_bar(df_filtered), use_container_width=True, config={'displayModeBar': False})

    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        st.markdown("<p style='font-size:13px; font-weight:bold; color:#2a9d8f; margin:0;'>Xu hướng điểm số trung bình theo giai đoạn</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_line_chart(df_filtered), use_container_width=True, config={'displayModeBar': False})
    with row2_c2:
        st.markdown("<p style='font-size:13px; font-weight:bold; color:#2a9d8f; margin:0;'>So sánh kết quả theo diện chính sách</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_policy_bar(df_filtered), use_container_width=True, config={'displayModeBar': False})

    row3_c1, row3_c2 = st.columns(2)
    with row3_c1:
        st.markdown("<p style='font-size:13px; font-weight:bold; color:#2a9d8f; margin:0;'>Phân tán mật độ: Hành vi tự học và Kết quả</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_scatter_plot(df_filtered), use_container_width=True, config={'displayModeBar': False})
    with row3_c2:
        st.markdown("<p style='font-size:13px; font-weight:bold; color:#2a9d8f; margin:0;'>Ma trận tương quan: Hành vi tự học và Kết quả</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_density_heatmap(df_filtered), use_container_width=True, config={'displayModeBar': False})
