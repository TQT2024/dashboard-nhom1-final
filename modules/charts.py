import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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

COMMON_LAYOUT = dict(
    height=380, 
    margin=dict(l=20, r=20, t=40, b=30),
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(size=12)
)

def draw_pie_chart(df, suffix=""):
    d = _prepare_labels(df)
    df_pie = d.groupby('Học lực').size().reset_index(name='Số lượng')
    fig = px.pie(df_pie, names='Học lực', values='Số lượng', category_orders={"Học lực": gpa_order}, hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(colors=PALETTE_SEQ))
    fig.update_layout(**COMMON_LAYOUT, title=f"Cơ cấu phân hạng học lực {suffix}", showlegend=False)
    return fig

def draw_smart_chart(df_filtered, df_all, suffix=""):
    years_selected = df_filtered['year_label'].unique()
    if len(years_selected) > 1:
        df_line = df_filtered.groupby('year_label')['gpa_scaled'].mean().reset_index()
        year_order = {"Năm 3": 0, "Năm 4": 1, "Đã tốt nghiệp": 2}
        df_line['order'] = df_line['year_label'].map(year_order)
        df_line = df_line.sort_values('order')
        fig = px.line(df_line, x="year_label", y="gpa_scaled", markers=True)
        fig.update_traces(line_color=ORANGE, line_width=4, marker=dict(size=10, color=MINT))
        fig.update_layout(**COMMON_LAYOUT, title=f"Xu hướng điểm số qua các giai đoạn {suffix}", yaxis=dict(range=[0, 105], title="GPA Quy đổi (Thang 100)"))
    else:
        current_gpa = df_filtered['gpa_scaled'].mean()
        overall_gpa = df_all['gpa_scaled'].mean()
        lbl = years_selected[0] if len(years_selected) == 1 else "Nhóm chọn"
        fig = go.Figure(data=[
            go.Bar(name='Nhóm hiện tại', x=[lbl], y=[current_gpa], marker_color=MINT, text=f"{current_gpa:.1f}", textposition='auto'),
            go.Bar(name='Trung bình toàn khóa', x=[lbl], y=[overall_gpa], marker_color="gray", opacity=0.5, text=f"{overall_gpa:.1f}", textposition='auto')
        ])
        fig.update_layout(**COMMON_LAYOUT, title=f"So sánh GPA nhóm với toàn khối {suffix}", barmode='group', yaxis=dict(range=[0, 105], title="GPA Quy đổi (Thang 100)"))
    fig.update_layout(xaxis=dict(title=None))
    return fig

def draw_density_heatmap(df, suffix=""):
    d = _prepare_labels(df)
    fig = px.density_heatmap(
        d, x="Thời gian tự học", y="Học lực", 
        category_orders={"Thời gian tự học": study_order, "Học lực": gpa_order},
        text_auto=True, color_continuous_scale=PALETTE_SEQ
    )
    # Hiển thị dải màu nằm ngang, ghi đè margin-bottom để không đè lên trục X
    fig.update_layout(
        **COMMON_LAYOUT, 
        title=f"Ma trận mật độ hành vi Tự học vs Học lực {suffix}",
        coloraxis_colorbar=dict(
            title="Số lượng SV",
            orientation="h",
            thickness=10,
            len=0.6,
            y=-0.25
        ),
        margin=dict(l=20, r=20, t=40, b=70) 
    )
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    return fig

def draw_scatter_plot(df, suffix=""):
    fig = px.scatter(
        df, x="index_tu_luc_scaled", y="gpa_scaled", 
        color="time_studying", color_continuous_scale=PALETTE_SEQ,
        labels={"index_tu_luc_scaled": "Năng lực Tự lực học tập", "gpa_scaled": "Kết quả điểm tích lũy GPA"}
    )
    fig.update_traces(marker=dict(size=12, opacity=0.6))
    # Hiển thị dải màu nằm ngang, ép tickvals từ 1-5, ghi đè margin-bottom
    fig.update_layout(
        **COMMON_LAYOUT, 
        title=f"Phân tán tương quan Tự học vs GPA {suffix}", 
        xaxis=dict(range=[0, 105]), 
        yaxis=dict(range=[0, 105]),
        coloraxis_colorbar=dict(
            title="Mức tự học",
            orientation="h",
            thickness=10,
            len=0.6,
            y=-0.25,
            tickvals=[1, 2, 3, 4, 5],
            ticktext=["1", "2", "3", "4", "5"]
        ),
        margin=dict(l=20, r=20, t=40, b=70)
    )
    return fig

def draw_stacked_bar(df, suffix=""):
    d = _prepare_labels(df)
    df_bar = d.groupby(['gender_label', 'Học lực']).size().reset_index(name='Số lượng')
    fig = px.bar(
        df_bar, y="gender_label", x="Số lượng", color="Học lực", orientation="h",
        text_auto='.1f', category_orders={"Học lực": gpa_order},
        color_discrete_sequence=PALETTE_SEQ[::-1]
    )
    fig.update_layout(**COMMON_LAYOUT, title=f"Cấu trúc học lực phân rã theo Giới tính {suffix}", barmode='stack', barnorm='percent', showlegend=True, legend=dict(orientation="h", y=-0.2, title=None), xaxis=dict(title=None), yaxis=dict(title=None))
    return fig

def draw_treemap(df, suffix=""):
    d = _prepare_labels(df)
    df_tree = d.groupby(['Học lực', 'Hỗ trợ từ trường']).size().reset_index(name='Số lượng')
    df_tree = df_tree[df_tree['Số lượng'] > 0]
    fig = px.treemap(
        df_tree, path=[px.Constant("Toàn bộ nhóm"), 'Học lực', 'Hỗ trợ từ trường'], 
        values='Số lượng', color='Số lượng', color_continuous_scale=PALETTE_SEQ
    )
    fig.update_traces(textinfo="label+value")
    fig.update_layout(**COMMON_LAYOUT, title=f"Phân cấp cấu trúc Mức độ hỗ trợ từ Nhà trường {suffix}") 
    return fig
