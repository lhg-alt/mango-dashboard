#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
세계 흐름 대시보드 - 샘플 데이터 버전
Yahoo Finance API 차단 우회
"""

import random
from datetime import datetime, timedelta
import pytz

def get_market_data():
    """샘플 시장 데이터 생성"""
    
    print("\n" + "="*60)
    print("⚠️  Yahoo Finance API가 GitHub Actions를 차단했습니다")
    print("   대신 샘플 데이터로 대시보드를 생성합니다")
    print("="*60 + "\n")
    
    # 현실적인 샘플 데이터
    market_data = [
        {
            "name": "비트코인 (BTC/KRW)",
            "price": 126500000 + random.randint(-1000000, 1000000),
            "change": random.uniform(-5, 5),
            "trend_30d": random.choice(["⬆️ 강한 상승", "📈 상승", "📉 하락", "⬇️ 강한 하락"]),
            "source": "Sample Data"
        },
        {
            "name": "이더리움 (ETH/KRW)",
            "price": 4240000 + random.randint(-50000, 50000),
            "change": random.uniform(-5, 5),
            "trend_30d": random.choice(["⬆️ 강한 상승", "📈 상승", "📉 하락"]),
            "source": "Sample Data"
        },
        {
            "name": "달러/원 (USD/KRW)",
            "price": 1442 + random.uniform(-10, 10),
            "change": random.uniform(-2, 2),
            "trend_30d": random.choice(["📈 상승", "📉 하락"]),
            "source": "Sample Data"
        },
        {
            "name": "나스닥 종합",
            "price": 23600 + random.randint(-200, 200),
            "change": random.uniform(-2, 3),
            "trend_30d": random.choice(["⬆️ 강한 상승", "📈 상승"]),
            "source": "Sample Data"
        },
        {
            "name": "S&P 500",
            "price": 6930 + random.randint(-50, 50),
            "change": random.uniform(-1, 2),
            "trend_30d": random.choice(["📈 상승", "📉 하락"]),
            "source": "Sample Data"
        },
        {
            "name": "다우존스",
            "price": 48700 + random.randint(-300, 300),
            "change": random.uniform(-2, 3),
            "trend_30d": random.choice(["⬆️ 강한 상승", "📈 상승"]),
            "source": "Sample Data"
        },
        {
            "name": "코스피",
            "price": 4130 + random.randint(-50, 50),
            "change": random.uniform(-3, 4),
            "trend_30d": random.choice(["📈 상승", "📉 하락"]),
            "source": "Sample Data"
        },
        {
            "name": "WTI 원유",
            "price": 56.7 + random.uniform(-2, 2),
            "change": random.uniform(-4, 3),
            "trend_30d": random.choice(["📉 하락", "⬇️ 강한 하락"]),
            "source": "Sample Data"
        },
        {
            "name": "국제 금",
            "price": 4550 + random.randint(-100, 100),
            "change": random.uniform(-1, 10),
            "trend_30d": random.choice(["⬆️ 강한 상승", "📈 상승"]),
            "source": "Sample Data"
        },
    ]
    
    print("📊 샘플 데이터 생성 완료:")
    for i, data in enumerate(market_data, 1):
        print(f"  [{i}/9] {data['name']}: {data['price']:,.2f} ({data['change']:+.2f}%)")
    
    return market_data


def get_news():
    """샘플 뉴스"""
    return {
        "📰 경제 뉴스": [
            {
                "title": "⚠️ 실시간 데이터는 Yahoo Finance API 제한으로 일시 중단되었습니다",
                "link": "#",
                "source": "시스템"
            },
            {
                "title": "💡 대시보드는 매일 자동 업데이트되며, 곧 실시간 데이터로 복구될 예정입니다",
                "link": "#",
                "source": "시스템"
            }
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
    if price >= 1000:
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
        .news-category {{ margin: 30px 0; padding: 25px; background: #fff3cd; border-radius: 16px; border-left: 5px solid #ffc107; }}
        .news-category h3 {{ font-size: 1.5em; margin-bottom: 15px; }}
        .news-item {{ padding: 12px 0; border-bottom: 1px solid #e0e0e0; }}
        .news-item a {{ color: #333; text-decoration: none; display: block; }}
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
            <div class="update-time">기준 시각: {update_time} (샘플 데이터)</div>
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
    print("🚀 세계 흐름 대시보드 업데이트 시작...\n")
    
    print("📊 시장 데이터 생성 중...")
    market_data = get_market_data()
    
    print("\n📰 뉴스 데이터 준비 중...")
    news_data = get_news()
    
    print("\n📝 HTML 생성 중...")
    html = generate_html(market_data, news_data)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ 완료! 샘플 데이터로 대시보드 생성\n")


if __name__ == "__main__":
    main()
