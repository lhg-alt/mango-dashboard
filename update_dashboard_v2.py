#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
세계 흐름 대시보드 - 안정 버전
정적 샘플 데이터로 테스트
"""

import json
import requests
from datetime import datetime
import pytz
import random

def get_market_data():
    """시장 데이터 수집 - 개선된 버전"""
    indicators = [
        {"name": "비트코인 (BTC/KRW)", "symbol": "BTC-KRW"},
        {"name": "이더리움 (ETH/KRW)", "symbol": "ETH-KRW"},
        {"name": "달러/원 (USD/KRW)", "symbol": "KRW=X"},
        {"name": "나스닥 종합", "symbol": "^IXIC"},
        {"name": "S&P 500", "symbol": "^GSPC"},
        {"name": "다우존스", "symbol": "^DJI"},
        {"name": "코스피", "symbol": "^KS11"},
        {"name": "WTI 원유", "symbol": "CL=F"},
        {"name": "국제 금", "symbol": "GC=F"},
    ]
    
    market_data = []
    
    for indicator in indicators:
        try:
            # Yahoo Finance v7 API 사용 (더 안정적)
            url = f"https://query1.finance.yahoo.com/v7/finance/quote"
            params = {"symbols": indicator['symbol']}
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            data = response.json()
            
            if 'quoteResponse' in data and 'result' in data['quoteResponse']:
                results = data['quoteResponse']['result']
                if results:
                    quote = results[0]
                    
                    current_price = quote.get('regularMarketPrice', 0)
                    previous_close = quote.get('regularMarketPreviousClose', 0)
                    change_percent = quote.get('regularMarketChangePercent', 0)
                    
                    # 백업: 직접 계산
                    if change_percent == 0 and current_price > 0 and previous_close > 0:
                        change_percent = ((current_price - previous_close) / previous_close) * 100
                    
                    # 30일 추세는 별도 API 호출
                    trend_30d = get_trend_30d(indicator['symbol'])
                    
                    market_data.append({
                        "name": indicator['name'],
                        "price": current_price,
                        "change": change_percent,
                        "trend_30d": trend_30d,
                        "source": "Yahoo Finance"
                    })
                    
                    print(f"✓ {indicator['name']}: {current_price:,.2f} ({change_percent:+.2f}%)")
                else:
                    raise Exception("No results")
                    
        except Exception as e:
            print(f"✗ {indicator['name']}: {str(e)}")
            # 실패시 샘플 데이터
            market_data.append({
                "name": indicator['name'],
                "price": 0,
                "change": 0,
                "trend_30d": "데이터 수집 중",
                "source": "Yahoo Finance"
            })
    
    return market_data


def get_trend_30d(symbol):
    """30일 추세 계산"""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        params = {"interval": "1d", "range": "1mo"}
        headers = {"User-Agent": "Mozilla/5.0"}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if 'chart' in data and 'result' in data['chart']:
            result = data['chart']['result'][0]
            quotes = result.get('indicators', {}).get('quote', [{}])[0]
            closes = [c for c in quotes.get('close', []) if c is not None]
            
            if len(closes) >= 2:
                start_price = closes[0]
                end_price = closes[-1]
                if start_price > 0:
                    trend_change = ((end_price - start_price) / start_price) * 100
                    if trend_change > 5:
                        return "⬆️ 강한 상승"
                    elif trend_change > 0:
                        return "📈 상승"
                    elif trend_change > -5:
                        return "📉 하락"
                    else:
                        return "⬇️ 강한 하락"
    except:
        pass
    
    return ""


def get_news():
    """뉴스 플레이스홀더"""
    return {
        "📰 경제 뉴스": [
            {"title": "실시간 뉴스는 추후 업데이트 예정입니다.", "link": "#", "source": "시스템"}
        ]
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
    if price == 0:
        return '<span style="color: #999;">데이터 수집 중</span>'
    elif price >= 1000:
        return f"{price:,.0f}"
    elif price >= 1:
        return f"{price:,.2f}"
    else:
        return f"{price:.4f}"


def generate_html(market_data, news_data):
    """HTML 생성"""
    PASSWORD = "mango2025"
    kst = pytz.timezone('Asia/Seoul')
    update_time = datetime.now(kst).strftime('%Y-%m-%d %H:%M')
    
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
            news_items = "".join([f'<div class="news-item"><a href="{n["link"]}">{n["title"]}</a></div>' for n in news_list])
            news_sections += f'<div class="news-category"><h3>{category}</h3>{news_items}</div>'
    
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
        .update-time {{ text-align: center; color: #666; margin-bottom: 30px; }}
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
        .news-category h3 {{ font-size: 1.5em; margin-bottom: 15px; }}
        .news-item {{ padding: 12px 0; border-bottom: 1px solid #e0e0e0; }}
        .news-item a {{ color: #333; text-decoration: none; display: block; transition: color 0.3s; }}
        .news-item a:hover {{ color: #FF6B35; padding-left: 10px; }}
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
            <div class="greeting">
                <h3>세계 경제, 한눈에! 🌏</h3>
                <p>최신 <strong>글로벌 금융 데이터</strong>를 실시간으로 제공합니다!</p>
            </div>
            <h2>📊 핵심 지표 라이브</h2>
            <table>
                <thead>
                    <tr><th>지표</th><th>가격</th><th>변동 (전일대비)</th><th>추세 (30일)</th><th>출처</th></tr>
                </thead>
                <tbody>{market_rows}</tbody>
            </table>
            <h2>🌍 경제 뉴스</h2>
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
    print("🚀 세계 흐름 대시보드 업데이트 시작...")
    print("\n📊 시장 데이터 수집 중...")
    
    market_data = get_market_data()
    news_data = get_news()
    
    print("\n📝 HTML 생성 중...")
    html = generate_html(market_data, news_data)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    success_count = len([d for d in market_data if d['price'] > 0])
    print(f"\n✅ 완료! 성공: {success_count}/{len(market_data)}개")


if __name__ == "__main__":
    main()
