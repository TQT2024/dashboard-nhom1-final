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
    
    # Phân cụm mức độ hỗ trợ từ trường cho Treemap (Hierarchical Clustering)
    d['Hỗ trợ từ trường'] = pd.cut(
        d['index_moi_truong_truong_scaled'], 
        bins=[0, 60, 80, 105], 
        labels=['Hỗ trợ Thấp', 'Hỗ trợ Trung bình', 'Hỗ trợ Cao'],
        right=False
    )
    return d

# Khống chế chiều cao tĩnh 170px và thu nhỏ font trục để chống tràn
COMMON_LAYOUT = dict(
    height=170, 
    margin=dict(l=10, r=10, t=10, b=10),
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(size=10)
)

def draw_pie_chart(df):
    d = _prepare_labels(df)
    df_pie = d.groupby('Học lực').size().reset_index(name='Số lượng')
    fig = px.pie(df_pie, names='Học lực', values='Số lượng', category_orders={"Học lực": gpa_order}, hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(colors=px.colors.sequential.YlGnBu))
    fig.update_layout(**COMMON_LAYOUT, showlegend=False)
    return fig

def draw_line_chart(df):
    df_line = df.groupby('year_label')['gpa_scaled'].mean().reset_index()
    year_order = {"Năm 3": 0, "Năm 4": 1, "Đã tốt nghiệp": 2}
    df_line['order'] = df_line['year_label'].map(year_order)
    df_line = df_line.sort_values('order')
    
    fig = px.line(df_line, x="year_label", y="gpa_scaled", markers=True)
    fig.update_traces(line_color='#2a9d8f', line_width=2, marker=dict(size=6))
    fig.update_layout(**COMMON_LAYOUT, yaxis=dict(range=[0, 100], title=None), xaxis=dict(title=None))
    return fig

def draw_density_heatmap(df):
    d = _prepare_labels(df)
    fig = px.density_heatmap(
        d, x="Thời gian tự học", y="Học lực", 
        category_orders={"Thời gian tự học": study_order, "Học lực": gpa_order},
        text_auto=True, color_continuous_scale="YlGnBu"
    )
    fig.update_layout(**COMMON_LAYOUT, coloraxis_showscale=False, xaxis=dict(title=None), yaxis=dict(title=None))
    return fig

def draw_scatter_plot(df):
    fig = px.scatter(
        df, x="index_tu_luc_scaled", y="gpa_scaled", 
        color="time_studying", color_continuous_scale="YlGnBu"
    )
    fig.update_traces(marker=dict(size=8, opacity=0.7))
    fig.update_layout(**COMMON_LAYOUT, xaxis=dict(range=[0, 105], title="Năng lực tự lực"), yaxis=dict(range=[0, 105], title="GPA"), coloraxis_showscale=False)
    return fig

def draw_stacked_bar(df):
    d = _prepare_labels(df)
    df_bar = d.groupby(['gender_label', 'Học lực']).size().reset_index(name='Số lượng')
    fig = px.bar(
        df_bar, y="gender_label", x="Số lượng", color="Học lực", orientation="h",
        text_auto='.1f', category_orders={"Học lực": gpa_order},
        color_discrete_sequence=px.colors.sequential.YlGnBu_r
    )
    fig.update_layout(**COMMON_LAYOUT, barmode='stack', barnorm='percent', xaxis=dict(title=None), yaxis=dict(title=None), showlegend=False)
    return fig

def draw_treemap(df):
    d = _prepare_labels(df)
    df_tree = d.groupby(['Học lực', 'Hỗ trợ từ trường']).size().reset_index(name='Số lượng')
    df_tree = df_tree[df_tree['Số lượng'] > 0]
    
    fig = px.treemap(
        df_tree, path=[px.Constant("Sinh viên"), 'Học lực', 'Hỗ trợ từ trường'], values='Số lượng',
        color='Số lượng', color_continuous_scale='YlGnBu'
    )
    fig.update_traces(textinfo="label+value")
    
    # ĐÃ FIX LOGIC GHI ĐÈ THAM SỐ TẠI ĐÂY
    fig.update_layout(**COMMON_LAYOUT) 
    fig.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, t=0, b=0)) 
    
    return fig
