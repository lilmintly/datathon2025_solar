# datathon2025_solar
project_root/
├── baselinecode/              # 코드 실행 디렉토리
│   ├── main.py                # 실행 메인 파일
│   ├── config.py              # 설정 관리
│   ├── .env
│   ├── requirements.txt       # 패키지 목록
│   ├── prompts/               # 프롬프트 템플릿
│   │   ├── __init__.py
│   │   ├── templates.py
│   └── utils/                 # 유틸리티 (API 호출, 평가 등)
│       ├── __init__.py
│       ├── experiment.py
├── data/                      # 데이터 디렉토리
│   ├── train.csv
│   ├── test.csv
│   └── sample_submission.csv
├── venv/                      # 가상환경 (venv)
├── README.md                  # 프로젝트 개요 및 실행 방법 안내