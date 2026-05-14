import streamlit as st
import os
import sys

# Ép hệ thống nhận diện thư mục gốc của dự án để nạp các module con chính xác
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tabs.tab_general import render_tab_general
from tabs.tab_individual import render_tab_individual

st.set_page_config(
    page_title="Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp",
    page_icon="🎓",
    layout="wide"
)

# Thu nhỏ font tiêu đề đề tài bằng HTML
st.markdown("<h3 style='margin-bottom:0px; color:#2a9d8f;'>🎓 Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp</h3>", unsafe_allow_html=True)
st.write("---")

# Đồng bộ trạng thái Tab để điều khiển thanh bộ lọc Sidebar động
if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = "Tổng quan dữ liệu nhóm"

# Tạo thanh điều hướng Tab
tab_options = ["Tổng quan dữ liệu nhóm", "Hồ sơ cá nhân sinh viên"]
tab1, tab2 = st.tabs(tab_options)

with tab1:
    # Nếu click vào Tab 1, cập nhật trạng thái để ẩn bộ lọc cá nhân trong Sidebar
    st.session_state['active_tab'] = "Tổng quan dữ liệu nhóm"
    render_tab_general()

with tab2:
    # Nếu click vào Tab 2, kích hoạt trạng thái để hiển thị bộ lọc cá nhân trong Sidebar
    st.session_state['active_tab'] = "Hồ sơ cá nhân sinh viên"
    render_tab_individual()
