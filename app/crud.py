from sqlalchemy.orm import Session, defer
from sqlalchemy import func
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional

from . import datatable, dataschemas


# ===========================
# TFT 예측 관련 CRUD
# ===========================

def get_tft_predictions(
    db: Session, 
    commodity: str, 
    start_date: date, 
    end_date: date
) -> List[datatable.TftPred]:
    """
    특정 품목의 기간별 예측값 조회
    
    Args:
        db: DB 세션
        commodity: 품목명 (예: "corn")
        start_date: 시작 날짜
        end_date: 종료 날짜
    
    Returns:
        TftPred 레코드 리스트 (최신순)
    """
    return db.query(datatable.TftPred)\
        .filter(datatable.TftPred.commodity == commodity)\
        .filter(datatable.TftPred.target_date >= start_date)\
        .filter(datatable.TftPred.target_date <= end_date)\
        .order_by(datatable.TftPred.target_date.desc())\
        .all()


def get_prediction_by_date(
    db: Session, 
    commodity: str, 
    target_date: date
) -> Optional[datatable.TftPred]:
    """
    특정 품목의 특정 날짜 예측값 조회
    
    Args:
        db: DB 세션
        commodity: 품목명
        target_date: 목표 날짜
    
    Returns:
        TftPred 레코드 또는 None
    """
    return db.query(datatable.TftPred)\
        .filter(datatable.TftPred.commodity == commodity)\
        .filter(datatable.TftPred.target_date == target_date)\
        .first()


def get_latest_predictions(
    db: Session, 
    commodity: str
) -> List[datatable.TftPred]:
    """
    최신 예측값 조회 (target_date별 가장 최신 created_at)
    
    조회 범위: (오늘 - 30일) ~ (오늘 + 60일)
    
    로직:
    1. target_date 범위 필터링
    2. 각 target_date별로 가장 최신 created_at의 레코드만 선택
    3. target_date 오름차순 정렬
    
    Args:
        db: DB 세션
        commodity: 품목명
    
    Returns:
        TftPred 레코드 리스트 (날짜순)
    """
    today = datetime.now().date()
    start_date = today - timedelta(days=30)
    end_date = today + timedelta(days=60)
    
    # 서브쿼리: 각 target_date별 최신 created_at
    subquery = db.query(
        datatable.TftPred.target_date,
        func.max(datatable.TftPred.created_at).label('max_created_at')
    ).filter(
        datatable.TftPred.commodity == commodity,
        datatable.TftPred.target_date >= start_date,
        datatable.TftPred.target_date <= end_date
    ).group_by(datatable.TftPred.target_date).subquery()
    
    # 메인 쿼리: 서브쿼리 결과와 조인
    return db.query(datatable.TftPred).join(
        subquery,
        (datatable.TftPred.target_date == subquery.c.target_date) &
        (datatable.TftPred.created_at == subquery.c.max_created_at)
    ).filter(
        datatable.TftPred.commodity == commodity
    ).order_by(datatable.TftPred.target_date.asc()).all()


# ===========================
# 예측 설명(Explanation) 관련 CRUD
# ===========================

def get_explanation_by_pred_id(
    db: Session, 
    pred_id: int
) -> Optional[datatable.ExpPred]:
    """
    특정 예측값에 연결된 설명 조회
    
    Args:
        db: DB 세션
        pred_id: 예측 레코드 ID
    
    Returns:
        ExpPred 레코드 또는 None
    """
    return db.query(datatable.ExpPred)\
        .filter(datatable.ExpPred.pred_id == pred_id)\
        .first()


def get_explanation_by_date(
    db: Session, 
    commodity: str, 
    target_date: date
) -> Optional[datatable.ExpPred]:
    """
    특정 품목의 특정 날짜 예측 설명 조회
    
    Args:
        db: DB 세션
        commodity: 품목명
        target_date: 목표 날짜
    
    Returns:
        ExpPred 레코드 또는 None
    """
    return db.query(datatable.ExpPred)\
        .join(datatable.TftPred, datatable.ExpPred.pred_id == datatable.TftPred.id)\
        .filter(datatable.TftPred.commodity == commodity)\
        .filter(datatable.TftPred.target_date == target_date)\
        .first()


# ===========================
# 뉴스 임베딩 관련 CRUD
# ===========================

def get_doc_embeddings_light(
    db: Session, 
    skip: int = 0, 
    limit: int = 10
) -> List[datatable.DocEmbeddings]:
    """
    뉴스 임베딩 목록 조회 (벡터 제외)
    
    Args:
        db: DB 세션
        skip: 건너뛸 레코드 수
        limit: 조회할 최대 레코드 수
    
    Returns:
        DocEmbeddings 레코드 리스트 (최신순, 벡터 제외)
    """
    return db.query(datatable.DocEmbeddings)\
        .options(defer(datatable.DocEmbeddings.embedding))\
        .order_by(datatable.DocEmbeddings.created_at.desc())\
        .offset(skip).limit(limit)\
        .all()


# ===========================
# 시장 지표(Market Metrics) 관련 CRUD
# ===========================

def get_market_metrics(
    db: Session, 
    commodity: str, 
    target_date: date
) -> List[datatable.MarketMetrics]:
    """
    특정 품목의 특정 날짜 시장 지표 조회
    
    Args:
        db: DB 세션
        commodity: 품목명
        target_date: 목표 날짜
    
    Returns:
        MarketMetrics 레코드 리스트
    """
    return db.query(datatable.MarketMetrics)\
        .filter(datatable.MarketMetrics.commodity == commodity)\
        .filter(datatable.MarketMetrics.date == target_date)\
        .all()


def get_historical_features(
    db: Session, 
    commodity: str, 
    end_date: date, 
    days: int = 60
) -> Dict[str, any]:
    """
    과거 N일의 모든 feature를 market_metrics에서 로드
    
    TFT 모델의 입력 데이터 생성에 사용됩니다.
    
    Args:
        db: DB 세션
        commodity: 품목명
        end_date: 종료 날짜
        days: 조회할 일수 (기본 60일)
    
    Returns:
        과거 데이터
        {
            'dates': [date1, date2, ...],  # 날짜 리스트
            'features': {                   # feature별 시계열 데이터
                'close': [v1, v2, ...],
                'open': [v1, v2, ...],
                ...
            }
        }
    """
    start_date = end_date - timedelta(days=days-1)
    
    # 기간 내 모든 market_metrics 조회
    metrics = db.query(datatable.MarketMetrics)\
        .filter(
            datatable.MarketMetrics.commodity == commodity,
            datatable.MarketMetrics.date >= start_date,
            datatable.MarketMetrics.date <= end_date
        )\
        .order_by(datatable.MarketMetrics.date.asc())\
        .all()
    
    # 날짜별로 그룹핑
    data_by_date = _group_metrics_by_date(metrics)
    
    # 날짜 정렬
    sorted_dates = sorted(data_by_date.keys())
    
    # Feature별로 시계열 데이터 구성
    features = _build_feature_timeseries(data_by_date, sorted_dates)
    
    return {
        'dates': sorted_dates,
        'features': features
    }


def _group_metrics_by_date(metrics: List[datatable.MarketMetrics]) -> Dict[str, Dict[str, float]]:
    """날짜별로 metrics 그룹핑"""
    data_by_date = {}
    
    for metric in metrics:
        date_str = str(metric.date)
        if date_str not in data_by_date:
            data_by_date[date_str] = {}
        
        data_by_date[date_str][metric.metric_id] = metric.numeric_value
    
    return data_by_date


def _build_feature_timeseries(
    data_by_date: Dict[str, Dict[str, float]], 
    sorted_dates: List[str]
) -> Dict[str, List[float]]:
    """Feature별로 시계열 데이터 구성"""
    # TFT 모델에 필요한 feature 목록
    feature_names = [
        # 가격/거래량 (6개)
        'close', 'open', 'high', 'low', 'volume', 'EMA',
        # 뉴스 PCA (32개)
        *[f'news_pca_{i}' for i in range(32)],
        # 기후 지수 (3개)
        'pdsi', 'spi30d', 'spi90d',
        # 거시경제 (2개)
        '10Y_Yield', 'USD_Index',
        # Hawkes Intensity (2개)
        'lambda_price', 'lambda_news',
        # 기타
        'news_count'
    ]
    
    features = {}
    for feature in feature_names:
        features[feature] = []
        for date_str in sorted_dates:
            value = data_by_date[date_str].get(feature, 0.0)
            features[feature].append(value)
    
    return features


# ===========================
# 실제 가격(Historical Prices) 관련 CRUD
# ===========================

def get_historical_prices(
    db: Session, 
    commodity: str, 
    start_date: date, 
    end_date: date
) -> List[datatable.HistoricalPrices]:
    """
    특정 품목의 기간별 실제 가격 조회
    
    Args:
        db: DB 세션
        commodity: 품목명
        start_date: 시작 날짜
        end_date: 종료 날짜
    
    Returns:
        HistoricalPrices 레코드 리스트 (날짜순)
    """
    return db.query(datatable.HistoricalPrices)\
        .filter(datatable.HistoricalPrices.commodity == commodity)\
        .filter(datatable.HistoricalPrices.date >= start_date)\
        .filter(datatable.HistoricalPrices.date <= end_date)\
        .order_by(datatable.HistoricalPrices.date.asc())\
        .all()
