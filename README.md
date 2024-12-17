# CrawlEmbedder
만개의 레시피 웹사이트에서 레시피를 수집하고 벡터 데이터베이스에 저장하는 프로젝트입니다.

## 기능

- 만개의 레시피 웹사이트 크롤링
- 레시피 데이터 전처리 및 임베딩
- Pinecone 벡터 데이터베이스 저장

## 필수 요구사항

- Python 3.8 이상
- pip (파이썬 패키지 관리자)

## 환경 설정

1. 저장소 클론
```bash
git clone [repository-url]
cd CrawlEmbedder
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 프로젝트 루트 디렉토리에 생성하고 다음 내용을 추가하세요:
```
RECIPE_DB_API_KEY=your_recipe_db_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_HOST_URL=your_pinecone_host_url
```

## 실행 방법

1. FastAPI 서버 실행:
```bash
uvicorn app.main:app --reload
```

2. 서버가 시작되면 자동으로 레시피 크롤링 및 데이터베이스 저장이 시작됩니다.

## 프로젝트 구조

```
app/
├── controller/        # API 컨트롤러
├── core/             # 설정 및 핵심 기능
├── dto/              # 데이터 전송 객체
├── model/            # 데이터 모델
├── repositorie/      # 데이터베이스 연결
├── service/          # 비즈니스 로직
│   ├── parse/       # 데이터 파싱
│   ├── preprocess/  # 데이터 전처리
│   └── scrap/       # 웹 스크래핑
└── main.py          # 애플리케이션 진입점
```

## 주의사항

- 웹 크롤링 시 해당 웹사이트의 이용약관을 준수해주세요.
- API 키는 절대 공개하지 마세요.
- 대량의 요청 시 서버에 부하가 걸릴 수 있으니 적절한 간격을 두고 실행해주세요.
```
