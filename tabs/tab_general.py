import streamlit as st
import plotly.express as px
import pandas as pd
from modules.database import load_general_data

def render_tab_general():
    df = load_general_data()
    if df.empty:
        st.warning("Hệ thống chưa tải được dữ liệu. Vui lòng kiểm tra kết nối cơ sở dữ liệu.")
        return

    # Bộ lọc động trên đầu trang
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_years = st.multiselect(
            "Lọc theo Năm học / Trạng thái:", 
            options=df['year_label'].unique(), 
            default=df['year_label'].unique()
        )
    with col_f2:
        selected_genders = st.multiselect(
            "Lọc theo Giới tính:", 
            options=df['gender_label'].unique(), 
            default=df['gender_label'].unique()
        )

    # Khởi tạo DataFrame lọc động dựa trên điều kiện của người dùng
    df_filtered = df[(df['year_label'].isin(selected_years)) & (df['gender_label'].isin(selected_genders))]

    if df_filtered.empty:
        st.warning("Không có dữ liệu phù hợp với tiêu chí bộ lọc đã chọn.")
        return

    st.markdown("### Chỉ số tổng hợp toàn nhóm")
    
    # Tính toán các chỉ số cốt lõi từ DataFrame đã lọc (df_filtered)
    total_students = len(df_filtered)
    avg_gpa_raw = df_filtered['gpa_raw'].mean()
    ratio_good = (len(df_filtered[df_filtered['gpa_raw'] >= 4]) / total_students) * 100 if total_students > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng số sinh viên (n)", f"{total_students} SV")
    col2.metric("GPA Trung bình (Thang 5)", f"{avg_gpa_raw:.2f} / 5.00")
    col3.metric("Tỷ lệ Học lực Khá/Giỏi trở lên", f"{ratio_good:.1f}%")

    st.markdown("---")

    # Phân bổ không gian hiển thị song song hệ thống biểu đồ thông minh
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Cấu trúc xếp loại học lực theo Giới tính**")
        
        gpa_map = {1: "Yếu (<2.0)", 2: "Trung bình (2.0-2.5)", 3: "Khá (2.5-3.2)", 4: "Giỏi (3.2-3.6)", 5: "Xuất sắc (>3.6)"}
        df_filtered['Học lực'] = df_filtered['gpa_raw'].map(gpa_map)
        gpa_order = ["Yếu (<2.0)", "Trung bình (2.0-2.5)", "Khá (2.5-3.2)", "Giỏi (3.2-3.6)", "Xuất sắc (>3.6)"]

        # Phân nhóm tính toán số lượng sinh viên nội bộ giới tính
        df_gender_gpa = df_filtered.groupby(['gender_label', 'Học lực']).size().reset_index(name='Số lượng')
        
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
        st.plotly_chart(fig_bar, width='stretch')

    with c2:
        st.markdown("**Mật độ tương quan giữa Thời gian tự học và Xếp loại học lực**")
        
        time_study_map = {1: "Dưới 2 giờ", 2: "2 - dưới 4 giờ", 3: "4 - dưới 6 giờ", 4: "6 - dưới 8 giờ", 5: "Trên 8 giờ"}
        df_filtered['Thời gian tự học'] = df_filtered['time_studying'].map(time_study_map)
        study_order = ["Dưới 2 giờ", "2 - dưới 4 giờ", "4 - dưới 6 giờ", "6 - dưới 8 giờ", "Trên 8 giờ"]

        fig_heat = px.density_heatmap(
            df_filtered, 
            x="Thời gian tự học", 
            y="Học lực", 
            category_orders={"Thời gian tự học": study_order, "Học lực": gpa_order},
            text_auto=True,
            color_continuous_scale="Blues",
            labels={"Thời gian tự học": "Thời gian tự học trong ngày", "Học lực": "Phân hạng học lực"}
        )
        fig_heat.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_heat, width='stretch')