import streamlit as st
import plotly.express as px
import pandas as pd
from modules.database import load_general_data

def render_tab_general():
    df = load_general_data()
    if df.empty:
        st.warning("Hệ thống chưa tải được dữ liệu. Vui lòng kiểm tra kết nối cơ sở dữ liệu.")
        return

    st.markdown("### Chỉ số Tổng hợp Giai đoạn Chuyên sâu (KPIs)")
    
    total_students = len(df)
    avg_gpa_raw = df['gpa_raw'].mean()
    ratio_good = (len(df[df['gpa_raw'] >= 4]) / total_students) * 100 if total_students > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng số sinh viên (n)", f"{total_students} SV")
    col2.metric("GPA Trung bình (Thang 5)", f"{avg_gpa_raw:.2f} / 5.00")
    col3.metric("Tỷ lệ Học lực Khá/Giỏi trở lên", f"{ratio_good:.1f}%")

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**So sánh Cấu trúc Học lực theo Giới tính (Hóa giải mẫu lệch 1:9)**")
        
        gpa_map = {1: "Yếu (<2.0)", 2: "Trung bình (2.0-2.5)", 3: "Khá (2.5-3.2)", 4: "Giỏi (3.2-3.6)", 5: "Xuất sắc (>3.6)"}
        df['Học lực'] = df['gpa_raw'].map(gpa_map)
        gpa_order = ["Yếu (<2.0)", "Trung bình (2.0-2.5)", "Khá (2.5-3.2)", "Giỏi (3.2-3.6)", "Xuất sắc (>3.6)"]

        df_gender_gpa = df.groupby(['gender_label', 'Học lực']).size().reset_index(name='Số lượng')
        
        fig_bar = px.bar(
            df_gender_gpa, 
            y="gender_label", 
            x="Số lượng", 
            color="Học lực", 
            orientation="h",
            text_auto='.1f',
            category_orders={"Học lực": gpa_order},
            color_discrete_sequence=px.colors.sequential.Blues_r,
            labels={"gender_label": "Giới tính", "Số lượng": "Tỷ trọng (%)"}
        )
        fig_bar.update_layout(
            barmode='stack',
            barnorm='percent',
            xaxis_title="Tỷ lệ phần trăm (%)", 
            yaxis_title=None, 
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.markdown("**Ma trận Mật độ: Mối tương quan hành vi tự học và Học lực**")
        
        time_study_map = {1: "Dưới 2 giờ", 2: "2 - dưới 4 giờ", 3: "4 - dưới 6 giờ", 4: "6 - dưới 8 giờ", 5: "Trên 8 giờ"}
        df['Thời gian tự học'] = df['time_studying'].map(time_study_map)
        study_order = ["Dưới 2 giờ", "2 - dưới 4 giờ", "4 - dưới 6 giờ", "6 - dưới 8 giờ", "Trên 8 giờ"]

        fig_heat = px.density_heatmap(
            df, 
            x="Thời gian tự học", 
            y="Học lực", 
            category_orders={"Thời gian tự học": study_order, "Học lực": gpa_order},
            text_auto=True,
            color_continuous_scale="Blues",
            labels={"Thời gian tự học": "Thời gian tự học trong ngày", "Học lực": "Phân hạng học lực"}
        )
        fig_heat.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_heat, use_container_width=True)
