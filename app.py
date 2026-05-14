import streamlit as st
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from modules.db import load_general_data
from tabs.tab_general import render_tab_general
from tabs.tab_individual import render_tab_individual

st.set_page_config(
    page_title="Dashboard Phân tích Sinh viên",
    layout="wide"
)

# Nạp dữ liệu vào Session State
if 'raw_df' not in st.session_state:
    try:
        st.session_state['raw_df'] = load_general_data()
    except Exception as e:
        st.error(f"Lỗi kết nối cơ sở dữ liệu nền: {e}")
        st.stop()

df = st.session_state['raw_df']

st.sidebar.markdown("### Bộ lọc hệ thống toàn cục")

available_years = sorted(df['year_label'].unique().tolist())
selected_years = st.sidebar.multiselect(
    "1. Tiêu chí năm học:", 
    options=available_years, 
    default=available_years, 
    key="global_years"
)

available_genders = sorted(df['gender_label'].unique().tolist())
selected_genders = st.sidebar.multiselect(
    "2. Tiêu chí giới tính:", 
    options=available_genders, 
    default=available_genders, 
    key="global_genders"
)

# Xử lý Logic Tiêu đề động (Tránh tràn viền khi chọn toàn bộ)
total_y = len(available_years)
total_g = len(available_genders)

if len(selected_years) == total_y and len(selected_genders) == total_g:
    st.session_state['filter_text'] = "(Toàn khóa)"
elif not selected_years or not selected_genders:
    st.session_state['filter_text'] = ""
else:
    y_str = "Tất cả năm" if len(selected_years) == total_y else ", ".join(selected_years)
    g_str = "Tất cả giới" if len(selected_genders) == total_g else ", ".join(selected_genders)
    st.session_state['filter_text'] = f"({y_str} | {g_str})"

# Lọc DataFrame
df_filtered = df.copy()
if selected_years:
    df_filtered = df_filtered[df_filtered['year_label'].isin(selected_years)]
if selected_genders:
    df_filtered = df_filtered[df_filtered['gender_label'].isin(selected_genders)]

st.session_state['filtered_df'] = df_filtered

# Áp dụng nguyên lý "Tiết lộ lũy tiến" để tạo chú giải dưới Sidebar
with st.sidebar.expander("ℹ️ Thang đo cấu hình dữ liệu", expanded=False):
    st.markdown("""
    <div style='font-size: 11px; color: gray; line-height: 1.6;'>
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

st.markdown("<h3 style='text-align: center; color:#2a9d8f; margin-bottom:20px;'>Dashboard phân tích các nhân tố ảnh hưởng đến kết quả học tập</h3>", unsafe_allow_html=True)

tab_options = ["Tổng quan dữ liệu khối", "Hồ sơ cá nhân sinh viên"]
tab1, tab2 = st.tabs(tab_options)

with tab1:
    render_tab_general()

with tab2:
    render_tab_individual()
