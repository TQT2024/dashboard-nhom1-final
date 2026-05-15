import plotly.graph_objects as go

def draw_radar_chart(student_data, df_all):
    mean_data = df_all[['index_tu_luc_scaled', 'index_moi_truong_truong_scaled', 'index_moi_truong_ban_be_scaled', 'gpa_scaled']].mean()
    categories = ['Năng lực Tự học', 'Hỗ trợ từ Trường', 'Áp lực Bạn bè', 'Kết quả GPA']
    
    sv_metrics = [
        float(student_data['index_tu_luc_scaled']), 
        float(student_data['index_moi_truong_truong_scaled']), 
        float(student_data['index_moi_truong_ban_be_scaled']), 
        float(student_data['gpa_scaled'])
    ]
    
    mean_metrics = [
        float(mean_data['index_tu_luc_scaled']), 
        float(mean_data['index_moi_truong_truong_scaled']), 
        float(mean_data['index_moi_truong_ban_be_scaled']), 
        float(mean_data['gpa_scaled'])
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=sv_metrics, theta=categories, fill='toself', 
        name='Cá nhân',
        fillcolor='rgba(42, 157, 143, 0.25)', 
        line=dict(color='#2a9d8f', width=3)
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=mean_metrics, theta=categories, fill='toself', 
        name='Trung bình khóa',
        fillcolor='rgba(231, 111, 81, 0.02)', 
        line=dict(color='#e76f51', width=1.5, dash='dash') 
    ))
    
    fig.update_layout(
        height=350, 
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=True, tickfont=dict(size=10, color='gray')),
            angularaxis=dict(tickfont=dict(size=12, color='#222', weight='bold'))
        ),
        margin=dict(l=80, r=80, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )
    return fig
