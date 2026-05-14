import plotly.express as px
import pandas as pd

gpa_order = ["Yếu (<2.0)", "Trung bình (2.0-2.5)", "Khá (2.5-3.2)", "Giỏi (3.2-3.6)", "Xuất sắc (>3.6)"]
study_order = ["Dưới 2 giờ", "2 - dưới 4 giờ", "4 - dưới 6 giờ", "6 - dưới 8 giờ", "Trên 8 giờ"]

def _prepare_labels(df):
    d = df.copy()
    gpa_map = {1: "Yếu (<2.0)", 2: "Trung bình (2.0-2.5)", 3: "Khá (2.5-3.2)", 4: "Giỏi (3.2-3.6)", 5: "Xuất sắc (>3.6)"}
    time_study_map = {1: "Dưới 2 giờ", 2: "2 - dưới 4 giờ", 3: "4 - dưới 6 giờ", 4: "6 - dưới 8 giờ", 5: "Trên 8 giờ"}
    
    d['Học lực'] = d['gpa_raw'].map(gpa_map)
    d['Thời gian tự học'] = d['time_studying'].map(time_study_map)
    return d

def draw_pie_chart(df):
    """Cấu phần học lực toàn khối - Đã đồng bộ đơn sắc thương hiệu, đẩy số lên đỉnh cột"""
    d = _prepare_labels(df)
    df_pie = d.groupby('Học lực').size().reset_index(name='Số lượng')
    
    fig = px.bar(
        df_pie, x="Học lực", y="Số lượng", text_auto=True,
        category_orders={"Học lực": gpa_order}
    )
    fig.update_traces(textposition='outside', marker_color='#2a9d8f', marker_line_color='rgba(0,0,0,0)')
    fig.update_layout(
        height=330, xaxis_title=None, yaxis_title="Số sinh viên", 
        showlegend=False, margin=dict(l=20, r=20, t=20, b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def draw_stacked_bar(df):
    """Cấu trúc học lực phân hạng so sánh liên giới tính"""
    d = _prepare_labels(df)
    df_bar = d.groupby(['gender_label', 'Học lực']).size().reset_index(name='Số lượng')
    fig = px.bar(
        df_bar, y="gender_label", x="Số lượng", color="Học lực", orientation="h",
        text_auto='.1f', category_orders={"Học lực": gpa_order},
        color_discrete_sequence=px.colors.sequential.YlGnBu_r,
        labels={"gender_label": "Giới tính", "Số lượng": "Tỷ trọng (%)"}
    )
    fig.update_traces(textposition='auto')
    fig.update_layout(height=310, barmode='stack', barnorm='percent', xaxis_title="Tỷ lệ %", yaxis_title=None, margin=dict(l=0, r=0, t=20, b=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def draw_line_chart(df):
    df_line = df.groupby('year_label')['gpa_scaled'].mean().reset_index()
    year_order = {"Năm 3": 0, "Năm 4": 1, "Đã tốt nghiệp": 2}
    df_line['order'] = df_line['year_label'].map(year_order)
    df_line = df_line.sort_values('order')
    
    fig = px.line(
        df_line, x="year_label", y="gpa_scaled", markers=True,
        labels={"year_label": "Giai đoạn học", "gpa_scaled": "Điểm quy đổi (Trung bình)"}
    )
    fig.update_traces(line_color='#2a9d8f', line_width=3, marker=dict(size=8, color='#2a9d8f'))
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10), yaxis=dict(range=[0, 100]), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    fig.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    return fig

def draw_policy_bar(df):
    """Biểu đồ dự phòng diện chính sách của Tab General"""
    df_policy = df.groupby('policy_label')['gpa_scaled'].mean().reset_index()
    fig = px.bar(
        df_policy, x="policy_label", y="gpa_scaled", text_auto='.1f',
        color="policy_label", color_discrete_sequence=['#2a9d8f', '#94d2bd'],
        labels={"policy_label": "Diện chính sách", "gpa_scaled": "Điểm quy đổi (Trung bình)"}
    )
    fig.update_layout(height=320, xaxis_title=None, yaxis_title="Điểm bình quân", showlegend=False, margin=dict(l=0, r=0, t=20, b=0), yaxis=dict(range=[0, 100]), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    return fig

def draw_scatter_plot(df):
    d = _prepare_labels(df)
    df_scatter = d.groupby(['time_studying', 'gpa_raw', 'Thời gian tự học', 'Học lực']).size().reset_index(name='Mật độ SV')
    
    fig = px.scatter(
        df_scatter, x="Thời gian tự học", y="Học lực", size="Mật độ SV", color="Mật độ SV",
        category_orders={"Thời gian tự học": study_order, "Học lực": gpa_order},
        color_continuous_scale="YlGnBu", size_max=35,
        labels={"Thời gian tự học " : "Thời gian tự học trong ngày", "Học lực": "Học lực"}
    )
    fig.update_xaxes(showgrid=True, gridcolor='#eef0f2', range=[-0.5, 4.5])
    fig.update_yaxes(showgrid=True, gridcolor='#eef0f2', range=[-0.5, 4.5])
    fig.update_layout(height=320, margin=dict(l=0, r=0, t=20, b=0), coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def draw_density_heatmap(df):
    d = _prepare_labels(df)
    fig = px.density_heatmap(
        d, x="Thời gian tự học", y="Học lực", 
        category_orders={"Thời gian tự học": study_order, "Học lực": gpa_order},
        text_auto=True, color_continuous_scale="YlGnBu",
        labels={"Thời gian tự học": "Thời gian tự học trong ngày", "Học lực": "Học lực"}
    )
    fig.update_xaxes(range=[-0.5, 4.5])
    fig.update_yaxes(range=[-0.5, 4.5])
    fig.update_layout(height=320, margin=dict(l=0, r=0, t=20, b=0), coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig
