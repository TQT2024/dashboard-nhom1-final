import streamlit as st
import pandas as pd
import numpy as np
from modules.charts import (
    draw_pie_chart, draw_smart_chart, draw_density_heatmap,
    draw_scatter_plot, draw_stacked_bar, draw_treemap
)

def get_gpa_label(val):
    if np.isnan(val): return "N/A"
    if val < 2.0: return "Yếu"
    elif val < 2.5: return "Trung bình"
    elif val < 3.2: return "Khá"
    elif val < 3.6: return "Giỏi"
    else: return "Xuất sắc"

def get_study_label(val):
    if np.isnan(val): return "N/A"
    if val < 1.5: return "Dưới 2 giờ"
    elif val < 2.5: return "2 - dưới 4 giờ"
    elif val < 3.5: return "4 - dưới 6 giờ"
    elif val < 4.5: return "6 - dưới 8 giờ"
    else: return "Trên 8 giờ"

def render_tab_general():
    if 'filtered_df' not in st.session_state or 'raw_df' not in st.session_state: 
        return
        
    df_filtered = st.session_state['filtered_df']
    df_raw = st.session_state['raw_df']
    total_students = len(df_filtered)
    
    # BẪY LỖI 1: Ngăn chặn lỗi rỗng khi bộ lọc quá khắt khe
    if total_students == 0:
        st.warning("⚠️ Không có sinh viên nào thỏa mãn tiêu chí bộ lọc. Vui lòng mở rộng dải lựa chọn ở Sidebar.")
        return

    # --- KHU VỰC 0: THẺ KPI ---
    avg_gpa = df_filtered['gpa_raw'].mean()
    avg_study = df_filtered['time_studying'].mean()

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.markdown(f"<div style='text-align:center; padding:10px; background-color:#f8f9fa; border-radius:5px;'><span style='font-size:12px; color:gray;'>Cỡ mẫu hiện tại (n)</span><br><b style='font-size:22px; color:#2a9d8f;'>{total_students:,} SV</b></div>", unsafe_allow_html=True)
    kpi2.markdown(f"<div style='text-align:center; padding:10px; background-color:#f8f9fa; border-radius:5px;'><span style='font-size:12px; color:gray;'>GPA trung bình</span><br><b style='font-size:22px; color:#2a9d8f;'>{avg_gpa:.2f} ({get_gpa_label(avg_gpa)})</b></div>", unsafe_allow_html=True)
    kpi3.markdown(f"<div style='text-align:center; padding:10px; background-color:#f8f9fa; border-radius:5px;'><span style='font-size:12px; color:gray;'>Thời gian tự học bình quân</span><br><b style='font-size:22px; color:#2a9d8f;'>{avg_study:.1f} ({get_study_label(avg_study)})</b></div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

    # BẪY LỖI 2: Cảnh báo kích thước mẫu nhỏ
    if total_students < 10:
        st.warning("ℹ️ Cảnh báo thống kê: Kích thước mẫu hiện tại quá nhỏ (n < 10) để đưa ra các kết luận xu hướng chính xác. Biểu đồ dưới đây mang tính chất tham khảo cục bộ.")

    # Ẩn thanh công cụ Plotly để giao diện sạch sẽ
    chart_config = {'displayModeBar': False}

    # --- TẦNG 1: THỰC TRẠNG VĨ MÔ ---
    st.markdown("<h4 style='color:#264653;'>1. Bức tranh học thuật hiện tại</h4>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#2a9d8f; text-align:center;'>Cấu trúc học lực toàn khối</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_pie_chart(df_filtered), use_container_width=True, config=chart_config)
    with r1c2:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#2a9d8f; text-align:center;'>Phân tích Điểm chuẩn hóa (Xu hướng / Đối chứng)</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_smart_chart(df_filtered, df_raw), use_container_width=True, config=chart_config)
    
    # Annotation Tầng 1
    good_excel_count = len(df_filtered[df_filtered['gpa_raw'] >= 4])
    good_excel_pct = (good_excel_count / total_students) * 100 if total_students > 0 else 0
    st.info(f"💡 **Nhận định:** Tỷ lệ sinh viên đạt mức Khá/Giỏi trở lên trong tệp phân tích chiếm **{good_excel_pct:.1f}%**. Hệ thống ghi nhận hiệu suất học thuật thay đổi trực tiếp theo bộ lọc được chọn.")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- TẦNG 2: MỔ XẺ NHÂN TỐ TỰ THÂN ---
    st.markdown("<h4 style='color:#264653;'>2. Tác động của hành vi chủ quan (Nhân tố lõi)</h4>", unsafe_allow_html=True)
    r2c1, r2c2 = st.columns([1.2, 1]) # Bố cục bất đối xứng để ưu tiên Heatmap
    with r2c1:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#2a9d8f; text-align:center;'>Ma trận Mật độ: Thời gian tự học & Học lực</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_density_heatmap(df_filtered), use_container_width=True, config=chart_config)
    with r2c2:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#2a9d8f; text-align:center;'>Phân tán: Năng lực Tự lực & Kết quả GPA</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_scatter_plot(df_filtered), use_container_width=True, config=chart_config)

    # Annotation Tầng 2 (Tính hệ số tương quan Pearson)
    if total_students > 5:
        corr_val = df_filtered['index_tu_luc_scaled'].corr(df_filtered['gpa_scaled'])
        if pd.isna(corr_val):
            corr_text = "Không đủ biên độ dữ liệu để nội suy hệ số tương quan."
        elif corr_val >= 0.5:
            corr_text = f"Mức độ tương quan thuận mạnh mẽ (r = {corr_val:.2f}). Năng lực tự lực nội tại quyết định trực tiếp đến sự bứt phá kết quả học tập."
        elif corr_val >= 0.2:
            corr_text = f"Mức độ tương quan thuận vừa phải (r = {corr_val:.2f})."
        else:
            corr_text = f"Mức độ tương quan yếu (r = {corr_val:.2f})."
            
        st.success(f"📈 **Phân tích mô hình:** Hệ số tương quan Pearson giữa Năng lực tự lực và GPA là **{corr_val:.2f}**. {corr_text}")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- TẦNG 3: MỔ XẺ NHÂN TỐ NGOẠI CẢNH ---
    st.markdown("<h4 style='color:#264653;'>3. Cấu trúc Nhân khẩu và Hỗ trợ từ Nhà trường</h4>", unsafe_allow_html=True)
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#2a9d8f; text-align:center;'>So sánh cấu trúc Học lực theo Giới tính</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_stacked_bar(df_filtered), use_container_width=True, config=chart_config)
    with r3c2:
        st.markdown("<p style='font-size:14px; font-weight:bold; color:#2a9d8f; text-align:center;'>Phân cấp cấu trúc: Nhóm Học lực & Mức hỗ trợ</p>", unsafe_allow_html=True)
        st.plotly_chart(draw_treemap(df_filtered), use_container_width=True, config=chart_config)
