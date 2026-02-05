import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_API_URL = "http://127.0.0.1:5432" #   <-- 아이피 주소 변경 필수

def send_prediction(data: dict, base_url: str = DEFAULT_API_URL) -> bool:
    endpoint = f"{base_url}/api/predictions"
    
    try:
        response = requests.post(endpoint, json=data, timeout=5)
        response.raise_for_status()
        
        logger.info(f"[Prediction 저장 성공] 응답: {response.json()}")
        return True

    except Exception as e:
        logger.error(f"[Prediction 저장 실패] {e}")
        return False

def send_explanation(data: dict, base_url: str = DEFAULT_API_URL) -> bool:
    endpoint = f"{base_url}/api/explanations"
    
    try:
        response = requests.post(endpoint, json=data, timeout=5)
        response.raise_for_status()
        
        logger.info(f"[Explanation 저장 성공] 응답: {response.json()}")
        return True

    except Exception as e:
        logger.error(f"[Explanation 저장 실패] {e}")
        return False
    
def send_news(data: dict, base_url: str = DEFAULT_API_URL) -> bool:
    endpoint = f"{base_url}/api/newsdb"
    
    try:
        response = requests.post(endpoint, json=data, timeout=5)
        response.raise_for_status()
        
        logger.info(f"[News 저장 성공] 응답: {response.json()}")
        return True

    except Exception as e:
        logger.error(f"[News 저장 실패] {e}")
        return False

def send_market_metric(data: dict, base_url: str = DEFAULT_API_URL) -> bool:
    endpoint = f"{base_url}/api/market-metrics"
    
    try:
        response = requests.post(endpoint, json=data, timeout=5)
        response.raise_for_status()
        
        logger.info(f"[Market Metric 저장 성공] 응답: {response.json()}")
        return True

    except Exception as e:
        logger.error(f"[Market Metric 저장 실패] {e}")
        return False

def send_historical_price(data: dict, base_url: str = DEFAULT_API_URL) -> bool:
    endpoint = f"{base_url}/api/historical-prices"
    
    try:
        response = requests.post(endpoint, json=data, timeout=5)
        response.raise_for_status()
        
        logger.info(f"[Historical Price 저장 성공] 응답: {response.json()}")
        return True

    except Exception as e:
        logger.error(f"[Historical Price 저장 실패] {e}")
        return False

def send_simulation(data: dict, base_url: str = DEFAULT_API_URL) -> dict:
    """
    시뮬레이션 요청 (AI 서버 준비 시 사용)
    
    Args:
        data: 시뮬레이션 요청 데이터
        base_url: API 서버 주소
    
    Returns:
        시뮬레이션 결과 (dict) 또는 None
    """
    endpoint = f"{base_url}/api/simulate"
    
    try:
        response = requests.post(endpoint, json=data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"[Simulation 성공] 결과: {result}")
        return result

    except Exception as e:
        logger.error(f"[Simulation 실패] {e}")
        return None

"""
    입력 데이터 형식 예시

    dummy_pred = {
        "target_date": "2026-06-01",
        "commodity": "Corn",
        "price_pred": 500.5,
        "conf_lower": 490.0,
        "conf_upper": 510.0,
        "top1_factor": "Test Factor",
        "top1_impact": 10.0,
        "top2_factor": "None",
        "top2_impact": 0,
        "top3_factor": "None",
        "top3_impact": 0,
        "top4_factor": "None",
        "top4_impact": 0,
        "top5_factor": "None",
        "top5_impact": 0
    }
    
    dummy_exp = {
        "pred_id": int,
        "content": str,
        "llm_model": str,
        "impact_news": [
            {
                "source": "Bloomberg",
                "title": "뉴스 제목",
                "impact_score": 85,
                "analysis": "영향 분석 내용"
            }
        ]
    }

    news_data = {
        "title": "뉴스 제목",
        "content": "금값 폭등...",
        "source_url": "http://...",
        "embedding": [0.1, 0.2, 0.3], # 1536차원 리스트
        "created_at": "2026-02-04T10:00:00Z"
    }
    
    market_metric_data = {
        "commodity": "Corn",
        "date": "2026-02-03",
        "metric_id": "net_long",
        "label": "Net Long (순매수)",
        "value": "15.4K",
        "numeric_value": 15400.0,
        "trend": 5.2,
        "impact": "High"
    }
    
    historical_price_data = {
        "commodity": "Corn",
        "date": "2026-01-15",
        "actual_price": 445.30
    }
    
    simulation_data = {
        "commodity": "Corn",
        "base_date": "2026-02-03",
        "feature_overrides": {
            "WTI": 80.0,
            "DXY": 105.5,
            "NET_LONG": 18000,
            "ETHANOL_PROD": 1.15
        }
    }

    각각의 함수 호출로 구분해서 전송:
    
    # 예측 데이터 전송
    send_prediction(dummy_pred)

    # 설명 데이터 전송
    send_explanation(dummy_exp)

    # 뉴스 데이터 전송
    send_news(news_data)
    
    # 시장 지표 전송
    send_market_metric(market_metric_data)
    
    # 실제 가격 전송
    send_historical_price(historical_price_data)
    
    # 시뮬레이션 요청
    result = send_simulation(simulation_data)
"""