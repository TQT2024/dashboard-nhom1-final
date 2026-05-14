import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join("data", "student_data.db")

def get_db_connection():
    """Thiết lập kết nối vật lý an toàn tới SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_general_data():
    """Tải bảng chỉ số tổng quan phục vụ tính toán vĩ mô cho Tab 1."""
    conn = get_db_connection()
    query = "SELECT * FROM vw_dashboard_main"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def load_individual_data():
    """Tải bảng hồ sơ định danh chi tiết phục vụ phân tích vi mô cho Tab 2."""
    conn = get_db_connection()
    query = "SELECT * FROM vw_individual_profile"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
