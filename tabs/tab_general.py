import streamlit as st
import plotly.express as px
import pandas as pd
from modules.database import load_general_data

def render_tab_general():
    df = load_general_data()
    if df.empty:
        st.warning("Hệ thống chưa tải được dữ liệu. Vui lòng kiểm tra kết nối cơ sở dữ liệu.")
        return

    st.markdown("### Chỉ số Tổng hợp (KPIs)")
    
    # Tính toán KPI
    total_students = len(df)
    avg_gpa = df['gpa'].mean()
    # Tính tỷ lệ sinh viên đạt GPA Khá, Giỏi (mức 4 và 5)
    ratio_good = (len(df[df['gpa'] >= 4]) / total_students) * 100 if total_students > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng số sinh viên (n)", total_students)
    col2.metric("GPA Trung bình (Thang 5)", f"{avg_gpa:.2f}")
    col3.metric("Tỷ lệ Học lực Khá/Giỏi (%)", f"{ratio_good:.1f}%")

    st.markdown("---")

    # Bố cục 2 biểu đồ
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**So sánh Cấu trúc Học lực theo Giới tính**")
        # Phân nhóm và tính tần suất để vẽ biểu đồ Stacked Bar
        df_gender_gpa = df.groupby(['gender_label', 'gpa']).size().reset_index(name='count')
        df_gender_gpa['gpa'] = df_gender_gpa['gpa'].astype(str) # Ép kiểu chuỗi để Plotly nhận diện biến phân loại
        
        fig_bar = px.bar(
            df_gender_gpa, 
            y="gender_label", 
            x="count", 
            color="gpa", 
            orientation="h",
            barnorm="percent", 
            text_auto='.1f',
            color_discrete_sequence=px.colors.sequential.Blues,
            labels={"gender_label": "Giới tính", "count": "Tỷ trọng (%)", "gpa": "Mức GPA"}
        )
        # Ẩn tiêu đề trục X để giao diện gọn hơn
        fig_bar.update_layout(xaxis_title=None, yaxis_title=None, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.markdown("**Ma trận Mật độ: Thời gian Tự học và Điểm số**")
        # Sử dụng Density Heatmap khắc phục Overplotting của Scatter Plot
        fig_heat = px.density_heatmap(
            df, 
            x="time_studying", 
            y="gpa", 
            text_auto=True,
            color_continuous_scale="Blues",
            labels={"time_studying": "Mức Thời gian Tự học (1-5)", "gpa": "Mức GPA (1-5)"}
        )
        fig_heat.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_heat, use_container_width=True)