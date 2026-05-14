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

    # Khung KPI tinh gọn, ép sát lề trên
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.markdown(f"<div style='text-align:center; border-right:1px solid #eee;'><span style='font-size:11px; color:gray;'>Mẫu khảo sát (n)</span><br><b style='font-size:18px; color:#2a9d8f;'>{total_students:,} SV</b></div>", unsafe_allow_html=True)
    kpi2.markdown(f"<div style='text-align:center; border-right:1px solid #eee;'><span style='font-size:11px; color:gray;'>GPA trung bình</span><br><b style='font-size:18px; color:#2a9d8f;'>{df_filtered['gpa_raw'].mean():.2f} / 5.00</b></div>", unsafe_allow_html=True)
    kpi3.markdown(f"<div style='text-align:center;'><span style='font-size:11px; color:gray;'>Tự học bình quân</span><br><b style='font-size:18px; color:#2a9d8f;'>Mức {df_filtered['time_studying'].mean():.1f} / 5</b></div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)

    if total_students == 0:
        st.info("Không có dữ liệu phù hợp với điều kiện bộ lọc.")
        return

    # TÁI CẤU TRÚC: Chuyển đổi sang lưới 3 cột để ép gọn không gian dọc
    row1_c1, row1_c2, row1_c3 = st.columns(3)
    row2_c1, row2_c2, row2_c3 = st.columns(3)

    # --- HÀNG 1 ---
    with row1_c1:
        st.markdown("<p style='font-size:12px; font-weight:bold; color:#2a9d8f; margin:0;'>📊 Cơ cấu học lực nhóm</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_pie_chart(df_filtered), use_container_width=True, config={'displayModeBar': False})
    with row1_c2:
        st.markdown("<p style='font-size:12px; font-weight:bold; color:#2a9d8f; margin:0;'>📊 Học lực theo giới tính (%)</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_stacked_bar(df_filtered), use_container_width=True, config={'displayModeBar': False})
    with row1_c3:
        st.markdown("<p style='font-size:12px; font-weight:bold; color:#2a9d8f; margin:0;'>📈 Biến thiên kết quả theo năm</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_line_chart(df_filtered), use_container_width=True, config={'displayModeBar': False})

    # --- HÀNG 2 ---
    with row2_c1:
        st.markdown("<p style='font-size:12px; font-weight:bold; color:#2a9d8f; margin:0;'>📊 Kết quả theo diện chính sách</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_policy_bar(df_filtered), use_container_width=True, config={'displayModeBar': False})
    with row2_c2:
        st.markdown("<p style='font-size:12px; font-weight:bold; color:#2a9d8f; margin:0;'>🔮 Thời gian học vs Học lực</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_scatter_plot(df_filtered), use_container_width=True, config={'displayModeBar': False})
    with row2_c3:
        st.markdown("<p style='font-size:12px; font-weight:bold; color:#2a9d8f; margin:0;'>🔥 Bản đồ nhiệt phân hạng SV</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_density_heatmap(df_filtered), use_container_width=True, config={'displayModeBar': False})
