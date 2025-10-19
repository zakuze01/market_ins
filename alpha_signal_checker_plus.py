import requests
import pandas as pd
import random

def lấy_danh_sách_top_coin(số_lượng=50):
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": số_lượng,
        "page": 1,
        "sparkline": False
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return [coin["symbol"].upper() for coin in res.json()]
    return []

def phân_tích_danh_sách_mã(danh_sách_mã):
    kết_quả = []
    for mã in danh_sách_mã:
        điểm_mua = random.uniform(0, 1)
        điểm_bán = random.uniform(0, 1)
        điểm_ròng = điểm_mua - điểm_bán
        hệ_số_vị_thế = điểm_ròng * 100

        tín_hiệu = "MUA" if điểm_ròng > 0.1 else "BÁN" if điểm_ròng < -0.1 else "TRUNG LẬP"
        độ_tin_cậy = "CAO" if abs(điểm_ròng) > 0.3 else "TRUNG BÌNH"

        kết_quả.append({
            "mã": mã,
            "điểm_mua": round(điểm_mua, 2),
            "điểm_bán": round(điểm_bán, 2),
            "điểm_ròng": round(điểm_ròng, 2),
            "hệ_số_kích_thước_vị_thế": round(hệ_số_vị_thế, 2),
            "tín_hiệu_chính": tín_hiệu,
            "độ_tin_cậy": độ_tin_cậy,
            "thành_phần": {
                "mạng_xã_hội": {
                    "điểm_galaxy": random.randint(50, 90),
                    "xếp_hạng_alt": random.randint(1, 200),
                    "tâm_lý_twitter": random.choice(["Tích cực", "Tiêu cực"]),
                    "tâm_lý_reddit": random.choice(["Tích cực", "Trung lập"]),
                    "tâm_lý_influencer": random.choice(["Tích cực", "Trung lập"]),
                    "lượng_tương_tác_xã_hội": random.randint(1000, 100000)
                },
                "tin_tức": {
                    "số_tin_tích_cực": random.randint(0, 5),
                    "số_tin_tiêu_cực": random.randint(0, 5),
                    "tâm_lý_tin_tức_trung_bình": round(random.uniform(-1, 1), 2),
                    "tin_nóng": [
                        {"tiêu_đề": "Tin tích cực về " + mã, "tâm_lý": "Tốt", "tác_động": "Tăng"},
                        {"tiêu_đề": "Tin tiêu cực về " + mã, "tâm_lý": "Xấu", "tác_động": "Giảm"},
                    ]
                }
            }
        })
    return pd.DataFrame(kết_quả)

def trực_quan_hóa_kết_quả(df):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import streamlit as st

    fig, ax = plt.subplots()
    sns.barplot(data=df, x="mã", y="điểm_ròng", hue="tín_hiệu_chính", ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

    fig2, ax2 = plt.subplots()
    sns.lineplot(data=df, x="mã", y="hệ_số_kích_thước_vị_thế", marker="o", ax=ax2)
    plt.xticks(rotation=90)
    st.pyplot(fig2)
