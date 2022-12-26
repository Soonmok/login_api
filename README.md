# Login API
Fastapi를 이용한 간단한 login api

## 구현된 기능
- 회원 가입 기능
- 로그인 기능
- 내 정보 보기 기능
- 비밀번호 찾기 기능

## Development Environment

`docker-compose` 를 통해 api와 database를 띄울 수 있습니다.

	# 이미지 빌드
    cd login_api # login_api 폴더 안에서 실행
	docker build -t login_api:latest .

	# api와 데이터 베이스 띄우기
	docker-compose up -d

    # 데이터베이스 마이그레이션 하기
    docker-compose exec api alembic upgrade head

	# 테스트 실행 
	export ENV=local # pytest code가 띄워진 데이터베이스를 바라보게 하도록 env 변수 설정 
    pytest

API 설명은 [localhost:8000/docs](localhost:8000/docs) 에서 확인할 수 있습니다.

주의 사항
- [localhost:8000/docs](localhost:8000/docs) 오른쪽 위에 있는 authorize 버튼을 누르거나, token api를 직접 호출하여 엑세스 토큰을 받을 수 있습니다. (로그인을 할 수 있습니다.) 
- token api나, autorize 버튼을 눌렀을 때 `username` 파라메터에는 `email`을 넣어야 합니다. 

## 사용 기술 스택
- FastAPI
- SQLAlchemy
- Pytest
- Docker-compose
- postgresql
- python 3.8
- alembic

## 신경 쓴 부분
- alembic을 사용하여 데이터베이스 마이그레이션을 관리하였습니다.
- pytest를 사용하여 테스트 코드를 작성하였습니다.
- 테스트 코드를 통해 기존 api를 어떤식으로 사용할 수 있는지 확인할 수 있습니다.
- docker-compose를 사용하여 api와 데이터베이스를 띄웠습니다.
- 비밀번호는 bcrypt를 사용하여 암호화 하였습니다.
- swagger를 사용하여 api 문서를 작성하였습니다.
