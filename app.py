import streamlit as st
import os
import sys

# Ép hệ thống nhận diện thư mục gốc của dự án
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tabs.tab_general import render_tab_general
from tabs.tab_individual import render_tab_individual

st.set_page_config(
    page_title="Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp",
    page_icon="🎓",
    layout="wide"
)

# THU NHỎ FONT TIÊU ĐỀ ĐỀ TÀI XUỐNG CỠ CHỮ H3 BẰNG HTML ĐỂ KHÔNG BỊ QUÁ BỰ
st.markdown("<h3 style='margin-bottom:0px; color:#2a9d8f;'>🎓 Phân tích các nhân tố ảnh hưởng đến sinh viên chuyên ngành và sau tốt nghiệp</h3>", unsafe_allow_html=True)
st.write("---")

tab1, tab2 = st.tabs(["Tổng quan dữ liệu nhóm", "Hồ sơ cá nhân sinh viên"])

with tab1:
    render_tab_general()

with tab2:
    render_tab_individual()
