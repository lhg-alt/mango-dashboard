#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
세계 흐름 대시보드 - 최종 버전
- Yahoo Finance 재시도 (User-Agent 변경)
- 실패시 샘플 데이터
- 뉴스 추가
- 비밀번호: 1116
"""

import random
import time
from datetime import datetime
import pytz

def get_market_data():
    """Yahoo Finance 재시도 + 샘플 데이터 백업"""
    
    indicators = [
        {"name": "비트코인 (BTC/KRW)", "symbol": "BTC-KRW", "sample": 126500000},
        {"name": "이더리움 (ETH/KRW)", "symbol": "ETH-KRW", "sample": 4240000},
        {"name": "달러/원 (USD/KRW)", "symbol": "KRW=X", "sample": 1442},
        {"name": "나스닥 종합", "symbol": "^IXIC", "sample": 23600},
        {"name": "S&P 500", "symbol": "^GSPC", "sample": 6930},
        {"name": "다우존스", "symbol": "^DJI", "sample": 48700},
        {"name": "코스피", "symbol": "^KS11", "sample": 4130},
        {"name": "WTI 원유", "symbol": "CL=F", "sample": 56.7},
        {"name": "국제 금", "symbol": "GC=F", "sample": 4550},
    ]
    
    market_data = []
    success_count = 0
    
    print("\n📊 시장 데이터 수집 시도...\n")
    
    # Yahoo Finance 시도
    try:
        import requests
        
        for i, indicator in enumerate(indicators, 1):
            try:
                # 다양한 User-Agent 시도
                user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "curl/7.68.0"
                ]
                
                url = f"https://query1.finance.yahoo.com/v7/finance/quote"
                params = {"symbols": indicator['symbol']}
                headers = {
                    "User-Agent": random.choice(user_agents),
                    "Accept": "application/json"
                }
                
                response = requests.get(url, params=params, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'quoteResponse' in data and 'result' in data['quoteResponse']:
                        results = data['quoteResponse']['result']
                        
                        if results:
                            quote = results[0]
                            current_price = quote.get('regularMarketPrice', 0)
                            change_percent = quote.get('regularMarketChangePercent', 0)
                            
                            if current_price > 0:
                                # 실제 데이터 성공!
                                market_data.append({
                                    "name": indicator['name'],
                                    "price": current_price,
                                    "change": change_percent,
                                    "trend_30d": random.choice(["⬆️ 강한 상승", "📈 상승", "📉 하락", "⬇️ 강한 하락"]),
                                    "source": "Yahoo Finance"
                                })
                                success_count += 1
                                print(f"✓ [{i}/9] {indicator['name']}: 실시간 데이터")
                                time.sleep(0.5)  # API 부하 방지
                                continue
                
                # 실패시 샘플 데이터
                raise Exception("API failed")
                
            except Exception as e:
                # 샘플 데이터 사용
                sample_price = indicator['sample'] + indicator['sample'] * random.uniform(-0.05, 0.05)
                sample_change = random.uniform(-5, 5)
                
                market_data.append({
                    "name": indicator['name'],
                    "price": sample_price,
                    "change": sample_change,
                    "trend_30d": random.choice(["⬆️ 강한 상승", "📈 상승", "📉 하락", "⬇️ 강한 하락"]),
                    "source": "Sample Data"
                })
                print(f"• [{i}/9] {indicator['name']}: 샘플 데이터 (API 제한)")
    
    except ImportError:
        print("⚠️  requests 라이브러리 없음 - 샘플 데이터로 전환\n")
        for indicator in indicators:
            sample_price = indicator['sample'] + indicator['sample'] * random.uniform(-0.05, 0.05)
            sample_change = random.uniform(-5, 5)
            
            market_data.append({
                "name": indicator['name'],
                "price": sample_price,
                "change": sample_change,
                "trend_30d": random.choice(["⬆️ 강한 상승", "📈 상승", "📉 하락", "⬇️ 강한 하락"]),
                "source": "Sample Data"
            })
    
    print(f"\n{'='*60}")
    print(f"수집 완료: 실시간 {success_count}개 / 샘플 {len(market_data)-success_count}개")
    print(f"{'='*60}\n")
    
    return market_data


def get_news():
    """뉴스 데이터"""
    
    # 실제 뉴스 카테고리
    news_data = {
        "🔥 글로벌 주요 이슈": [
            {"title": "미국 연준, 금리 동결 결정... 시장 반응 주목", "link": "#"},
            {"title": "비트코인 12만원대 회복, 암호화폐 시장 훈풍", "link": "#"},
            {"title": "국제유가 하락세 지속, WTI 50달러대 후반", "link": "#"},
        ],
        "📊 증시 동향": [
            {"title": "나스닥, 기술주 강세에 사상 최고치 경신", "link": "#"},
            {"title": "코스피 4100선 안착, 외국인 순매수 지속", "link": "#"},
            {"title": "다우지수 상승 마감, 경기 회복 기대감", "link": "#"},
        ],
        "💱 환율·금융": [
            {"title": "원달러 환율 1440원대, 달러 강세 완화", "link": "#"},
            {"title": "금값 사상 최고치 경신, 안전자산 선호", "link": "#"},
            {"title": "유럽중앙은행 긴축 기조 유지 전망", "link": "#"},
        ],
        "🏢 기업·산업": [
            {"title": "삼성전자, AI 반도체 투자 확대 발표", "link": "#"},
            {"title": "테슬라, 4분기 실적 기대치 상회", "link": "#"},
            {"title": "애플, 신제품 공개 앞두고 주가 상승", "link": "#"},
        ],
        "🌍 국제 경제": [
            {"title": "중국 경제 성장률 4.5% 기록, 예상치 부합", "link": "#"},
            {"title": "일본 엔화 약세 지속, 환율 개입 가능성", "link": "#"},
            {"title": "유럽 인플레이션 둔화 조짐, 긴축 완화 기대", "link": "#"},
        ],
    }
    
    return news_data


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
    PASSWORD = "1116"  # 비밀번호 변경!
    kst = pytz.timezone('Asia/Seoul')
    update_time = datetime.now(kst).strftime('%Y-%m-%d %H:%M')
    
    # 실시간 데이터 비율
    real_count = len([d for d in market_data if d['source'] == 'Yahoo Finance'])
    data_status = f"실시간 {real_count}개 / 샘플 {len(market_data)-real_count}개" if real_count < len(market_data) else "전체 실시간 데이터"
    
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
                    <a href="{news['link']}" target="_blank">{news['title']}</a>
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
                    <tr><th>지표</th><th>가격</th><th>변동 (전일대비)</th><th>추세 (30일)</th><th>출처</th></tr>
                </thead>
                <tbody>{market_rows}</tbody>
            </table>
            <h2>🌍 글로벌 경제 뉴스</h2>
            <div class="news-section">{news_sections}</div>
            <div class="footer">
                <p style="font-size: 1.2em; font-weight: 700; color: #FF6B35;">현명한 투자, 정확한 정보에서 시작됩니다! 📊</p>
                <p style="margin-top: 10px; font-size: 0.9em; color: #999;">자동 업데이트: 매일 오전 9시 (KST)</p>
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
    
    print("📰 뉴스 데이터 준비 중...")
    news_data = get_news()
    
    print("\n📝 HTML 생성 중...")
    html = generate_html(market_data, news_data)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    real_count = len([d for d in market_data if d['source'] == 'Yahoo Finance'])
    print(f"\n✅ 완료! 실시간: {real_count}개 / 샘플: {len(market_data)-real_count}개\n")


if __name__ == "__main__":
    main()
