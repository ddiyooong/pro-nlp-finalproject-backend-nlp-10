from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime, timedelta
from .. import crud, dataschemas
from ..database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Predictions & Explanations"]
)

# --- [예측 (Predictions)] ---

# GET /api/predictions?commodity=corn
@router.get("/predictions", response_model=dataschemas.PredictionsWithPricesResponse)
def get_predictions(
    commodity: str,
    db: Session = Depends(get_db)
):
    """
    최신 배치의 예측 데이터 + 과거 30일 실제 가격 반환
    - predictions: 각 target_date별 created_at 최신 (오늘-30일 ~ 오늘+60일)
    - historical_prices: 과거 30일 ~ 오늘까지의 실제 가격
    """
    pred = crud.get_latest_predictions(db, commodity)
    if not pred:
        raise HTTPException(
            status_code=404,
            detail=f"{commodity}의 최신 예측 데이터가 없습니다."
        )
    
    # 과거 30일 ~ 오늘까지의 실제 가격 조회
    today = datetime.now().date()
    start_date = today - timedelta(days=30)
    prices = crud.get_historical_prices(db, commodity, start_date, today)
    
    prices_list = [
        dataschemas.HistoricalPriceItem(
            date=p.date.isoformat(),
            actual_price=float(p.actual_price)
        )
        for p in prices
    ] if prices else []
    
    return dataschemas.PredictionsWithPricesResponse(
        predictions=pred,
        historical_prices=prices_list
    )

# GET /api/predictions/2025-12-01?commodity=corn
@router.get("/predictions/{target_date}", response_model=dataschemas.TftPredResponse)
def get_prediction_by_date(
    target_date: date, 
    commodity: str, 
    db: Session = Depends(get_db)
):
    pred = crud.get_prediction_by_date(db, commodity, target_date)
    if not pred:
        raise HTTPException(status_code=404, detail="해당 날짜의 데이터가 없습니다.")
    return pred


# --- [설명 (Explanations)] ---

# GET /api/explanations/2025-12-01?commodity=corn
@router.get("/explanations/{target_date}", response_model=dataschemas.ExpPredResponse)
def get_explanation_by_date(
    target_date: date, 
    commodity: str, 
    db: Session = Depends(get_db)
):
    exp = crud.get_explanation_by_date(db, commodity, target_date)
    if not exp:
        raise HTTPException(status_code=404, detail="해당 날짜의 설명이 없습니다.")
    return exp