
import streamlit as st
import pandas as pd
from alpha_signal_checker_plus import (
    lấy_danh_sách_top_coin,
    phân_tích_danh_sách_mã,
    trực_quan_hóa_kết_quả
)

st.set_page_config(page_title="Crypto Alpha Signal", layout="wide")

st.title("📊 Phân tích tín hiệu Alpha - Crypto Market")

st.markdown("### Chọn số lượng coin top từ CoinGecko")
số_coin = st.slider("Số lượng coin:", min_value=10, max_value=100, step=10, value=30)

if st.button("🚀 Phân tích tín hiệu"):
    with st.spinner("Đang lấy dữ liệu và phân tích..."):
        danh_sách_mã = lấy_danh_sách_top_coin(số_coin)
        df_kết_quả = phân_tích_danh_sách_mã(danh_sách_mã)
        st.session_state["kq_df"] = df_kết_quả
        st.success("✅ Phân tích hoàn tất!")
        st.dataframe(df_kết_quả)

        st.markdown("### 📈 Biểu đồ dòng tiền & điểm ròng")
        trực_quan_hóa_kết_quả(df_kết_quả)
