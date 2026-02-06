from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
import logging

from .. import crud, dataschemas
from ..database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Batch Write"]
)


# ===========================
# TFT 예측 (Predictions)
# ===========================

@router.post("/predictions", response_model=dataschemas.TftPredResponse)
def create_prediction(
    data: dataschemas.TftPredCreate,
    db: Session = Depends(get_db)
):
    """TFT 예측 단건 저장"""
    record = crud.create_tft_prediction(db, data)
    logger.info(f"예측 저장 완료: {data.commodity} / {data.target_date}")
    return record


@router.post("/predictions/bulk", response_model=dataschemas.BatchResult)
def create_predictions_bulk(
    data: dataschemas.TftPredBulkCreate,
    db: Session = Depends(get_db)
):
    """TFT 예측 벌크 저장 (7일치 등)"""
    count = crud.create_tft_predictions_bulk(db, data.predictions)
    logger.info(f"예측 벌크 저장 완료: {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 저장 완료", count=count)


@router.delete("/predictions", response_model=dataschemas.BatchResult)
def delete_predictions(
    data: dataschemas.DeleteByDateRange,
    db: Session = Depends(get_db)
):
    """예측 삭제 (commodity + date 범위)"""
    count = crud.delete_tft_predictions(db, data.commodity, data.start_date, data.end_date)
    logger.info(f"예측 삭제 완료: {data.commodity} {data.start_date}~{data.end_date}, {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 삭제 완료", count=count)


# ===========================
# 예측 설명 (Explanations)
# ===========================

@router.post("/explanations", response_model=dataschemas.ExpPredResponse)
def create_explanation(
    data: dataschemas.ExpPredCreate,
    db: Session = Depends(get_db)
):
    """예측 설명 저장"""
    record = crud.create_explanation(db, data)
    logger.info(f"설명 저장 완료: pred_id={data.pred_id}")
    return record


@router.delete("/explanations/{pred_id}", response_model=dataschemas.BatchResult)
def delete_explanation(
    pred_id: int,
    db: Session = Depends(get_db)
):
    """특정 예측의 설명 삭제"""
    count = crud.delete_explanation_by_pred_id(db, pred_id)
    logger.info(f"설명 삭제 완료: pred_id={pred_id}, {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 삭제 완료", count=count)


# ===========================
# 뉴스 (News)
# ===========================

@router.post("/newsdb", response_model=dataschemas.NewsResponse)
def create_news(
    data: dataschemas.NewsCreate,
    db: Session = Depends(get_db)
):
    """뉴스 단건 저장"""
    record = crud.create_news(db, data)
    logger.info(f"뉴스 저장 완료: {data.title[:30]}")
    return record


@router.post("/newsdb/bulk", response_model=dataschemas.BatchResult)
def create_news_bulk(
    data: dataschemas.NewsBulkCreate,
    db: Session = Depends(get_db)
):
    """뉴스 벌크 저장"""
    count = crud.create_news_bulk(db, data.news_list)
    logger.info(f"뉴스 벌크 저장 완료: {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 저장 완료", count=count)


@router.delete("/newsdb", response_model=dataschemas.BatchResult)
def delete_news(
    data: dataschemas.DeleteByDate,
    db: Session = Depends(get_db)
):
    """특정 날짜 이전의 뉴스 삭제"""
    count = crud.delete_news_by_date(db, data.date)
    logger.info(f"뉴스 삭제 완료: {data.date} 이전, {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 삭제 완료", count=count)


# ===========================
# 일일 요약 (Daily Summary)
# ===========================

@router.post("/daily-summary", response_model=dataschemas.DailySummaryResponse)
def create_daily_summary(
    data: dataschemas.DailySummaryCreate,
    db: Session = Depends(get_db)
):
    """일일 요약 저장"""
    record = crud.create_daily_summary(db, data)
    logger.info(f"일일 요약 저장 완료: {data.commodity} / {data.target_date}")
    return record


@router.delete("/daily-summary", response_model=dataschemas.BatchResult)
def delete_daily_summary(
    data: dataschemas.DeleteByDateRange,
    db: Session = Depends(get_db)
):
    """일일 요약 삭제 (commodity + date 범위)"""
    count = crud.delete_daily_summary(db, data.commodity, data.start_date, data.end_date)
    logger.info(f"일일 요약 삭제 완료: {data.commodity} {data.start_date}~{data.end_date}, {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 삭제 완료", count=count)


# ===========================
# 시장 지표 (Market Metrics)
# ===========================

@router.post("/market-metrics", response_model=dataschemas.BatchResult)
def create_market_metrics(
    data: dataschemas.MarketMetricBulkCreate,
    db: Session = Depends(get_db)
):
    """시장 지표 벌크 저장 (날짜당 46개 feature 등)"""
    count = crud.create_market_metrics_bulk(db, data.commodity, data.date, data.metrics)
    logger.info(f"시장 지표 저장 완료: {data.commodity} / {data.date}, {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 저장 완료", count=count)


@router.post("/market-metrics/bulk", response_model=dataschemas.BatchResult)
def create_market_metrics_bulk(
    data: dataschemas.MarketMetricBulkCreate,
    db: Session = Depends(get_db)
):
    """시장 지표 벌크 저장 (POST /market-metrics와 동일)"""
    count = crud.create_market_metrics_bulk(db, data.commodity, data.date, data.metrics)
    logger.info(f"시장 지표 벌크 저장 완료: {data.commodity} / {data.date}, {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 저장 완료", count=count)


@router.put("/market-metrics", response_model=dataschemas.BatchResult)
def upsert_market_metrics(
    data: dataschemas.MarketMetricBulkUpsert,
    db: Session = Depends(get_db)
):
    """시장 지표 Upsert (commodity + date + metric_id 기준)"""
    count = crud.upsert_market_metrics(db, data.commodity, data.date, data.metrics)
    logger.info(f"시장 지표 Upsert 완료: {data.commodity} / {data.date}, {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 Upsert 완료", count=count)


@router.delete("/market-metrics", response_model=dataschemas.BatchResult)
def delete_market_metrics(
    data: dataschemas.DeleteByDateRange,
    db: Session = Depends(get_db)
):
    """시장 지표 삭제 (commodity + date 범위)"""
    count = crud.delete_market_metrics(db, data.commodity, data.start_date, data.end_date)
    logger.info(f"시장 지표 삭제 완료: {data.commodity} {data.start_date}~{data.end_date}, {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 삭제 완료", count=count)


# ===========================
# 실제 가격 (Historical Prices)
# ===========================

@router.post("/historical-prices", response_model=dataschemas.BatchResult)
def create_historical_prices(
    data: dataschemas.HistoricalPriceBulkCreate,
    db: Session = Depends(get_db)
):
    """실제 가격 벌크 저장"""
    count = crud.create_historical_prices_bulk(db, data.commodity, data.prices)
    logger.info(f"실제 가격 저장 완료: {data.commodity}, {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 저장 완료", count=count)


@router.post("/historical-prices/bulk", response_model=dataschemas.BatchResult)
def create_historical_prices_bulk(
    data: dataschemas.HistoricalPriceBulkCreate,
    db: Session = Depends(get_db)
):
    """실제 가격 벌크 저장 (POST /historical-prices와 동일)"""
    count = crud.create_historical_prices_bulk(db, data.commodity, data.prices)
    logger.info(f"실제 가격 벌크 저장 완료: {data.commodity}, {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 저장 완료", count=count)


@router.put("/historical-prices", response_model=dataschemas.BatchResult)
def upsert_historical_prices(
    data: dataschemas.HistoricalPriceBulkUpsert,
    db: Session = Depends(get_db)
):
    """실제 가격 Upsert (commodity + date 기준)"""
    count = crud.upsert_historical_prices(db, data.commodity, data.prices)
    logger.info(f"실제 가격 Upsert 완료: {data.commodity}, {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 Upsert 완료", count=count)


@router.delete("/historical-prices", response_model=dataschemas.BatchResult)
def delete_historical_prices(
    data: dataschemas.DeleteByDateRange,
    db: Session = Depends(get_db)
):
    """실제 가격 삭제 (commodity + date 범위)"""
    count = crud.delete_historical_prices(db, data.commodity, data.start_date, data.end_date)
    logger.info(f"실제 가격 삭제 완료: {data.commodity} {data.start_date}~{data.end_date}, {count}건")
    return dataschemas.BatchResult(success=True, message=f"{count}건 삭제 완료", count=count)
