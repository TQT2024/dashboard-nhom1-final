import streamlit as st
import pandas as pd
from modules.charts import *

def render_tab_general():
    if 'filtered_df' not in st.session_state: return
    df_filtered = st.session_state['filtered_df']
    df_raw = st.session_state['raw_df']
    
    if len(df_filtered) == 0:
        st.warning("⚠️ Không có dữ liệu phù hợp.")
        return

    # KPI Section
    k1, k2, k3 = st.columns(3)
    k1.metric("Cỡ mẫu (n)", f"{len(df_filtered)} SV")
    k2.metric("GPA Trung bình", f"{df_filtered['gpa_raw'].mean():.2f}")
    k3.metric("Tự học bình quân", f"{df_filtered['time_studying'].mean():.1f}/5")
    st.markdown("---")

    # Tầng 1: Thực trạng
    st.subheader("1. Bức tranh học thuật hiện tại")
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(draw_pie_chart(df_filtered), use_container_width=True)
    with c2: st.plotly_chart(draw_smart_chart(df_filtered, df_raw), use_container_width=True)
    
    # Tầng 2: Nhân tố tự thân
    st.subheader("2. Tác động của hành vi cá nhân")
    c3, c4 = st.columns([1.2, 1])
    with c3: st.plotly_chart(draw_density_heatmap(df_filtered), use_container_width=True)
    with c4: st.plotly_chart(draw_scatter_plot(df_filtered), use_container_width=True)
    
    # Chú thích động dựa trên toán học tương quan
    if len(df_filtered) > 5:
        corr = df_filtered['index_tu_luc_scaled'].corr(df_filtered['gpa_scaled'])
        st.info(f"💡 **Phân tích tương quan:** Hệ số r = {corr:.2f}. " + 
                ("Tương quan thuận mạnh: Năng lực tự học quyết định GPA." if corr > 0.5 else "Tương quan vừa phải."))

    # Tầng 3: Nhân tố ngoại cảnh
    st.subheader("3. Đặc thù giới tính và môi trường")
    c5, c6 = st.columns(2)
    with c5: st.plotly_chart(draw_stacked_bar(df_filtered), use_container_width=True)
    with c6: st.plotly_chart(draw_treemap(df_filtered), use_container_width=True)
