from app.api.deps import get_db
from app.repos.test_repo import get_or_create_test
from fastapi import FastAPI

app = FastAPI()

# @app.on_event("startup") # FastAPI의 이벤트 시스템을 사용하여 애플리케이션이 시작될 때 실행되는 함수를 정의할 수 있음.
# def startup_event():
#     # 여기에 데이터베이스 연결이나 초기화 작업 수행 가능.
#     def on_startup():
#         Base.metadata.create_all(bind=engine)  # 데이터베이스 테이블 생성

@app.get("/")
# 테스트 ORM 모델. 실제 프로젝트에서는 삭제.
def test_route():
    return get_or_create_test(db=next(get_db()), message="Successfully connected to the database")