from fastapi import FastAPI
from app import datatable
from app.database import engine
from app.routers import predictions, newsdb, market_metrics, historical_prices, simulation
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",  ## 아이피 갱신 필요 - 프론트 주소!
    "http://127.0.0.1:3000",    
    "*"
]


# DB에 테이블이 없으면 자동 생성 (CREATE TABLE IF NOT EXISTS)
datatable.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Commodity Price AI Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],   
)

# 라우터 등록
app.include_router(predictions.router)
app.include_router(newsdb.router)
app.include_router(market_metrics.router)
app.include_router(historical_prices.router)
app.include_router(simulation.router)

@app.get("/")
def read_root():
    return {"message": "Server is running with new structure! 🚀"}