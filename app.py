import streamlit as st
from tabs.tab_general import render_tab_general
from tabs.tab_individual import render_tab_individual

# 1. Cấu hình trang (Lệnh này bắt buộc phải là lệnh Streamlit đầu tiên trong file)
st.set_page_config(
    page_title="Dashboard Phân tích Học tập",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Tiêu đề hệ thống
st.markdown("<h1 style='text-align: center; color: #1a5276;'>Hệ thống Phân tích Yếu tố Ảnh hưởng đến Kết quả Học tập</h1>", unsafe_allow_html=True)
st.markdown("---")

# 3. Khởi tạo cấu trúc Tab
tab1, tab2 = st.tabs(["📈 Phân tích Tổng quan", "👤 Hồ sơ Cá nhân & Khuyến nghị (AI)"])

# 4. Điều hướng và gọi Module giao diện
with tab1:
    render_tab_general()

with tab2:
    render_tab_individual()