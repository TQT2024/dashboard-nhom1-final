import streamlit as st
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tabs.tab_general import render_tab_general
from tabs.tab_individual import render_tab_individual

st.set_page_config(
    page_title="Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp",
    page_icon="🎓", layout="wide"
)

# Khởi tạo trạng thái tab nếu chưa có
if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = "Tổng quan dữ liệu nhóm"

tab_options = ["Tổng quan dữ liệu nhóm", "Hồ sơ cá nhân sinh viên"]
tab1, tab2 = st.tabs(tab_options)

with tab1:
    st.session_state['active_tab'] = "Tổng quan dữ liệu nhóm"
    st.markdown("<h3 style='text-align: center; color:#2a9d8f; margin-bottom:20px;'>🎓 Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp</h3>", unsafe_allow_html=True)
    render_tab_general()

with tab2:
    st.session_state['active_tab'] = "Hồ sơ cá nhân sinh viên"
    st.markdown("<h3 style='text-align: center; color:#2a9d8f; margin-bottom:20px;'>🎓 Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp</h3>", unsafe_allow_html=True)
    render_tab_individual()
