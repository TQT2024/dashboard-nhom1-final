import streamlit as st
from modules.database import load_general_data
# Import trực tiếp các module vẽ biểu đồ độc lập từ file mới tách
from modules.charts import draw_pie_chart, draw_stacked_bar, draw_line_chart, draw_scatter_plot, draw_density_heatmap

def render_tab_general():
    df = load_general_data()
    if df.empty:
        st.warning("Hệ thống chưa tải được dữ liệu. Vui lòng kiểm tra kết nối cơ sở dữ liệu.")
        return

    # Khung hộp bộ lọc động trên đầu trang
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_years = st.multiselect("Lọc theo Năm học / Trạng thái:", options=df['year_label'].unique(), default=df['year_label'].unique())
    with col_f2:
        selected_genders = st.multiselect("Lọc theo Giới tính:", options=df['gender_label'].unique(), default=df['gender_label'].unique())

    df_filtered = df[(df['year_label'].isin(selected_years)) & (df['gender_label'].isin(selected_genders))]

    if df_filtered.empty:
        st.warning("Không có dữ liệu phù hợp với tiêu chí bộ lọc đã chọn.")
        return

    st.markdown("### Chỉ số tổng hợp toàn nhóm")
    total_students = len(df_filtered)
    avg_gpa_raw = df_filtered['gpa_raw'].mean()
    ratio_good = (len(df_filtered[df_filtered['gpa_raw'] >= 4]) / total_students) * 100 if total_students > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng số sinh viên (n)", f"{total_students} SV")
    col2.metric("GPA Trung bình (Thang 5)", f"{avg_gpa_raw:.2f} / 5.00")
    col3.metric("Tỷ lệ Học lực Khá/Giỏi trở lên", f"{ratio_good:.1f}%")

    st.markdown("---")

    # ==============================================================================
    # BỐ CỤC 3 HÀNG DỌC - MỖI HÀNG ĐỐI CHIẾU SONG SONG 2 BIỂU ĐỒ THEO TIÊU CHÍ CỦA CÔ
    # ==============================================================================
    
    # Hàng mốc 1: Cấu phần tổng quan
    st.markdown("#### 1. Thống kê tỷ trọng cấu phần học lực")
    c1_h1, c2_h1 = st.columns([1, 1.2]) # Chia tỷ lệ cột cho biểu đồ tròn cân đối
    with c1_h1:
        st.markdown("<p style='text-align: center; color:gray;'><b>Tỷ trọng cơ cấu học lực toàn khóa</b> (Pie Chart)</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_pie_chart(df_filtered), width='stretch')
    with c2_h1:
        st.markdown("<p style='text-align: center; color:gray;'><b>Phân phối học lực theo Giới tính</b> (Stacked Bar Chart)</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_stacked_bar(df_filtered), width='stretch')

    st.markdown("---")
    
    # Hàng mốc 2: Tiến trình xu hướng học tập
    st.markdown("#### 2. Phân tích tiến trình và xu hướng biến thiên")
    st.markdown("<p style='color:gray;'><b>Xu hướng biến động của kết quả điểm GPA trung bình qua các năm học chuyên ngành</b> (Line Graph)</p>", unsafe_allow_html=True)
    st.plotly_chart(draw_line_chart(df_filtered), width='stretch')

    st.markdown("---")
    
    # Hàng mốc 3: Giải mã tương quan
    st.markdown("#### 3. Đối chiếu ma trận mật độ và tương quan học thuật")
    c1_h3, c2_h3 = st.columns(2)
    with c1_h3:
        st.markdown("<p style='text-align: center; color:gray;'><b>Tương quan Thời gian tự học và Điểm số</b> (Scatter Plot với Size Mapping)</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_scatter_plot(df_filtered), width='stretch')
    with c2_h3:
        st.markdown("<p style='text-align: center; color:gray;'><b>Ma trận mật độ phân hạng sinh viên</b> (Density Heatmap nâng cao)</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_density_heatmap(df_filtered), width='stretch')
