import plotly.express as px
import pandas as pd

# Cấu hình thứ tự sắp xếp chuẩn cho các trục tọa độ phân hạng
gpa_order = ["Yếu (<2.0)", "Trung bình (2.0-2.5)", "Khá (2.5-3.2)", "Giỏi (3.2-3.6)", "Xuất sắc (>3.6)"]
study_order = ["Dưới 2 giờ", "2 - dưới 4 giờ", "4 - dưới 6 giờ", "6 - dưới 8 giờ", "Trên 8 giờ"]

def _prepare_labels(df):
    """Hàm dùng nội bộ để chuẩn hóa nhãn chữ tiếng Việt cho dữ liệu phân hạng Ordinal"""
    d = df.copy()
    gpa_map = {1: "Yếu (<2.0)", 2: "Trung bình (2.0-2.5)", 3: "Khá (2.5-3.2)", 4: "Giỏi (3.2-3.6)", 5: "Xuất sắc (>3.6)"}
    time_study_map = {1: "Dưới 2 giờ", 2: "2 - dưới 4 giờ", 3: "4 - dưới 6 giờ", 4: "6 - dưới 8 giờ", 5: "Trên 8 giờ"}
    
    d['Học lực'] = d['gpa_raw'].map(gpa_map)
    d['Thời gian tự học'] = d['time_studying'].map(time_study_map)
    return d

def draw_pie_chart(df):
    """Biểu đồ cơ bản 1: Pie Chart - Tỷ trọng cấu phần học lực toàn khối"""
    d = _prepare_labels(df)
    df_pie = d.groupby('Học lực').size().reset_index(name='Số lượng')
    
    fig = px.pie(
        df_pie, values='Số lượng', names='Học lực',
        category_orders={"Học lực": gpa_order},
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=-0.1))
    return fig

def draw_stacked_bar(df):
    """Biểu đồ cơ bản 2: Stacked Bar Chart - Cấu trúc học lực theo Giới tính"""
    d = _prepare_labels(df)
    df_bar = d.groupby(['gender_label', 'Học lực']).size().reset_index(name='Số lượng')
    
    fig = px.bar(
        df_bar, y="gender_label", x="Số lượng", color="Học lực", orientation="h",
        text_auto='.1f', category_orders={"Học lực": gpa_order},
        color_discrete_sequence=px.colors.sequential.Blues_r,
        labels={"gender_label": "Giới tính", "Số lượng": "Tỷ trọng (%)"}
    )
    fig.update_layout(barmode='stack', barnorm='percent', xaxis_title="Tỷ lệ (%)", yaxis_title=None, margin=dict(l=0, r=0, t=10, b=0))
    return fig

def draw_line_chart(df):
    """Biểu đồ cơ bản 3: Line Graph - Xu hướng điểm trung bình biến thiên qua các năm"""
    df_line = df.groupby('year_label')['gpa_scaled'].mean().reset_index()
    # Sắp xếp thứ tự thời gian năm học một cách thủ công để tránh lỗi bảng chữ cái ABC
    year_order = {"Năm 3": 0, "Năm 4": 1, "Đã tốt nghiệp": 2}
    df_line['order'] = df_line['year_label'].map(year_order)
    df_line = df_line.sort_values('order')
    
    fig = px.line(
        df_line, x="year_label", y="gpa_scaled", markers=True,
        labels={"year_label": "Tiến trình năm học", "gpa_scaled": "GPA Quy đổi (Trung bình)"}
    )
    fig.update_traces(line_color='#1f77b4', line_width=3, marker=dict(size=8))
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0))
    return fig

def draw_scatter_plot(df):
    """Biểu đồ cơ bản 4: Scatter Plot - Tương quan điểm số dùng Size Mapping khắc phục Overplotting"""
    d = _prepare_labels(df)
    # Gom nhóm để tính số lượng sinh viên tại mỗi tọa độ giao nhau (X, Y)
    df_scatter = d.groupby(['time_studying', 'gpa_raw', 'Thời gian tự học', 'Học lực']).size().reset_index(name='Mật độ SV')
    
    fig = px.scatter(
        df_scatter, x="Thời gian tự học", y="Học lực", size="Mật độ SV", color="Mật độ SV",
        category_orders={"Thời gian tự học": study_order, "Học lực": gpa_order},
        color_continuous_scale="Blues", size_max=40,
        labels={"Thời gian tự học": "Thời gian tự học/ngày", "Học lực": "Học lực"}
    )
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), coloraxis_showscale=False)
    return fig

def draw_density_heatmap(df):
    """Biểu đồ nâng cao 1: Density Heatmap - Ma trận ô vuông mật độ đa biến"""
    d = _prepare_labels(df)
    fig = px.density_heatmap(
        d, x="Thời gian tự học", y="Học lực", 
        category_orders={"Thời gian tự học": study_order, "Học lực": gpa_order},
        text_auto=True, color_continuous_scale="Blues",
        labels={"Thời gian tự học": "Thời gian tự học/ngày", "Học lực": "Học lực"}
    )
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0))
    return fig
