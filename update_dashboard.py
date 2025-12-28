name: 세계 흐름 대시보드 자동 업데이트

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  update-dashboard:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
    - name: 체크아웃
      uses: actions/checkout@v3
      with:
        fetch-depth: 0
    
    - name: Python 설정
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: 패키지 설치
      run: |
        pip install requests pytz feedparser
    
    - name: 대시보드 업데이트
      run: |
        python update_dashboard.py
    
    - name: 변경사항 커밋 및 푸시
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git pull origin main
        git add index.html
        git diff --quiet && git diff --staged --quiet || (git commit -m "🔄 자동 업데이트: $(date +'%Y-%m-%d %H:%M KST')" && git push origin main)
