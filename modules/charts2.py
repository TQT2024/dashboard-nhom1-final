import plotly.graph_objects as go

def draw_radar_chart(student_data, df_all):
    """Biểu đồ Radar đa giác kép đồng bộ hệ màu Mint - Cam đất (Nén chiều cao height=280)"""
    # Tính toán giá trị trung bình toàn khóa làm tham chiếu nền
    mean_data = df_all[['index_tu_luc_scaled', 'index_moi_truong_truong_scaled', 'index_moi_truong_ban_be_scaled', 'gpa_scaled']].mean()
    
    categories = ['Năng lực Tự lực', 'Hỗ trợ từ Trường', 'Áp lực Bạn bè', 'Kết quả GPA']
    
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
    
    # 1. Đa giác cá nhân sinh viên - Tông xanh Mint thương hiệu
    fig.add_trace(go.Scatterpolar(
        r=sv_metrics, theta=categories, fill='toself', 
        name=str(student_data['full_name']),
        fillcolor='rgba(42, 157, 143, 0.2)', 
        line=dict(color='#2a9d8f', width=2.5)
    ))
    
    # 2. Đa giác trung bình khóa - Tông Cam đất tương phản đối chiếu
    fig.add_trace(go.Scatterpolar(
        r=mean_metrics, theta=categories, fill='toself', 
        name='Trung bình khóa',
        fillcolor='rgba(231, 111, 81, 0.02)', 
        line=dict(color='#e76f51', width=1.5, dash='dash') 
    ))
    
    fig.update_layout(
        height=280, # NÉN CHÂN BIỂU ĐỒ XUỐNG 280PX ĐỂ KHÔNG BỊ TRÀN MAN HÌNH
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=True, tickfont=dict(size=8, color='gray')),
            angularaxis=dict(tickfont=dict(size=10, color='#333'))
        ),
        margin=dict(l=40, r=40, t=15, b=15),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(size=9))
    )
    return fig
