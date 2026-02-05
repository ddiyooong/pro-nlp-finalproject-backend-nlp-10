from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, dataschemas
from ..database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Simulation"]
)

# POST /api/simulate
@router.post("/simulate", response_model=dataschemas.SimulationResponse)
def simulate_prediction(
    request: dataschemas.SimulationRequest,
    db: Session = Depends(get_db)
):
    """
    시뮬레이션 엔드포인트
    
    현재는 AI 서버가 준비되지 않아 모의 응답을 반환합니다.
    향후 AI 서버 연동 시 실제 모델을 사용한 시뮬레이션을 수행합니다.
    """
    
    # 기준 날짜의 원본 예측 조회
    base_prediction = crud.get_prediction_by_date(db, request.commodity, request.base_date)
    
    if not base_prediction:
        raise HTTPException(
            status_code=404, 
            detail=f"{request.commodity}의 {request.base_date} 예측 데이터가 없습니다."
        )
    
    original_forecast = float(base_prediction.price_pred)
    
    # TODO: AI 서버가 준비되면 실제 시뮬레이션 API 호출
    # 현재는 간단한 모의 계산으로 대체
    
    # feature_overrides에서 영향도를 임시로 계산
    feature_impacts = []
    total_impact = 0.0
    
    for feature_name, new_value in request.feature_overrides.items():
        # 임시 계산: 각 feature의 변화를 가정
        # 실제로는 AI 서버에서 정확한 계산이 이루어져야 함
        current_value = new_value * 0.95  # 가정: 5% 변화
        value_change = new_value - current_value
        contribution = value_change * 0.1  # 임시 기여도 계산
        total_impact += contribution
        
        feature_impacts.append(
            dataschemas.FeatureImpact(
                feature=feature_name,
                current_value=current_value,
                new_value=new_value,
                value_change=value_change,
                contribution=contribution
            )
        )
    
    # 시뮬레이션 결과 계산
    simulated_forecast = original_forecast + total_impact
    change = simulated_forecast - original_forecast
    change_percent = (change / original_forecast) * 100 if original_forecast != 0 else 0.0
    
    return dataschemas.SimulationResponse(
        original_forecast=original_forecast,
        simulated_forecast=round(simulated_forecast, 2),
        change=round(change, 2),
        change_percent=round(change_percent, 2),
        feature_impacts=feature_impacts
    )
