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

# Đồng bộ trạng thái Tab để điều khiển thanh bộ lọc Sidebar động
if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = "Tổng quan dữ liệu nhóm"

# Tạo thanh điều hướng Tab tinh giản
tab_options = ["Tổng quan dữ liệu nhóm", "Hồ sơ cá nhân sinh viên"]
tab1, tab2 = st.tabs(tab_options)

with tab1:
    st.session_state['active_tab'] = "Tổng quan dữ liệu nhóm"
    # ĐƯA TIÊU ĐỀ CANH GIỮA VÀO TRONG TAB 1
    st.markdown("<h3 style='text-align: center; color:#2a9d8f; margin-bottom:20px;'>🎓 Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp</h3>", unsafe_allow_html=True)
    render_tab_general()

with tab2:
    st.session_state['active_tab'] = "Hồ sơ cá nhân sinh viên"
    # ĐƯA TIÊU ĐỀ CANH GIỮA VÀO TRONG TAB 2 (Giải quyết lỗi mất tên dashboard)
    st.markdown("<h3 style='text-align: center; color:#2a9d8f; margin-bottom:20px;'>🎓 Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp</h3>", unsafe_allow_html=True)
    render_tab_individual()
