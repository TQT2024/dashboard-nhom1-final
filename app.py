import streamlit as st
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from modules.db import load_general_data
from tabs.tab_general import render_tab_general
from tabs.tab_individual import render_tab_individual

st.set_page_config(page_title="Dashboard Phân tích Sinh viên", layout="wide")

if 'raw_df' not in st.session_state:
    try:
        st.session_state['raw_df'] = load_general_data()
    except Exception as e:
        st.error(f"Lỗi truy xuất CSDL: {e}")
        st.stop()

df = st.session_state['raw_df']

st.sidebar.markdown("### Bộ lọc hệ thống")
available_years = sorted(df['year_label'].unique().tolist())
selected_years = st.sidebar.multiselect("Năm học:", options=available_years, default=available_years)

available_genders = sorted(df['gender_label'].unique().tolist())
selected_genders = st.sidebar.multiselect("Giới tính:", options=available_genders, default=available_genders)

# Xử lý chuỗi tiêu đề động
if len(selected_years) == len(available_years) and len(selected_genders) == len(available_genders):
    filter_suffix = "(Toàn khóa)"
elif not selected_years or not selected_genders:
    filter_suffix = ""
else:
    y_str = "Tất cả năm" if len(selected_years) == len(available_years) else ", ".join(selected_years)
    g_str = "Tất cả giới" if len(selected_genders) == len(available_genders) else ", ".join(selected_genders)
    filter_suffix = f"(Tệp: {g_str} | {y_str})"

st.session_state['filter_suffix'] = filter_suffix

df_filtered = df.copy()
if selected_years:
    df_filtered = df_filtered[df_filtered['year_label'].isin(selected_years)]
if selected_genders:
    df_filtered = df_filtered[df_filtered['gender_label'].isin(selected_genders)]
st.session_state['filtered_df'] = df_filtered

with st.sidebar.expander("ℹ️ Thang đo cấu hình dữ liệu", expanded=False):
    st.markdown("""
    <div style='font-size: 11px; color: gray;'>
    <b>Thang phân loại GPA:</b><br>
    • [1.0 - 2.0): Yếu<br>
    • [2.0 - 2.5): Trung bình<br>
    • [2.5 - 3.2): Khá<br>
    • [3.2 - 3.6): Giỏi<br>
    • [3.6 - 5.0]: Xuất sắc<br><br>
    <b>Thang thời gian tự học:</b><br>
    • [1.0 - 1.5): Dưới 2 giờ<br>
    • [1.5 - 2.5): 2 - dưới 4 giờ<br>
    • [2.5 - 3.5): 4 - dưới 6 giờ<br>
    • [3.5 - 4.5): 6 - dưới 8 giờ<br>
    • [4.5 - 5.0]: Trên 8 giờ
    </div>
    """, unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color:#2a9d8f; margin-bottom:15px;'>Dashboard Phân Tích Các Nhân Tố Ảnh Hưởng Đến Kết Quả Học Tập</h3>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Tổng quan dữ liệu khối", "Hồ sơ cá nhân sinh viên"])
with tab1: render_tab_general()
with tab2: render_tab_individual()
