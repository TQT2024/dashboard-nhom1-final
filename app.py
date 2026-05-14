import streamlit as st
import os
import sys

# Ép hệ thống nhận diện thư mục gốc của dự án để nạp các module con chính xác
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tabs.tab_general import render_tab_general
from tabs.tab_individual import render_tab_individual

# Cấu hình trang bắt buộc phải là lệnh Streamlit đầu tiên
st.set_page_config(
    page_title="Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp")
st.write("---")

# Khởi tạo thanh điều hướng các Tab giao diện theo quy tắc tinh giản
tab1, tab2 = st.tabs(["Tổng quan dữ liệu nhóm", "Hồ sơ cá nhân sinh viên"])

with tab1:
    render_tab_general()

with tab2:
    render_tab_individual()
