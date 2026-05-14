import streamlit as st
import os
import sys

# Khởi tạo đường dẫn hệ thống để nhận diện module cục bộ
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from modules.db import load_general_data
from tabs.tab_general import render_tab_general
from tabs.tab_individual import render_tab_individual

st.set_page_config(
    page_title="Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp",
    page_icon="🎓", layout="wide"
)

# 1. Khởi tạo và nạp dữ liệu gốc vào bộ nhớ Session State để tối ưu hiệu năng
if 'raw_df' not in st.session_state:
    try:
        st.session_state['raw_df'] = load_general_data()
    except Exception as e:
        st.error(f"Lỗi kết nối cơ sở dữ liệu nền: {e}")
        st.stop()

df = st.session_state['raw_df']

# 2. Xây dựng khu vực bộ lọc vĩ mô tập trung trên thanh Sidebar
st.sidebar.markdown("### 🔍 Bộ lọc hệ thống toàn cục")

# Bộ lọc đa chọn cho Năm học / Trạng thái tốt nghiệp
available_years = sorted(df['year_label'].unique().tolist())
selected_years = st.sidebar.multiselect(
    "1. Chọn Năm học / Trạng thái:", 
    options=available_years, 
    default=available_years, 
    key="global_years"
)

# Bộ lọc đa chọn cho Giới tính sinh viên
available_genders = sorted(df['gender_label'].unique().tolist())
selected_genders = st.sidebar.multiselect(
    "2. Chọn Giới tính:", 
    options=available_genders, 
    default=available_genders, 
    key="global_genders"
)

# 3. Xử lý cắt lọc dữ liệu động dựa trên cấu hình Sidebar
df_filtered = df.copy()
if selected_years:
    df_filtered = df_filtered[df_filtered['year_label'].isin(selected_years)]
if selected_genders:
    df_filtered = df_filtered[df_filtered['gender_label'].isin(selected_genders)]

# Lưu trữ tập dữ liệu sau lọc vào Session State để các tab nội bộ truy xuất đồng bộ
st.session_state['filtered_df'] = df_filtered

# 4. Thiết lập kiến trúc Tabs giao diện chính
tab_options = ["Tổng quan dữ liệu nhóm", "Hồ sơ cá nhân sinh viên"]
tab1, tab2 = st.tabs(tab_options)

with tab1:
    st.markdown("<h3 style='text-align: center; color:#2a9d8f; margin-bottom:20px;'>🎓 Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp</h3>", unsafe_allow_html=True)
    render_tab_general()

with tab2:
    st.markdown("<h3 style='text-align: center; color:#2a9d8f; margin-bottom:20px;'>🎓 Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp</h3>", unsafe_allow_html=True)
    render_tab_individual()
