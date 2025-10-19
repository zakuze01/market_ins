import os
import requests
import pandas as pd

LUNAR_API_KEY = "z6sz4fzdeohc5f5r5lflxelygmgxo6ac5a4gjpfi"
CRYPTOPANIC_API_KEY = "89a992580a65612dd01af5b885e02b578965e23b"
NEWS_API_KEY = "be8a5006af7d42f69dc7284f5cd3f38e"
ALPHA_API_KEY = "ZP0JGOAQ48UR7A2B"

def lay_top_coin(limit=30):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        data = res.json()
        return [coin["symbol"].upper() for coin in data[:limit]]
    return []

def lay_sentiment_lunarcrush(symbols):
    url = "https://api.lunarcrush.com/v2"
    params = {
        "data": "assets",
        "key": LUNAR_API_KEY,
        "symbol": ",".join(symbols)
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        raw = res.json().get("data", [])
        return {item["symbol"]: item for item in raw}
    return {}

def lay_tin_tuc_newsapi():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "crypto",
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": NEWS_API_KEY
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json().get("articles", [])[:10]
    return []

def lay_tin_tuc_cryptopanic():
    url = "https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": CRYPTOPANIC_API_KEY,
        "filter": "hot",
        "currencies": "BTC,ETH"
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json().get("results", [])
    return []

def lay_fear_greed_index():
    url = "https://api.alternative.me/fng/"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json().get("data", [])
        if data:
            return data[0]
    return {}

def phan_tich_danh_sach_mã(danh_sach_mã):
    sentiment_data = lay_sentiment_lunarcrush(danh_sach_mã)
    kết_quả = []

    for mã in danh_sách_mã:
        dữ_liệu = sentiment_data.get(mã, {})
        galaxy = dữ_liệu.get("galaxy_score", 0)
        alt_rank = dữ_liệu.get("alt_rank", 1000)

        điểm_ròng = galaxy / 100 - alt_rank / 1000
        hệ_số = điểm_ròng * 100
        tín_hiệu = "MUA" if điểm_ròng > 0.1 else "BÁN" if điểm_ròng < -0.1 else "TRUNG LẬP"
        độ_tin_cậy = "CAO" if abs(điểm_ròng) > 0.3 else "TRUNG BÌNH"

        kết_quả.append({
            "mã": mã,
            "galaxy_score": galaxy,
            "alt_rank": alt_rank,
            "điểm_ròng": round(điểm_ròng, 2),
            "hệ_số_kích_thước_vị_thế": round(hệ_số, 2),
            "tín_hiệu_chính": tín_hiệu,
            "độ_tin_cậy": độ_tin_cậy
        })
    return pd.DataFrame(kết_quả)
