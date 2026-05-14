import streamlit as st
from modules.database import load_general_data
# ĐÃ ĐỒNG BỘ: Gọi chuẩn xác từ module charts gốc cho Tab General
from modules.charts import draw_pie_chart, draw_stacked_bar, draw_line_chart, draw_policy_bar, draw_scatter_plot, draw_density_heatmap

def render_tab_general():
    df = load_general_data()
    if df.empty:
        st.warning("Hệ thống chưa tải được dữ liệu. Vui lòng kiểm tra kết nối cơ sở dữ liệu.")
        return

    st.markdown("""
        <style>
        .stMetric {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 10px;
            border: 1px solid #eef0f2;
        }
        </style>
    """, unsafe_allow_html=True)

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_years = st.multiselect("Lọc theo Năm học / Trạng thái:", options=df['year_label'].unique(), default=df['year_label'].unique())
    with col_f2:
        selected_genders = st.multiselect("Lọc theo Giới tính:", options=df['gender_label'].unique(), default=df['gender_label'].unique())

    df_filtered = df[(df['year_label'].isin(selected_years)) & (df['gender_label'].isin(selected_genders))]

    if df_filtered.empty:
        st.warning("Không có dữ liệu phù hợp với tiêu chí bộ lọc đã chọn.")
        return

    if len(selected_genders) == 0 or len(selected_genders) == len(df['gender_label'].unique()):
        gender_title_text = "Toàn khối"
    else:
        gender_title_text = f"Sinh viên " + ", ".join(selected_genders)

    if len(selected_years) == 0 or len(selected_years) == len(df['year_label'].unique()):
        year_title_text = "các giai đoạn năm học chuyên ngành"
    else:
        year_title_text = "giai đoạn " + ", ".join(selected_years)

    st.markdown(f"<h5 style='color:#2a9d8f; margin-top:10px;'>📊 Kết quả phân tích tổng quan nhóm {gender_title_text} ({year_title_text})</h5>", unsafe_allow_html=True)
    st.write("")

    if len(selected_genders) == 1:
        c1_h1, c2_h1 = st.columns([1, 2.5])
        with c1_h1:
            st.markdown("<br>", unsafe_allow_html=True)
            total_students = len(df_filtered)
            avg_gpa_raw = df_filtered['gpa_raw'].mean()
            ratio_good = (len(df_filtered[df_filtered['gpa_raw'] >= 4]) / total_students) * 100 if total_students > 0 else 0
            
            st.metric("Tổng mẫu khảo sát (n)", f"{total_students} SV")
            st.metric("GPA trung bình toàn nhóm", f"{avg_gpa_raw:.2f} / 5.00")
            st.metric("Tỷ lệ học lực Khá trở lên", f"{ratio_good:.1f}%")
        with c2_h1:
            st.markdown(f"<p style='text-align: center; font-size:12px; font-weight: bold; margin-bottom:5px; color:#444;'>Cơ cấu xếp loại học lực nhóm nghiên cứu</p>", unsafe_allow_html=True)
            st.plotly_chart(draw_pie_chart(df_filtered), width='stretch', config={'displayModeBar': False})
    else:
        c1_h1, c2_h1, c3_h1 = st.columns([1, 1.3, 1.4])
        with c1_h1:
            st.markdown("<br>", unsafe_allow_html=True)
            total_students = len(df_filtered)
            avg_gpa_raw = df_filtered['gpa_raw'].mean()
            ratio_good = (len(df_filtered[df_filtered['gpa_raw'] >= 4]) / total_students) * 100 if total_students > 0 else 0
            
            st.metric("Tổng mẫu khảo sát (n)", f"{total_students} SV")
            st.metric("GPA trung bình toàn nhóm", f"{avg_gpa_raw:.2f} / 5.00")
            st.metric("Tỷ lệ học lực Khá trở lên", f"{ratio_good:.1f}%")
        with c2_h1:
            st.markdown("<p style='text-align: center; font-size:12px; font-weight: bold; margin-bottom:5px; color:#444;'>Cơ cấu học lực toàn nhóm</p>", unsafe_allow_html=True)
            st.plotly_chart(draw_pie_chart(df_filtered), width='stretch', config={'displayModeBar': False})
        with c3_h1:
            clean_label = gender_title_text.lower() if "Sinh viên" in gender_title_text else "các giới tính"
            bar_label = f"Cấu trúc học lực của {clean_label}"
            st.markdown(f"<p style='text-align: center; font-size:12px; font-weight: bold; margin-bottom:5px; color:#444;'>{bar_label}</p>", unsafe_allow_html=True)
            st.plotly_chart(draw_stacked_bar(df_filtered), width='stretch', config={'displayModeBar': False})

    st.markdown("<div style='margin-top:-10px; margin-bottom:15px;'><hr style='margin:0; border-top: 1px solid #e2e8f0;'/></div>", unsafe_allow_html=True)

    c1_h2, c2_h2, c3_h2 = st.columns(3)
    
    with c1_h2:
        if len(df_filtered['year_label'].unique()) == 1:
            st.markdown("<p style='text-align: center; font-size:12px; font-weight: bold; margin-bottom:5px; color:#444;'>Hiệu suất điểm theo Diện chính sách</p>", unsafe_allow_html=True)
            st.plotly_chart(draw_policy_bar(df_filtered), width='stretch', config={'displayModeBar': False})
        else:
            st.markdown("<p style='text-align: center; font-size:12px; font-weight: bold; margin-bottom:5px; color:#444;'>Biến thiên kết quả học tập qua các năm</p>", unsafe_allow_html=True)
            st.plotly_chart(draw_line_chart(df_filtered), width='stretch', config={'displayModeBar': False})
            
    with c2_h2:
        st.markdown("<p style='text-align: center; font-size:12px; font-weight: bold; margin-bottom:5px; color:#444;'>Tương quan Thời gian học và Học lực</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_scatter_plot(df_filtered), width='stretch', config={'displayModeBar': False})
        
    with c3_h2:
        st.markdown("<p style='text-align: center; font-size:12px; font-weight: bold; margin-bottom:5px; color:#444;'>Ma trận mật độ phân hạng sinh viên</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_density_heatmap(df_filtered), width='stretch', config={'displayModeBar': False})
