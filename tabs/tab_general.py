import streamlit as st
import pandas as pd
from modules.charts import *

def _get_gpa_label(val):
    if val < 2.0: return "Mức Yếu"
    if val < 2.5: return "Mức Trung bình"
    if val < 3.2: return "Mức Khá"
    if val < 3.6: return "Mức Giỏi"
    return "Mức Xuất sắc"

def _get_study_label(val):
    if val < 1.5: return "~ Dưới 2 giờ"
    if val < 2.5: return "~ 2 - dưới 4 giờ"
    if val < 3.5: return "~ 4 - dưới 6 giờ"
    if val < 4.5: return "~ 6 - dưới 8 giờ"
    return "~ Trên 8 giờ"

def render_tab_general():
    if 'filtered_df' not in st.session_state: return
    df_filtered = st.session_state['filtered_df']
    df_raw = st.session_state['raw_df']
    
    if len(df_filtered) == 0:
        st.warning("⚠️ Không có dữ liệu phù hợp với điều kiện lọc hiện hành.")
        return

    years = st.session_state.get('global_years', [])
    genders = st.session_state.get('global_genders', [])
    
    is_all_years = len(years) == 0 or len(years) == len(df_raw['year_label'].unique())
    is_all_genders = len(genders) == 0 or len(genders) == len(df_raw['gender_label'].unique())
    
    if is_all_years and is_all_genders:
        suffix = " (Toàn khóa)"
    else:
        parts = []
        if not is_all_years: parts.append("+".join(years))
        if not is_all_genders: parts.append("+".join(genders))
        suffix = f" ({', '.join(parts)})"

    gpa_avg = df_filtered['gpa_raw'].mean()
    study_avg = df_filtered['time_studying'].mean()

    k1, k2, k3 = st.columns(3)
    k1.metric("Cỡ mẫu khảo sát (n)", f"{len(df_filtered)} SV")
    k2.metric("GPA Trung bình toàn khối", f"{gpa_avg:.2f} ({_get_gpa_label(gpa_avg)})")
    k3.metric("Thời gian tự học bình quân", f"{study_avg:.1f}/5 ({_get_study_label(study_avg)})")
    st.markdown("---")

    st.subheader("1. Bức tranh học thuật hiện tại")
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(draw_pie_chart(df_filtered, suffix), use_container_width=True, config={'displayModeBar': False})
    with c2: st.plotly_chart(draw_smart_chart(df_filtered, df_raw, suffix), use_container_width=True, config={'displayModeBar': False})
    
    st.subheader("2. Tác động của hành vi cá nhân")
    c3, c4 = st.columns([1.2, 1])
    with c3: st.plotly_chart(draw_density_heatmap(df_filtered, suffix), use_container_width=True, config={'displayModeBar': False})
    with c4: st.plotly_chart(draw_scatter_plot(df_filtered, suffix), use_container_width=True, config={'displayModeBar': False})
    
    if len(df_filtered) > 5:
        corr = df_filtered['index_tu_luc_scaled'].corr(df_filtered['gpa_scaled'])
        desc = "Mức độ tương quan thuận mạnh mẽ: Hành vi tự lực nội tại trực tiếp thúc đẩy điểm tích lũy học tập." if corr > 0.5 else "Mức độ tương quan thuận ở dải vừa phải."
        st.info(f"🔮 **Hệ số tương quan Pearson tuyến tính:** r = {corr:.2f}. {desc}")

    st.subheader("3. Đặc thù giới tính và môi trường")
    c5, c6 = st.columns(2)
    with c5: st.plotly_chart(draw_stacked_bar(df_filtered, suffix), use_container_width=True, config={'displayModeBar': False})
    with c6: st.plotly_chart(draw_treemap(df_filtered, suffix), use_container_width=True, config={'displayModeBar': False})
