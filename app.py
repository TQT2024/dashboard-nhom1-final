import streamlit as st
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from modules.db import load_general_data
from tabs.tab_general import render_tab_general
from tabs.tab_individual import render_tab_individual

st.set_page_config(
    page_title="Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành",
    layout="wide"
)

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

df_filtered = df.copy()
if selected_years:
    df_filtered = df_filtered[df_filtered['year_label'].isin(selected_years)]
if selected_genders:
    df_filtered = df_filtered[df_filtered['gender_label'].isin(selected_genders)]

st.session_state['filtered_df'] = df_filtered

st.markdown("<h3 style='text-align: center; color:#2a9d8f; margin-bottom:20px;'>HỆ THỐNG TRỰC QUAN HÓA: CÁC NHÂN TỐ ẢNH HƯỞNG ĐẾN KẾT QUẢ HỌC TẬP</h3>", unsafe_allow_html=True)

tab_options = ["Tổng quan dữ liệu khối", "Hồ sơ cá nhân sinh viên"]
tab1, tab2 = st.tabs(tab_options)

with tab1:
    render_tab_general()

with tab2:
    render_tab_individual()
