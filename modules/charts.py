import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Cấu hình hệ màu thương hiệu
MINT = "#2a9d8f"
ORANGE = "#e76f51"
PALETTE_SEQ = px.colors.sequential.YlGnBu

gpa_order = ["Yếu (<2.0)", "Trung bình (2.0-2.5)", "Khá (2.5-3.2)", "Giỏi (3.2-3.6)", "Xuất sắc (>3.6)"]
study_order = ["Dưới 2 giờ", "2 - dưới 4 giờ", "4 - dưới 6 giờ", "6 - dưới 8 giờ", "Trên 8 giờ"]

def _prepare_labels(df):
    d = df.copy()
    gpa_map = {1: "Yếu (<2.0)", 2: "Trung bình (2.0-2.5)", 3: "Khá (2.5-3.2)", 4: "Giỏi (3.2-3.6)", 5: "Xuất sắc (>3.6)"}
    time_study_map = {1: "Dưới 2 giờ", 2: "2 - dưới 4 giờ", 3: "4 - dưới 6 giờ", 4: "6 - dưới 8 giờ", 5: "Trên 8 giờ"}
    d['Học lực'] = d['gpa_raw'].map(gpa_map)
    d['Thời gian tự học'] = d['time_studying'].map(time_study_map)
    d['Hỗ trợ từ trường'] = pd.cut(
        d['index_moi_truong_truong_scaled'], 
        bins=[0, 60, 80, 105], 
        labels=['Hỗ trợ Thấp', 'Hỗ trợ Trung bình', 'Hỗ trợ Cao'],
        right=False
    )
    return d

# NÂNG CẤP: Kích thước lớn 380px, font chữ 12px
COMMON_LAYOUT = dict(
    height=380, 
    margin=dict(l=20, r=20, t=30, b=30),
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(size=12, family="Arial")
)

def draw_pie_chart(df):
    d = _prepare_labels(df)
    df_pie = d.groupby('Học lực').size().reset_index(name='Số lượng')
    fig = px.pie(df_pie, names='Học lực', values='Số lượng', category_orders={"Học lực": gpa_order}, hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(colors=PALETTE_SEQ))
    fig.update_layout(**COMMON_LAYOUT, showlegend=False)
    return fig

def draw_smart_chart(df_filtered, df_all):
    """LOGIC THÔNG MINH: Chuyển đổi Line sang Bar nếu chỉ lọc 1 năm"""
    years_selected = df_filtered['year_label'].unique()
    
    if len(years_selected) > 1:
        # Vẽ biểu đồ Line (Xu hướng)
        df_line = df_filtered.groupby('year_label')['gpa_scaled'].mean().reset_index()
        year_order = {"Năm 3": 0, "Năm 4": 1, "Đã tốt nghiệp": 2}
        df_line['order'] = df_line['year_label'].map(year_order)
        df_line = df_line.sort_values('order')
        
        fig = px.line(df_line, x="year_label", y="gpa_scaled", markers=True)
        fig.update_traces(line_color=ORANGE, line_width=4, marker=dict(size=10, color=MINT))
        fig.update_layout(**COMMON_LAYOUT, yaxis=dict(range=[0, 100], title="GPA Quy đổi"))
    else:
        # Vẽ biểu đồ Bar so sánh (Đối chứng)
        current_gpa = df_filtered['gpa_scaled'].mean()
        overall_gpa = df_all['gpa_scaled'].mean()
        
        fig = go.Figure(data=[
            go.Bar(name='Nhóm được chọn', x=[years_selected[0]], y=[current_gpa], marker_color=MINT, text=f"{current_gpa:.1f}"),
            go.Bar(name='Trung bình toàn khóa', x=[years_selected[0]], y=[overall_gpa], marker_color="gray", opacity=0.5, text=f"{overall_gpa:.1f}")
        ])
        fig.update_layout(**COMMON_LAYOUT, barmode='group', yaxis=dict(range=[0, 100], title="GPA Quy đổi"))
    
    fig.update_layout(xaxis=dict(title=None))
    return fig

def draw_density_heatmap(df):
    d = _prepare_labels(df)
    fig = px.density_heatmap(
        d, x="Thời gian tự học", y="Học lực", 
        category_orders={"Thời gian tự học": study_order, "Học lực": gpa_order},
        text_auto=True, color_continuous_scale=PALETTE_SEQ
    )
    fig.update_layout(**COMMON_LAYOUT, coloraxis_showscale=False)
    return fig

def draw_scatter_plot(df):
    """ÉP CỨNG TỌA ĐỘ 0-105 để thấy rõ xu hướng"""
    fig = px.scatter(
        df, x="index_tu_luc_scaled", y="gpa_scaled", 
        color="time_studying", color_continuous_scale=PALETTE_SEQ,
        labels={"index_tu_luc_scaled": "Điểm Tự lực", "gpa_scaled": "Kết quả GPA"}
    )
    fig.update_traces(marker=dict(size=12, opacity=0.6, line=dict(width=1, color='White')))
    fig.update_layout(**COMMON_LAYOUT, xaxis=dict(range=[0, 105]), yaxis=dict(range=[0, 105]), coloraxis_showscale=False)
    return fig

def draw_stacked_bar(df):
    d = _prepare_labels(df)
    df_bar = d.groupby(['gender_label', 'Học lực']).size().reset_index(name='Số lượng')
    fig = px.bar(
        df_bar, y="gender_label", x="Số lượng", color="Học lực", orientation="h",
        text_auto='.1f', category_orders={"Học lực": gpa_order},
        color_discrete_sequence=PALETTE_SEQ[::-1]
    )
    fig.update_layout(**COMMON_LAYOUT, barmode='stack', barnorm='percent', showlegend=True, legend=dict(orientation="h", y=-0.2))
    return fig

def draw_treemap(df):
    """GOM NHÓM DỮ LIỆU để Treemap rõ ràng, không nát chữ"""
    d = _prepare_labels(df)
    df_tree = d.groupby(['Học lực', 'Hỗ trợ từ trường']).size().reset_index(name='Số lượng')
    df_tree = df_tree[df_tree['Số lượng'] > 0] # Loại bỏ các nhóm rỗng
    
    fig = px.treemap(
        df_tree, path=[px.Constant("Tất cả"), 'Học lực', 'Hỗ trợ từ trường'], 
        values='Số lượng', color='Số lượng', color_continuous_scale=PALETTE_SEQ
    )
    fig.update_traces(textinfo="label+value")
    fig.update_layout(**COMMON_LAYOUT, margin=dict(l=0, r=0, t=0, b=0))
    return fig
