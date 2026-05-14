import streamlit as st
from modules.charts import (
    draw_pie_chart, draw_stacked_bar, draw_line_chart, 
    draw_policy_bar, draw_scatter_plot, draw_density_heatmap
)

def render_tab_general():
    # Lấy tập dữ liệu đã qua xử lý lọc tại Sidebar từ bộ nhớ dùng chung
    if 'filtered_df' not in st.session_state:
        st.warning("Hệ thống đang đồng bộ dữ liệu lọc...")
        return
        
    df_filtered = st.session_state['filtered_df']

    # Thống kê nhanh các chỉ số KPI động theo tập dữ liệu hiện hành
    total_students = len(df_filtered)
    avg_gpa_100 = df_filtered['gpa_scaled'].mean() if total_students > 0 else 0
    avg_study_hours = df_filtered['time_studying'].mean() if total_students > 0 else 0

    st.markdown("##### 📊 Kết quả phân tích tổng quan nhóm Toàn khối")
    
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric("Tổng mẫu khảo sát (n)", f"{total_students:,} SV")
    with kpi2:
        st.metric("GPA trung bình toàn nhóm", f"{df_filtered['gpa_raw'].mean():.2f} / 5.00" if total_students > 0 else "0.00")
    with kpi3:
        st.metric("Mức độ tự học bình quân", f"Mức {avg_study_hours:.1f} / 5")
    st.markdown("---")

    if total_students == 0:
        st.info("💡 Không có dữ liệu phù hợp với điều kiện bộ lọc hiện tại trên Sidebar. Vui lòng chọn lại!")
        return

    # Khởi tạo mạng lưới ma trận hiển thị 6 biểu đồ phân tích tương quan
    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        st.markdown("<p style='font-weight:bold; color:#2a9d8f;'>📊 Cơ cấu học lực toàn nhóm</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_pie_chart(df_filtered), use_container_width=True)
    with row1_c2:
        st.markdown("<p style='font-weight:bold; color:#2a9d8f;'>📊 Cấu trúc học lực của các giới tính (%)</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_stacked_bar(df_filtered), use_container_width=True)

    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        st.markdown("<p style='font-weight:bold; color:#2a9d8f;'>📈 Biến thiên kết quả học tập qua các năm</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_line_chart(df_filtered), use_container_width=True)
    with row2_c2:
        st.markdown("<p style='font-weight:bold; color:#2a9d8f;'>📊 Tương quan kết quả học tập theo diện chính sách</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_policy_bar(df_filtered), use_container_width=True)

    row3_c1, row3_c2 = st.columns(2)
    with row3_c1:
        st.markdown("<p style='font-weight:bold; color:#2a9d8f;'>🔮 Tương quan Thời gian tự học và Học lực</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_scatter_plot(df_filtered), use_container_width=True)
    with row3_c2:
        st.markdown("<p style='font-weight:bold; color:#2a9d8f;'>🔥 Ma trận mật độ phân hạng học sinh sinh viên</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_density_heatmap(df_filtered), use_container_width=True)
