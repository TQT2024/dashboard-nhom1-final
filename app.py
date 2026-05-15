import streamlit as st
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from modules.db import load_general_data
from tabs.tab_general import render_tab_general
from tabs.tab_individual import render_tab_individual

st.set_page_config(
    page_title="Dashboard phân tích các yếu tố ảnh hưởng đến GPA của sinh viên",
    layout="wide"
)

if 'raw_df' not in st.session_state:
    try:
        st.session_state['raw_df'] = load_general_data()
    except Exception as e:
        st.error(f"Lỗi truy xuất hệ thống dữ liệu: {e}")
        st.stop()

df = st.session_state['raw_df']

st.sidebar.markdown("<p style='font-size:16px; font-weight:bold; color:#222; margin-bottom:5px;'>Bộ lọc dữ liệu</p>", unsafe_allow_html=True)

available_years = sorted(df['year_label'].unique().tolist())
# ĐỒNG BỘ: Khóa cứng key toàn cục global_years
selected_years = st.sidebar.multiselect("Niên khóa:", options=available_years, default=available_years, key="global_years")

available_genders = sorted(df['gender_label'].unique().tolist())
# ĐỒNG BỘ: Khóa cứng key toàn cục global_genders
selected_genders = st.sidebar.multiselect("Giới tính:", options=available_genders, default=available_genders, key="global_genders")

df_filtered = df.copy()
# SỬA LỖI: Tránh rỗng dữ liệu khi xóa sạch bộ lọc, mặc định lấy toàn bộ dải mẫu
if selected_years:
    df_filtered = df_filtered[df_filtered['year_label'].isin(selected_years)]
if selected_genders:
    df_filtered = df_filtered[df_filtered['gender_label'].isin(selected_genders)]
st.session_state['filtered_df'] = df_filtered

total_y, total_g = len(available_years), len(available_genders)
if len(selected_years) == total_y and len(selected_genders) == total_g:
    filter_suffix = "(Toàn khóa)"
elif not selected_years or not selected_genders:
    filter_suffix = "(Chưa chọn dữ liệu)"
else:
    y_text = "Tất cả năm" if len(selected_years) == total_y else "+".join(selected_years)
    g_text = "Tất cả giới" if len(selected_genders) == total_g else "+".join(selected_genders)
    filter_suffix = f"({g_text} | {y_text})"

st.session_state['filter_suffix'] = filter_suffix

with st.sidebar.expander("Thang đo và Phương pháp chuẩn hóa", expanded=False):
    st.markdown("""
    **Phương pháp:** Chuyển đổi tuyến tính từ thang đo khảo sát Likert (1-5) sang thang điểm 100 hệ thống.

    
    | Khảo sát | Hệ 100 | Ý nghĩa định tính |
    | :---: | :---: | :--- |
    | 1 | 20 | Rất thấp / Rất kém |
    | 2 | 40 | Thấp / Kém |
    | 3 | 60 | Trung bình / Bình thường |
    | 4 | 80 | Cao / Tốt |
    | 5 | 100 | Rất cao / Rất tốt |
    
    **Công thức:** $X_{scaled} = X_{likert} \\times 20$
    """)

st.markdown(f"<h2 style='text-align: center; color:#2a9d8f; font-weight: bold; margin-bottom: 25px;'>Dashboard phân tích các yếu tố ảnh hưởng đến GPA của sinh viên</h2>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Phân tích tổng quan nhóm", "Tra cứu hồ sơ cá nhân"])

with tab1:
    render_tab_general()

with tab2:
    render_tab_individual()
