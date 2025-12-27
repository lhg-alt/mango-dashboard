#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
망고 대시보드 자동 업데이트 스크립트
매일 자동으로 최신 금융 데이터와 뉴스를 수집하여 HTML 생성
"""

import json
import requests
from datetime import datetime
import pytz

def get_market_data():
    """Yahoo Finance API를 통해 시장 데이터 수집"""
    indicators = [
        {"name": "비트코인 (BTC/KRW)", "symbol": "BTC-KRW"},
        {"name": "이더리움 (ETH/KRW)", "symbol": "ETH-KRW"},
        {"name": "달러 지수 (DXY)", "symbol": "DX-Y.NYB"},
        {"name": "달러/원 (USD/KRW)", "symbol": "KRW=X"},
        {"name": "엔/원 (JPY/KRW)", "symbol": "JPYKRW=X"},
        {"name": "위안/원 (CNY/KRW)", "symbol": "CNYKRW=X"},
        {"name": "유로/원 (EUR/KRW)", "symbol": "EURKRW=X"},
        {"name": "나스닥 종합", "symbol": "^IXIC"},
        {"name": "S&P 500", "symbol": "^GSPC"},
        {"name": "다우존스", "symbol": "^DJI"},
        {"name": "니케이 225", "symbol": "^N225"},
        {"name": "상해종합", "symbol": "000001.SS"},
        {"name": "코스피", "symbol": "^KS11"},
        {"name": "WTI 원유", "symbol": "CL=F"},
        {"name": "국제 금", "symbol": "GC=F"},
        {"name": "미국 국채 10년", "symbol": "^TNX"},
        {"name": "미국 국채 2년", "symbol": "^IRX"}
    ]
    
    market_data = []
    
    for indicator in indicators:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{indicator['symbol']}"
            params = {
                "interval": "1d",
                "range": "2d"
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                result = data['chart']['result'][0]
                meta = result.get('meta', {})
                
                current_price = meta.get('regularMarketPrice', 0)
                previous_close = meta.get('previousClose', 0)
                
                if previous_close and previous_close > 0:
                    change_percent = ((current_price - previous_close) / previous_close) * 100
                else:
                    change_percent = 0
                
                market_data.append({
                    "name": indicator['name'],
                    "price": current_price,
                    "change": change_percent,
                    "source": "Yahoo Finance"
                })
        except Exception as e:
            print(f"Error fetching {indicator['name']}: {e}")
            market_data.append({
                "name": indicator['name'],
                "price": 0,
                "change": 0,
                "source": "Yahoo Finance"
            })
    
    return market_data


def get_news():
    """Google News RSS에서 경제 뉴스 수집"""
    news_categories = {
        "📆 일정": [],
        "🥔 핫이슈": [],
        "📊 증시 UP&DOWN": [],
        "✨ 금융시장 동향": [],
        "🍯 투자·재테크": [],
        "👂 산업 뉴스": [],
        "💼 기업 소식": [],
        "⚙️ 테크(Tech)": [],
        "🗞️ 경제 정책": [],
        "🚩 경제 지표": [],
        "🏘️ 부동산": []
    }
    
    # Google News RSS 피드
    keywords = ["경제", "주식", "증시", "부동산", "투자"]
    
    try:
        import feedparser
        
        all_news = []
        for keyword in keywords:
            feed_url = f"https://news.google.com/rss/search?q={keyword}+when:1d&hl=ko&gl=KR&ceid=KR:ko"
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:5]:  # 각 키워드당 5개
                all_news.append({
                    "title": entry.title,
                    "link": entry.link,
                    "source": entry.source.title if hasattr(entry, 'source') else "Google News"
                })
        
        # 뉴스를 적절한 카테고리에 분류 (간단한 키워드 매칭)
        for news in all_news:
            title = news['title']
            if any(word in title for word in ["부동산", "아파트", "집값"]):
                news_categories["🏘️ 부동산"].append(news)
            elif any(word in title for word in ["주식", "증시", "코스피", "나스닥"]):
                news_categories["📊 증시 UP&DOWN"].append(news)
            elif any(word in title for word in ["정책", "정부", "금리"]):
                news_categories["🗞️ 경제 정책"].append(news)
            elif any(word in title for word in ["기업", "CEO", "회사"]):
                news_categories["💼 기업 소식"].append(news)
            else:
                news_categories["🥔 핫이슈"].append(news)
        
    except Exception as e:
        print(f"Error fetching news: {e}")
    
    return news_categories


def format_change(change):
    """변동률 포맷팅"""
    if change > 0:
        return f'<span class="change-positive">🔴 +{abs(change):.2f}%</span>'
    elif change < 0:
        return f'<span class="change-negative">🔵 -{abs(change):.2f}%</span>'
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
    """HTML 파일 생성"""
    
    # 비밀번호 설정 (원하는 비밀번호로 변경하세요!)
    PASSWORD = "1116"
    
    # 현재 시각 (한국 시간)
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)
    update_time = now.strftime('%Y-%m-%d %H:%M')
    
    # 시장 데이터 테이블 생성
    market_rows = ""
    for data in market_data:
        market_rows += f"""
        <tr>
            <td class="index-name">{data['name']}</td>
            <td class="price"><strong>{format_price(data['price'])}</strong></td>
            <td>{format_change(data['change'])}</td>
            <td>{data['source']}</td>
            <td></td>
        </tr>
        """
    
    # 뉴스 섹션 생성
    news_sections = ""
    for category, news_list in news_data.items():
        if news_list:
            news_items = ""
            for news in news_list[:5]:  # 각 카테고리당 최대 5개
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
    
    if not news_sections:
        news_sections = """
        <div class="news-category">
            <h3>📰 경제 뉴스</h3>
            <p style="padding: 20px; color: #666;">현재 뉴스를 불러올 수 없습니다.</p>
        </div>
        """
    
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 윌리엄의 Macro Insight</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&family=Montserrat:wght@700;900&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary: #FF6B35;
            --secondary: #F7931E;
            --accent: #FFC93C;
            --dark: #2D3142;
            --light: #EFF1F3;
            --success: #00D9A3;
            --danger: #FF5252;
        }}

        body {{
            font-family: 'Noto Sans KR', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
            padding: 20px;
            min-height: 100vh;
            color: var(--dark);
        }}

        /* 비밀번호 입력 화면 */
        #password-screen {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            z-index: 9999;
        }}

        .password-box {{
            background: white;
            padding: 60px 50px;
            border-radius: 24px;
            box-shadow: 0 25px 80px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 450px;
            width: 90%;
            animation: slideIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .password-box h2 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 2.5em;
            font-weight: 900;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
        }}

        .password-box p {{
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}

        .password-input {{
            width: 100%;
            padding: 18px 24px;
            font-size: 1.1em;
            border: 3px solid #eee;
            border-radius: 12px;
            margin-bottom: 20px;
            font-family: 'Noto Sans KR', sans-serif;
            transition: all 0.3s;
        }}

        .password-input:focus {{
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
        }}

        .password-btn {{
            width: 100%;
            padding: 18px;
            font-size: 1.1em;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
            font-family: 'Noto Sans KR', sans-serif;
        }}

        .password-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(255, 107, 53, 0.4);
        }}

        .error-message {{
            color: var(--danger);
            margin-top: 15px;
            font-weight: 600;
            display: none;
        }}

        .lock-icon {{
            font-size: 4em;
            margin-bottom: 20px;
        }}

        /* 대시보드 화면 */
        #dashboard {{
            display: none;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 24px;
            padding: 50px;
            box-shadow: 0 25px 80px rgba(0,0,0,0.25);
            animation: slideIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        header {{
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 4px solid var(--primary);
            padding-bottom: 30px;
        }}

        h1 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 3.5em;
            font-weight: 900;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            letter-spacing: -1px;
        }}

        .update-time {{
            color: #666;
            font-size: 1em;
            font-weight: 500;
        }}

        .greeting {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 35px;
            border-radius: 20px;
            margin-bottom: 40px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(255, 107, 53, 0.3);
            position: relative;
            overflow: hidden;
        }}

        .greeting::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }}

        @keyframes rotate {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}

        .greeting h3 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 2.2em;
            margin-bottom: 15px;
            position: relative;
            z-index: 1;
        }}

        .greeting p {{
            font-size: 1.15em;
            line-height: 1.7;
            position: relative;
            z-index: 1;
        }}

        h2 {{
            font-family: 'Montserrat', sans-serif;
            color: var(--dark);
            font-size: 2em;
            margin: 50px 0 25px 0;
            padding-left: 20px;
            border-left: 6px solid var(--primary);
            font-weight: 900;
        }}

        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 25px 0;
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        }}

        thead {{
            background: linear-gradient(135deg, var(--dark) 0%, #4a5568 100%);
        }}

        th {{
            color: white;
            padding: 20px 18px;
            text-align: left;
            font-weight: 700;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        tbody tr {{
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            border-bottom: 1px solid #eee;
        }}

        tbody tr:hover {{
            background: linear-gradient(90deg, #fff5f0 0%, white 100%);
            transform: scale(1.01);
            box-shadow: 0 4px 15px rgba(255, 107, 53, 0.1);
        }}

        tbody tr:last-child {{
            border-bottom: none;
        }}

        td {{
            padding: 18px;
            font-size: 1em;
        }}

        .index-name {{
            font-weight: 700;
            color: var(--dark);
        }}

        .price {{
            font-family: 'Montserrat', sans-serif;
            font-size: 1.15em;
            font-weight: 700;
            color: var(--dark);
        }}

        .change-positive {{
            color: var(--danger);
            font-weight: 700;
        }}

        .change-negative {{
            color: #2196F3;
            font-weight: 700;
        }}

        .change-neutral {{
            color: #9E9E9E;
            font-weight: 700;
        }}

        .news-section {{
            margin: 30px 0;
        }}

        .news-category {{
            margin: 35px 0;
            padding: 25px;
            background: linear-gradient(135deg, #f8f9fa 0%, white 100%);
            border-radius: 16px;
            border-left: 5px solid var(--primary);
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }}

        .news-category h3 {{
            color: var(--dark);
            font-family: 'Montserrat', sans-serif;
            font-size: 1.5em;
            margin-bottom: 20px;
            font-weight: 900;
        }}

        .news-item {{
            padding: 15px 0;
            border-bottom: 1px solid #e0e0e0;
            transition: all 0.3s;
        }}

        .news-item:last-child {{
            border-bottom: none;
        }}

        .news-item:hover {{
            padding-left: 15px;
        }}

        .news-item a {{
            color: #333;
            text-decoration: none;
            font-size: 1.05em;
            display: flex;
            align-items: flex-start;
            gap: 10px;
            line-height: 1.6;
            transition: color 0.3s;
        }}

        .news-item a:hover {{
            color: var(--primary);
        }}

        .news-item a::before {{
            content: "▪";
            color: var(--primary);
            font-weight: bold;
            font-size: 1.3em;
            flex-shrink: 0;
        }}

        .footer {{
            text-align: center;
            margin-top: 60px;
            padding: 30px 0;
            border-top: 3px solid #eee;
        }}

        .footer p {{
            color: #666;
            font-size: 1.1em;
            line-height: 1.8;
        }}

        .footer-highlight {{
            font-size: 1.3em;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 10px;
        }}

        @media (max-width: 768px) {{
            .password-box {{
                padding: 40px 30px;
            }}

            .container {{
                padding: 25px;
                border-radius: 16px;
            }}
            
            h1 {{
                font-size: 2.2em;
            }}
            
            h2 {{
                font-size: 1.5em;
            }}
            
            table {{
                font-size: 0.85em;
            }}
            
            th, td {{
                padding: 12px 8px;
            }}

            .greeting h3 {{
                font-size: 1.6em;
            }}
        }}
    </style>
</head>
<body>
    <!-- 비밀번호 입력 화면 -->
    <div id="password-screen">
        <div class="password-box">
            <div class="lock-icon">🔒</div>
            <h2>망고 대시보드</h2>
            <p>비밀번호를 입력하세요</p>
            <input type="password" 
                   id="password-input" 
                   class="password-input" 
                   placeholder="비밀번호" 
                   onkeypress="if(event.key==='Enter') checkPassword()">
            <button class="password-btn" onclick="checkPassword()">🔓 입장하기</button>
            <p class="error-message" id="error-message">❌ 비밀번호가 틀렸습니다</p>
        </div>
    </div>

    <!-- 대시보드 화면 -->
    <div id="dashboard">
        <div class="container">
            <header>
                <h1>📊 윌리엄의 Macro Insight</h1>
                <div class="update-time">기준 시각: {update_time}</div>
            </header>

            <div class="greeting">
                <h3>와썹 망고! 😍</h3>
                <p>오늘도 윌리엄이 <strong>실시간 데이터</strong>와 <strong>추세 그래프</strong>를 싹 정리했어! 📈<br>
                <strong>뉴스 브리핑</strong>까지 한눈에 확인하고 시장 흐름을 잡아봐! 🔥</p>
            </div>

            <h2>1. 📊 핵심 지표 라이브 (Live Ticker)</h2>
            <table>
                <thead>
                    <tr>
                        <th>지표 (Index)</th>
                        <th>가격 (Price)</th>
                        <th>변동 (Change)</th>
                        <th>출처 (Source)</th>
                        <th>추세 (Trend 30D)</th>
                    </tr>
                </thead>
                <tbody>
                    {market_rows}
                </tbody>
            </table>

            <h2>🌍 경제뉴스 브리핑 🌍</h2>
            <div class="news-section">
                {news_sections}
            </div>

            <div class="footer">
                <p class="footer-highlight">오늘도 성투해 망고! 질문 있으면 언제든 환영이야! 💛</p>
                <p style="margin-top: 15px; font-size: 0.95em;">Data Powered by Yahoo Finance & Google News</p>
                <p style="margin-top: 10px; font-size: 0.85em; color: #999;">자동 업데이트: 매일 오전 9시 (KST)</p>
            </div>
        </div>
    </div>

    <script>
        // 비밀번호 설정 (Python 스크립트와 동일하게)
        const CORRECT_PASSWORD = '{PASSWORD}';
        
        // 세션 스토리지에서 로그인 상태 확인
        if (sessionStorage.getItem('mango-logged-in') === 'true') {{
            showDashboard();
        }} else {{
            // 페이지 로드 시 비밀번호 입력창에 포커스
            document.getElementById('password-input').focus();
        }}

        function checkPassword() {{
            const input = document.getElementById('password-input');
            const errorMsg = document.getElementById('error-message');
            
            if (input.value === CORRECT_PASSWORD) {{
                // 비밀번호 맞음
                sessionStorage.setItem('mango-logged-in', 'true');
                showDashboard();
            }} else {{
                // 비밀번호 틀림
                errorMsg.style.display = 'block';
                input.value = '';
                input.focus();
                
                // 입력창 흔들기 효과
                input.style.animation = 'shake 0.5s';
                setTimeout(() => {{
                    input.style.animation = '';
                }}, 500);
            }}
        }}

        function showDashboard() {{
            document.getElementById('password-screen').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
        }}

        // 흔들기 애니메이션
        const style = document.createElement('style');
        style.textContent = `
            @keyframes shake {{
                0%, 100% {{ transform: translateX(0); }}
                25% {{ transform: translateX(-10px); }}
                75% {{ transform: translateX(10px); }}
            }}
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
"""
    
    return html_content


def main():
    """메인 실행 함수"""
    print("🚀 망고 대시보드 업데이트 시작...")
    
    # 데이터 수집
    print("📊 시장 데이터 수집 중...")
    market_data = get_market_data()
    
    print("📰 뉴스 데이터 수집 중...")
    news_data = get_news()
    
    # HTML 생성
    print("📝 HTML 파일 생성 중...")
    html_content = generate_html(market_data, news_data)
    
    # 파일 저장
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ 업데이트 완료!")
    print(f"   - 수집된 지표: {len(market_data)}개")
    print(f"   - 수집된 뉴스: {sum(len(v) for v in news_data.values())}개")


if __name__ == "__main__":
    main()
