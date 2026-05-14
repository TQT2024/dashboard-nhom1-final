import streamlit as st
from modules.database import load_general_data
from modules.charts import draw_pie_chart, draw_stacked_bar, draw_line_chart, draw_scatter_plot, draw_density_heatmap

def render_tab_general():
    df = load_general_data()
    if df.empty:
        st.warning("Hệ thống chưa tải được dữ liệu. Vui lòng kiểm tra kết nối cơ sở dữ liệu.")
        return

    # Bộ lọc động trên đầu trang
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_years = st.multiselect("Lọc theo Năm học / Trạng thái:", options=df['year_label'].unique(), default=df['year_label'].unique())
    with col_f2:
        selected_genders = st.multiselect("Lọc theo Giới tính:", options=df['gender_label'].unique(), default=df['gender_label'].unique())

    df_filtered = df[(df['year_label'].isin(selected_years)) & (df['gender_label'].isin(selected_genders))]

    if df_filtered.empty:
        st.warning("Không có dữ liệu phù hợp với tiêu chí bộ lọc đã chọn.")
        return

    # ==============================================================================
    # XỬ LÝ LOGIC TIÊU ĐỀ ĐỘNG (DYNAMIC TEXT GRAPH LABELS) ĐẠT CHUẨN BI
    # ==============================================================================
    # 1. Xác định ngữ cảnh giới tính
    if len(selected_genders) == 1:
        gender_title_text = f"sinh viên {selected_genders[0]}"
    else:
        gender_title_text = "toàn khối"

    # 2. Xác định ngữ cảnh thời gian năm học
    if len(selected_years) == 1:
        year_title_text = f"giai đoạn {selected_years[0]}"
    elif len(selected_years) == 0 or len(selected_years) == len(df['year_label'].unique()):
        year_title_text = "các năm chuyên ngành"
    else:
        year_title_text = "các giai đoạn đã chọn"

    # Gộp chuỗi text động nạp thẳng vào tiêu đề giao diện st.markdown
    st.markdown(f"### Chỉ số tổng hợp nhóm {gender_title_text} ({year_title_text})")
    
    total_students = len(df_filtered)
    avg_gpa_raw = df_filtered['gpa_raw'].mean()
    ratio_good = (len(df_filtered[df_filtered['gpa_raw'] >= 4]) / total_students) * 100 if total_students > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng số sinh viên (n)", f"{total_students} SV")
    col2.metric("GPA Trung bình (Thang 5)", f"{avg_gpa_raw:.2f} / 5.00")
    col3.metric("Tỷ lệ Học lực Khá/Giỏi trở lên", f"{ratio_good:.1f}%")

    st.markdown("---")

    # Bố cục 3 hàng dọc đối chiếu song song biểu đồ
    st.markdown("#### 1. Thống kê tỷ trọng cấu phần học lực")
    c1_h1, c2_h1 = st.columns([1, 1.2])
    with c1_h1:
        st.markdown(f"<p style='text-align: center; color:gray;'><b>Tỷ trọng cơ cấu học lực {gender_title_text}</b> (Pie Chart)</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_pie_chart(df_filtered), width='stretch')
    with c2_h1:
        # Nhãn biểu đồ Bar tự động đổi tên theo ngữ cảnh
        bar_label = f"Phân phối học lực {gender_title_text}" if len(selected_genders) == 1 else "Phân phối học lực theo Giới tính"
        st.markdown(f"<p style='text-align: center; color:gray;'><b>{bar_label}</b> (Bar Chart)</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_stacked_bar(df_filtered), width='stretch')

    st.markdown("---")
    
    st.markdown("#### 2. Phân tích tiến trình và xu hướng biến thiên")
    st.markdown(f"<p style='color:gray;'><b>Xu hướng biến động kết quả GPA bình quân của nhóm {gender_title_text} qua các giai đoạn</b> (Line Graph)</p>", unsafe_allow_html=True)
    st.plotly_chart(draw_line_chart(df_filtered), width='stretch')

    st.markdown("---")
    
    st.markdown("#### 3. Đối chiếu ma trận mật độ và tương quan học thuật")
    c1_h3, c2_h3 = st.columns(2)
    with c1_h3:
        st.markdown(f"<p style='text-align: center; color:gray;'><b>Tương quan Thời gian học và Điểm số nhóm {gender_title_text}</b> (Scatter Plot)</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_scatter_plot(df_filtered), width='stretch')
    with c2_h3:
        st.markdown(f"<p style='text-align: center; color:gray;'><b>Ma trận mật độ phân hạng của nhóm {gender_title_text}</b> (Density Heatmap)</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_density_heatmap(df_filtered), width='stretch')
