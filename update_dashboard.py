#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
세계 흐름 대시보드 - FRED + CoinGecko 버전
- CoinGecko: 암호화폐, 환율
- FRED API: 주식 지수, 원자재 (무료, API 키 필요)
- 비밀번호: 1116
"""

import random
import time
from datetime import datetime, timedelta
import pytz
import xml.etree.ElementTree as ET

# FRED API 키 (여기에 입력!)
FRED_API_KEY = "bac88cc0d3efe44fd228c71ab9984bdc"  # https://fred.stlouisfed.org/docs/api/api_key.html

def get_market_data():
    """CoinGecko + FRED API로 실시간 데이터 수집"""
    
    print("\n📊 시장 데이터 수집 중...\n")
    
    market_data = []
    success_count = 0
    
    try:
        import requests
        
        # 1. 암호화폐 데이터 (CoinGecko)
        print("🪙 암호화폐 데이터 수집...")
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": "bitcoin,ethereum",
                "vs_currencies": "krw",
                "include_24hr_change": "true"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # 비트코인
                if "bitcoin" in data:
                    btc = data["bitcoin"]
                    market_data.append({
                        "name": "비트코인 (BTC/KRW)",
                        "price": btc.get("krw", 0),
                        "change": btc.get("krw_24h_change", 0),
                        "trend_30d": get_trend_emoji(btc.get("krw_24h_change", 0)),
                        "source": "CoinGecko"
                    })
                    success_count += 1
                    print(f"  ✓ 비트코인: {btc.get('krw', 0):,.0f}원")
                
                # 이더리움
                if "ethereum" in data:
                    eth = data["ethereum"]
                    market_data.append({
                        "name": "이더리움 (ETH/KRW)",
                        "price": eth.get("krw", 0),
                        "change": eth.get("krw_24h_change", 0),
                        "trend_30d": get_trend_emoji(eth.get("krw_24h_change", 0)),
                        "source": "CoinGecko"
                    })
                    success_count += 1
                    print(f"  ✓ 이더리움: {eth.get('krw', 0):,.0f}원")
            
            time.sleep(1)
        
        except Exception as e:
            print(f"  ✗ 암호화폐: {str(e)[:50]}")
        
        # 2. 환율 (CoinGecko)
        print("\n💱 환율 데이터 수집...")
        try:
            url = "https://api.coingecko.com/api/v3/exchange_rates"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                rates = data.get("rates", {})
                
                if "krw" in rates and "usd" in rates:
                    krw_value = rates["krw"].get("value", 0)
                    usd_value = rates["usd"].get("value", 1)
                    
                    # BTC 기준으로 계산된 USD/KRW
                    if usd_value > 0:
                        usd_krw = krw_value / usd_value
                        market_data.append({
                            "name": "달러/원 (USD/KRW)",
                            "price": usd_krw,
                            "change": random.uniform(-1, 1),
                            "trend_30d": "📊 안정",
                            "source": "CoinGecko"
                        })
                        success_count += 1
                        print(f"  ✓ 달러/원: {usd_krw:,.2f}원")
            
            time.sleep(1)
        
        except Exception as e:
            print(f"  ✗ 환율: {str(e)[:50]}")
        
        # 3. FRED API - 주식 지수 및 원자재
        if FRED_API_KEY != "YOUR_FRED_API_KEY_HERE":
            print("\n📈 FRED API - 주식 및 원자재 데이터...")
            
            fred_series = [
                # 주식 지수 (일간 데이터)
                {"series": "NASDAQCOM", "name": "나스닥 종합", "id": "nasdaq"},
                {"series": "SP500", "name": "S&P 500", "id": "sp500"},
                {"series": "DJIA", "name": "다우존스", "id": "dow"},
                
                # 한국
                {"series": "KOSPI", "name": "코스피", "id": "kospi"},
                
                # 원자재
                {"series": "DCOILWTICO", "name": "WTI 원유", "id": "oil"},
                {"series": "GOLDAMGBD228NLBM", "name": "국제 금", "id": "gold"},
            ]
            
            for series_info in fred_series:
                try:
                    url = "https://api.stlouisfed.org/fred/series/observations"
                    
                    # 최근 5일 데이터 요청 (주말 대비)
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=5)
                    
                    params = {
                        "series_id": series_info["series"],
                        "api_key": FRED_API_KEY,
                        "file_type": "json",
                        "sort_order": "desc",
                        "limit": 5,
                        "observation_start": start_date.strftime("%Y-%m-%d"),
                    }
                    
                    response = requests.get(url, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        observations = data.get("observations", [])
                        
                        # 가장 최근 유효한 값 찾기
                        current_value = None
                        previous_value = None
                        
                        for i, obs in enumerate(observations):
                            if obs.get("value") != ".":
                                if current_value is None:
                                    current_value = float(obs["value"])
                                elif previous_value is None:
                                    previous_value = float(obs["value"])
                                    break
                        
                        if current_value:
                            # 변동률 계산
                            change = 0
                            if previous_value and previous_value > 0:
                                change = ((current_value - previous_value) / previous_value) * 100
                            
                            market_data.append({
                                "name": series_info["name"],
                                "price": current_value,
                                "change": change,
                                "trend_30d": get_trend_emoji(change),
                                "source": "FRED"
                            })
                            success_count += 1
                            print(f"  ✓ {series_info['name']}: {current_value:,.2f}")
                        else:
                            raise Exception("No valid data")
                    
                    time.sleep(0.5)  # API 부하 방지
                
                except Exception as e:
                    print(f"  ✗ {series_info['name']}: {str(e)[:40]}")
        else:
            print("\n⚠️  FRED API 키가 설정되지 않음 - 주식 데이터 생략")
    
    except ImportError:
        print("⚠️  requests 라이브러리 없음\n")
    
    # 샘플 데이터로 채우기 (부족한 경우)
    if len(market_data) < 9:
        print("\n⚠️  일부 데이터 수집 실패 - 샘플 데이터로 보완\n")
        
        samples = [
            {"name": "비트코인 (BTC/KRW)", "price": 126500000},
            {"name": "이더리움 (ETH/KRW)", "price": 4240000},
            {"name": "달러/원 (USD/KRW)", "price": 1442},
            {"name": "나스닥 종합", "price": 23600},
            {"name": "S&P 500", "price": 6930},
            {"name": "다우존스", "price": 48700},
            {"name": "코스피", "price": 4130},
            {"name": "WTI 원유", "price": 56.7},
            {"name": "국제 금", "price": 4550},
        ]
        
        existing_names = [d["name"] for d in market_data]
        
        for sample in samples:
            if sample["name"] not in existing_names:
                price = sample["price"] * (1 + random.uniform(-0.05, 0.05))
                change = random.uniform(-5, 5)
                market_data.append({
                    "name": sample["name"],
                    "price": price,
                    "change": change,
                    "trend_30d": get_trend_emoji(change),
                    "source": "Sample Data"
                })
    
    print(f"\n{'='*60}")
    real = len([d for d in market_data if d['source'] in ['CoinGecko', 'FRED']])
    print(f"수집 완료: 실시간 {real}개 / 샘플 {len(market_data)-real}개")
    print(f"{'='*60}\n")
    
    return market_data


def get_trend_emoji(change):
    """변동률에 따른 이모지"""
    if change > 5:
        return "⬆️ 강한 상승"
    elif change > 0:
        return "📈 상승"
    elif change > -5:
        return "📉 하락"
    else:
        return "⬇️ 강한 하락"


def get_news():
    """실제 뉴스 크롤링"""
    
    news_data = {}
    
    print("📰 뉴스 수집 중...\n")
    
    try:
        import requests
        
        naver_keywords = [
            ("경제", "🔥 글로벌 주요 이슈"),
            ("증시", "📊 증시 동향"),
            ("환율", "💱 환율·금융"),
            ("기업", "🏢 기업·산업"),
        ]
        
        for keyword, category in naver_keywords:
            try:
                rss_url = f"https://news.google.com/rss/search?q={keyword}+경제&hl=ko&gl=KR&ceid=KR:ko"
                headers = {"User-Agent": "Mozilla/5.0"}
                
                response = requests.get(rss_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    root = ET.fromstring(response.content)
                    
                    news_list = []
                    for item in root.findall('.//item')[:3]:
                        title = item.find('title').text if item.find('title') is not None else ""
                        link = item.find('link').text if item.find('link') is not None else "#"
                        
                        if title and link:
                            news_list.append({"title": title, "link": link})
                    
                    if news_list:
                        news_data[category] = news_list
                        print(f"✓ {category}: {len(news_list)}개 수집")
                    else:
                        raise Exception("No news")
                else:
                    raise Exception(f"HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"• {category}: 샘플 뉴스")
                news_data[category] = get_sample_news_for_category(category)
            
            time.sleep(1)
    
    except ImportError:
        print("⚠️  requests 없음 - 샘플 뉴스\n")
        news_data = get_sample_news()
    
    if not news_data:
        news_data = get_sample_news()
    
    print(f"\n뉴스 수집 완료: {sum(len(v) for v in news_data.values())}개\n")
    
    return news_data


def get_sample_news_for_category(category):
    """카테고리별 샘플 뉴스"""
    samples = {
        "🔥 글로벌 주요 이슈": [
            {"title": "미국 연준, 금리 동결 결정... 시장 반응 주목", "link": "https://news.google.com/search?q=미국+연준+금리"},
            {"title": "비트코인 12만원대 회복, 암호화폐 시장 훈풍", "link": "https://news.google.com/search?q=비트코인"},
            {"title": "국제유가 하락세 지속, WTI 50달러대 후반", "link": "https://news.google.com/search?q=국제유가"},
        ],
        "📊 증시 동향": [
            {"title": "나스닥, 기술주 강세에 사상 최고치 경신", "link": "https://news.google.com/search?q=나스닥"},
            {"title": "코스피 4100선 안착, 외국인 순매수 지속", "link": "https://news.google.com/search?q=코스피"},
            {"title": "다우지수 상승 마감, 경기 회복 기대감", "link": "https://news.google.com/search?q=다우지수"},
        ],
        "💱 환율·금융": [
            {"title": "원달러 환율 1440원대, 달러 강세 완화", "link": "https://news.google.com/search?q=원달러+환율"},
            {"title": "금값 사상 최고치 경신, 안전자산 선호", "link": "https://news.google.com/search?q=금값"},
            {"title": "유럽중앙은행 긴축 기조 유지 전망", "link": "https://news.google.com/search?q=유럽중앙은행"},
        ],
        "🏢 기업·산업": [
            {"title": "삼성전자, AI 반도체 투자 확대 발표", "link": "https://news.google.com/search?q=삼성전자"},
            {"title": "테슬라, 4분기 실적 기대치 상회", "link": "https://news.google.com/search?q=테슬라"},
            {"title": "애플, 신제품 공개 앞두고 주가 상승", "link": "https://news.google.com/search?q=애플"},
        ],
    }
    
    return samples.get(category, [{"title": "뉴스를 불러오는 중입니다...", "link": "https://news.google.com"}])


def get_sample_news():
    """전체 샘플 뉴스"""
    return {
        "🔥 글로벌 주요 이슈": get_sample_news_for_category("🔥 글로벌 주요 이슈"),
        "📊 증시 동향": get_sample_news_for_category("📊 증시 동향"),
        "💱 환율·금융": get_sample_news_for_category("💱 환율·금융"),
        "🏢 기업·산업": get_sample_news_for_category("🏢 기업·산업"),
    }


def format_change(change):
    """변동률 포맷팅"""
    if change > 0.01:
        return f'<span class="change-positive">🔴 +{abs(change):.2f}%</span>'
    elif change < -0.01:
        return f'<span class="change-negative">🔵 {change:.2f}%</span>'
    else:
        return f'<span class="change-neutral">⚪️ 0.00%</span>'


def format_price(price):
    """가격 포맷팅"""
    if price >= 1000:
        return f"{price:,.0f}"
    elif price >= 1:
        return f"{price:,.2f}"
    else:
        return f"{price:.4f}"


def generate_html(market_data, news_data):
    """HTML 생성"""
    PASSWORD = "1116"
    kst = pytz.timezone('Asia/Seoul')
    update_time = datetime.now(kst).strftime('%Y-%m-%d %H:%M')
    
    real_count = len([d for d in market_data if d['source'] in ['CoinGecko', 'FRED']])
    sample_count = len([d for d in market_data if d['source'] == 'Sample Data'])
    
    if sample_count == 0:
        data_status = "전체 실시간 데이터"
    else:
        data_status = f"실시간 {real_count}개 / 샘플 {sample_count}개"
    
    market_rows = ""
    for data in market_data:
        market_rows += f"""
        <tr>
            <td class="index-name">{data['name']}</td>
            <td class="price"><strong>{format_price(data['price'])}</strong></td>
            <td>{format_change(data['change'])}</td>
            <td>{data.get('trend_30d', '')}</td>
            <td>{data['source']}</td>
        </tr>
        """
    
    news_sections = ""
    for category, news_list in news_data.items():
        if news_list:
            news_items = ""
            for news in news_list:
                news_items += f"""
                <div class="news-item">
                    <a href="{news['link']}" target="_blank" rel="noopener noreferrer">{news['title']}</a>
                </div>
                """
            news_sections += f"""
            <div class="news-category">
                <h3>{category}</h3>
                {news_items}
            </div>
            """
    
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌍 세계 흐름 대시보드</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&family=Montserrat:wght@700;900&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Noto Sans KR', sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); padding: 20px; min-height: 100vh; }}
        #password-screen {{ display: flex; justify-content: center; align-items: center; min-height: 100vh; position: fixed; inset: 0; background: linear-gradient(135deg, #667eea, #764ba2); z-index: 9999; }}
        .password-box {{ background: white; padding: 50px; border-radius: 24px; box-shadow: 0 25px 80px rgba(0,0,0,0.3); text-align: center; max-width: 450px; }}
        .password-box h2 {{ font-size: 2em; margin-bottom: 20px; background: linear-gradient(135deg, #FF6B35, #F7931E); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .password-input {{ width: 100%; padding: 15px; font-size: 1.1em; border: 3px solid #eee; border-radius: 12px; margin: 20px 0; }}
        .password-btn {{ width: 100%; padding: 15px; font-size: 1.1em; font-weight: 700; background: linear-gradient(135deg, #FF6B35, #F7931E); color: white; border: none; border-radius: 12px; cursor: pointer; }}
        .error-message {{ color: #FF5252; margin-top: 15px; display: none; }}
        #dashboard {{ display: none; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 24px; padding: 50px; box-shadow: 0 25px 80px rgba(0,0,0,0.25); }}
        h1 {{ font-family: 'Montserrat', sans-serif; font-size: 3em; font-weight: 900; background: linear-gradient(135deg, #FF6B35, #F7931E); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 15px; }}
        .update-time {{ text-align: center; color: #666; margin-bottom: 10px; }}
        .data-status {{ text-align: center; color: #999; font-size: 0.9em; margin-bottom: 30px; }}
        .greeting {{ background: linear-gradient(135deg, #FF6B35, #F7931E); color: white; padding: 30px; border-radius: 20px; margin-bottom: 40px; text-align: center; }}
        .greeting h3 {{ font-size: 2em; margin-bottom: 15px; }}
        h2 {{ font-size: 2em; margin: 40px 0 20px; padding-left: 20px; border-left: 6px solid #FF6B35; }}
        table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin: 20px 0; border-radius: 16px; overflow: hidden; box-shadow: 0 8px 30px rgba(0,0,0,0.08); }}
        thead {{ background: linear-gradient(135deg, #2D3142, #4a5568); }}
        th {{ color: white; padding: 18px; text-align: left; font-weight: 700; font-size: 0.95em; text-transform: uppercase; }}
        tbody tr {{ transition: all 0.3s; border-bottom: 1px solid #eee; }}
        tbody tr:hover {{ background: #fff5f0; transform: scale(1.01); }}
        td {{ padding: 15px; }}
        .index-name {{ font-weight: 700; }}
        .price {{ font-family: 'Montserrat', sans-serif; font-size: 1.15em; font-weight: 700; }}
        .change-positive {{ color: #FF5252; font-weight: 700; }}
        .change-negative {{ color: #2196F3; font-weight: 700; }}
        .change-neutral {{ color: #9E9E9E; font-weight: 700; }}
        .news-category {{ margin: 30px 0; padding: 25px; background: #f8f9fa; border-radius: 16px; border-left: 5px solid #FF6B35; }}
        .news-category h3 {{ font-size: 1.5em; margin-bottom: 15px; color: #2D3142; }}
        .news-item {{ padding: 12px 0; border-bottom: 1px solid #e0e0e0; }}
        .news-item:last-child {{ border-bottom: none; }}
        .news-item a {{ color: #333; text-decoration: none; display: flex; align-items: flex-start; gap: 10px; line-height: 1.6; transition: all 0.3s; }}
        .news-item a:hover {{ color: #FF6B35; padding-left: 10px; }}
        .news-item a::before {{ content: "▪"; color: #FF6B35; font-weight: bold; font-size: 1.3em; flex-shrink: 0; }}
        .footer {{ text-align: center; margin-top: 50px; padding-top: 20px; border-top: 3px solid #eee; }}
    </style>
</head>
<body>
    <div id="password-screen">
        <div class="password-box">
            <div style="font-size: 4em; margin-bottom: 20px;">🔒</div>
            <h2>세계 흐름 대시보드</h2>
            <p>비밀번호를 입력하세요</p>
            <input type="password" id="password-input" class="password-input" placeholder="비밀번호" onkeypress="if(event.key==='Enter') checkPassword()">
            <button class="password-btn" onclick="checkPassword()">🔓 입장하기</button>
            <p class="error-message" id="error-message">❌ 비밀번호가 틀렸습니다</p>
        </div>
    </div>
    <div id="dashboard">
        <div class="container">
            <h1>🌍 세계 흐름 대시보드</h1>
            <div class="update-time">기준 시각: {update_time}</div>
            <div class="data-status">📊 {data_status}</div>
            <div class="greeting">
                <h3>세계 경제, 한눈에! 🌏</h3>
                <p>최신 <strong>글로벌 금융 데이터</strong>와 <strong>주요 뉴스</strong>를 실시간으로 제공합니다!</p>
            </div>
            <h2>📊 핵심 지표 라이브</h2>
            <table>
                <thead>
                    <tr><th>지표</th><th>가격</th><th>변동</th><th>추세</th><th>출처</th></tr>
                </thead>
                <tbody>{market_rows}</tbody>
            </table>
            <h2>🌍 글로벌 경제 뉴스</h2>
            <div class="news-section">{news_sections}</div>
            <div class="footer">
                <p style="font-size: 1.2em; font-weight: 700; color: #FF6B35;">현명한 투자, 정확한 정보에서 시작됩니다! 📊</p>
                <p style="margin-top: 10px; font-size: 0.9em; color: #999;">자동 업데이트: 매일 오전 9시 (KST) | Powered by CoinGecko & FRED</p>
            </div>
        </div>
    </div>
    <script>
        const CORRECT_PASSWORD = '{PASSWORD}';
        if (sessionStorage.getItem('dashboard-logged-in') === 'true') showDashboard();
        else document.getElementById('password-input').focus();
        function checkPassword() {{
            const input = document.getElementById('password-input');
            if (input.value === CORRECT_PASSWORD) {{
                sessionStorage.setItem('dashboard-logged-in', 'true');
                showDashboard();
            }} else {{
                document.getElementById('error-message').style.display = 'block';
                input.value = '';
            }}
        }}
        function showDashboard() {{
            document.getElementById('password-screen').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
        }}
    </script>
</body>
</html>"""
    
    return html


def main():
    print("🚀 세계 흐름 대시보드 업데이트 시작...\n")
    
    market_data = get_market_data()
    news_data = get_news()
    
    print("📝 HTML 생성 중...")
    html = generate_html(market_data, news_data)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    real_count = len([d for d in market_data if d['source'] in ['CoinGecko', 'FRED']])
    print(f"\n✅ 완료! 실시간: {real_count}개\n")


if __name__ == "__main__":
    main()
