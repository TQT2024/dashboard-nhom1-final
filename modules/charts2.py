import plotly.graph_objects as go

def draw_radar_chart(student_data, df_all):
    """Biểu đồ Radar đa giác kép đồng bộ hệ màu Mint - Cam đất (Tối ưu kích thước nhãn chữ và phóng to đa giác)"""
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
        name='Cá nhân',
        fillcolor='rgba(42, 157, 143, 0.25)', 
        line=dict(color='#2a9d8f', width=3)
    ))
    
    # 2. Đa giác trung bình khóa - Tông Cam đất tương phản đối chiếu
    fig.add_trace(go.Scatterpolar(
        r=mean_metrics, theta=categories, fill='toself', 
        name='Trung bình khóa',
        fillcolor='rgba(231, 111, 81, 0.02)', 
        line=dict(color='#e76f51', width=2, dash='dash') 
    ))
    
    fig.update_layout(
        height=320, # Tăng chiều cao tối ưu để đa giác bung rộng
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=True, tickfont=dict(size=9, color='gray')),
            angularaxis=dict(tickfont=dict(size=11, color='#222', weight='bold')) # Làm nét và đậm chữ tiêu chí
        ),
        margin=dict(l=50, r=50, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=10))
    )
    return fig
