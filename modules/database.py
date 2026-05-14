import sqlite3
import pandas as pd
import streamlit as st
import os

# Định vị đường dẫn tương đối đến file database
# Đảm bảo file database.py nằm trong thư mục modules/ và student_data.db nằm trong thư mục data/
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "student_data.db")

@st.cache_data(ttl=3600)  # TTL=3600: Cache sẽ tự động làm mới sau 1 giờ (phục vụ tốt nếu có cập nhật CSDL)
def load_general_data():
    """Truy xuất dữ liệu tổng quan cho Tab 1 từ View vw_dashboard_main"""
    try:
        # Sử dụng 'with' để đảm bảo kết nối tự động đóng sau khi query xong
        with sqlite3.connect(DB_PATH) as conn:
            query = "SELECT * FROM vw_dashboard_main"
            df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"Lỗi kết nối CSDL (Tab Tổng quan): {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_individual_data():
    """Truy xuất dữ liệu chi tiết hồ sơ cá nhân cho Tab 2 từ View vw_individual_profile"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = "SELECT * FROM vw_individual_profile"
            df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"Lỗi kết nối CSDL (Tab Cá nhân): {e}")
        return pd.DataFrame()