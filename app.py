import streamlit as st
import os
import sys

# Ép hệ thống nhận diện thư mục gốc của dự án để nạp các module con chính xác
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tabs.tab_general import render_tab_general
from tabs.tab_individual import render_tab_individual

# Cấu hình trang bắt buộc phải là lệnh Streamlit đầu tiên
st.set_page_config(
    page_title="Hệ Thống Giám Sát Sinh Viên AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 HỆ THỐNG GIÁM SÁT VÀ HỖ TRỢ RA QUYẾT ĐỊNH SINH VIÊN")
st.markdown("*Kiến trúc Modular Dashboard tích hợp Hệ cố vấn AI cá nhân hóa*")
st.write("---")

# Khởi tạo thanh điều hướng các Tab giao diện
tab1, tab2 = st.tabs(["📊 Phân Tích Nhóm (General)", "🔍 Tra Cứu Cá Nhân (Individual Drill-down)"])

with tab1:
    render_tab_general()

with tab2:
    render_tab_individual()
