from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

#---------------------------------------------------------------------

class TftPredBase(BaseModel):
    target_date: date
    commodity: str
    price_pred: float
    conf_lower: float
    conf_upper: float
    
    top1_factor: Optional[str] = None
    top1_impact: Optional[float] = None
    top2_factor: Optional[str] = None
    top2_impact: Optional[float] = None
    top3_factor: Optional[str] = None
    top3_impact: Optional[float] = None
    top4_factor: Optional[str] = None
    top4_impact: Optional[float] = None
    top5_factor: Optional[str] = None
    top5_impact: Optional[float] = None

class TftPredCreate(TftPredBase):
    pass

class TftPredResponse(TftPredBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

#---------------------------------------------------------------------

class ImpactNews(BaseModel):
    source: str
    title: str
    impact_score: int
    analysis: str

class ExpPredCreate(BaseModel):
    pred_id: int
    content: str
    llm_model: str
    impact_news: Optional[List[dict]] = None

class ExpPredResponse(BaseModel):
    id: int
    pred_id: int
    content: str
    llm_model: str
    impact_news: Optional[List[ImpactNews]] = None
    created_at: datetime

    class Config:
        from_attributes = True

#---------------------------------------------------------------------

class DailySummaryCreate(BaseModel):
    target_date: date
    commodity: str
    score: float
    related_news_ids: List[int]

class DailySummaryResponse(DailySummaryCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

#---------------------------------------------------------------------

class NewsBase(BaseModel):
    title: str
    content: str
    source_url: Optional[str] = None
    created_at: datetime


class NewsCreate(NewsBase):
    embedding: List[float]

class NewsResponse(NewsBase):
    id: int
    
    class Config:
        from_attributes = True

class NewsResponseWithVector(NewsResponse):
    embedding: List[float]

#---------------------------------------------------------------------

class MarketMetricItem(BaseModel):
    metric_id: str
    label: str
    value: str
    numeric_value: float
    trend: float
    impact: str

class MarketMetricBase(BaseModel):
    commodity: str
    date: date
    metric_id: str
    label: str
    value: str
    numeric_value: float
    trend: float
    impact: str

class MarketMetricCreate(MarketMetricBase):
    pass

class MarketMetricResponse(MarketMetricBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class MarketMetricsResponse(BaseModel):
    commodity: str
    date: str
    metrics: List[MarketMetricItem]

#---------------------------------------------------------------------

class HistoricalPriceItem(BaseModel):
    date: str
    actual_price: float

class HistoricalPriceBase(BaseModel):
    commodity: str
    date: date
    actual_price: float

class HistoricalPriceCreate(HistoricalPriceBase):
    pass

class HistoricalPriceResponse(HistoricalPriceBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class HistoricalPricesResponse(BaseModel):
    commodity: str
    prices: List[HistoricalPriceItem]

#---------------------------------------------------------------------

class FeatureImpact(BaseModel):
    feature: str
    current_value: float
    new_value: float
    value_change: float
    contribution: float

class SimulationRequest(BaseModel):
    commodity: str
    base_date: date
    feature_overrides: dict

class SimulationResponse(BaseModel):
    original_forecast: float
    simulated_forecast: float
    change: float
    change_percent: float
    feature_impacts: List[FeatureImpact]