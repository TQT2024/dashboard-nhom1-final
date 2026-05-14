import streamlit as st
import os
import sys

# Khởi tạo đường dẫn hệ thống
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from modules.db import load_general_data
from tabs.tab_general import render_tab_general
from tabs.tab_individual import render_tab_individual

st.set_page_config(
    page_title="Dashboard Phân tích Sinh viên",
    page_icon="🎓",
    layout="wide"
)

# Nạp dữ liệu gốc (Cache 1 giờ)
if 'raw_df' not in st.session_state:
    try:
        st.session_state['raw_df'] = load_general_data()
    except Exception as e:
        st.error(f"Lỗi truy xuất CSDL: {e}")
        st.stop()

df = st.session_state['raw_df']

# --- SIDEBAR BỘ LỌC ---
st.sidebar.header("🔍 BỘ LỌC HỆ THỐNG")
available_years = sorted(df['year_label'].unique().tolist())
selected_years = st.sidebar.multiselect("Giai đoạn học tập:", options=available_years, default=available_years)

available_genders = sorted(df['gender_label'].unique().tolist())
selected_genders = st.sidebar.multiselect("Giới tính sinh viên:", options=available_genders, default=available_genders)

# Xử lý Logic Tiêu đề động
total_y, total_g = len(available_years), len(available_genders)
if len(selected_years) == total_y and len(selected_genders) == total_g:
    filter_suffix = "(Toàn khóa)"
elif not selected_years or not selected_genders:
    filter_suffix = "(Chưa chọn dữ liệu)"
else:
    y_text = "Tất cả năm" if len(selected_years) == total_y else ", ".join(selected_years)
    g_text = "Tất cả giới" if len(selected_genders) == total_g else ", ".join(selected_genders)
    filter_suffix = f"(Nhóm: {g_text} | {y_text})"

st.session_state['filter_suffix'] = filter_suffix

# Thực hiện lọc dữ liệu
df_filtered = df.copy()
if selected_years:
    df_filtered = df_filtered[df_filtered['year_label'].isin(selected_years)]
if selected_genders:
    df_filtered = df_filtered[df_filtered['gender_label'].isin(selected_genders)]
st.session_state['filtered_df'] = df_filtered

# Chú thích thang đo (Ẩn hiện thông minh)
with st.sidebar.expander("ℹ️ THÔNG TIN THANG ĐO", expanded=False):
    st.caption("Dữ liệu được chuẩn hóa thang 100 từ khảo sát Likert 1-5.")

# --- GIAO DIỆN CHÍNH ---
st.markdown(f"<h2 style='text-align: center; color:#2a9d8f;'>PHÂN TÍCH CÁC NHÂN TỐ ẢNH HƯỞNG ĐẾN KẾT QUẢ HỌC TẬP</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color:gray; font-size:14px;'>Đồ án cuối kỳ - {filter_suffix}</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 PHÂN TÍCH TỔNG QUAN", "👤 HỒ SƠ & TRỢ LÝ AI"])

with tab1:
    render_tab_general()

with tab2:
    render_tab_individual()
