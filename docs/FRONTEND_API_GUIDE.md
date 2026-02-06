# 🌐 프론트엔드 API 가이드

**Base URL**: `http://44.252.76.158:8000`

---

## 📡 API 개요

### 기본 정보

| 항목 | 값 |
|------|-----|
| **Base URL** | `http://44.252.76.158:8000` |
| **프로토콜** | HTTP/HTTPS |
| **데이터 형식** | JSON |
| **문자 인코딩** | UTF-8 |
| **날짜 형식** | `YYYY-MM-DD` |
| **Timestamp 형식** | ISO 8601 |

### 지원 품목 (Commodity)

현재 지원되는 품목:
- `corn` - 옥수수

---

## 🔐 인증

**현재 버전**: 인증 불필요

향후 API 키 기반 인증이 추가될 수 있습니다.

---

## 📦 공통 응답 형식

### 성공 응답

```json
{
  "data": {...},
  "status": "success"
}
```

### 에러 응답

```json
{
  "detail": "에러 메시지"
}
```

### HTTP 상태 코드

| 코드 | 의미 |
|------|------|
| `200` | 성공 |
| `400` | 잘못된 요청 |
| `404` | 리소스 없음 |
| `500` | 서버 오류 |

---

## 🎯 API 엔드포인트

---

## 1️⃣ 예측 (Predictions)

### 1-1. 최신 예측 + 실제 가격 조회

가장 최근 배치의 예측 데이터와 과거 30일간 실제 가격을 함께 반환합니다.
- `predictions`: 오늘-30일 ~ 오늘+60일 범위의 예측 (target_date별 최신 created_at)
- `historical_prices`: 과거 30일 ~ 오늘까지의 실제 거래 가격

```http
GET /api/predictions?commodity={commodity}
```

**Parameters:**
| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `commodity` | string | ✅ | 품목명 (예: "corn") |

**Response:**
```json
{
  "predictions": [
    {
      "id": 1,
      "target_date": "2026-02-07",
      "commodity": "corn",
      "price_pred": 450.50,
      "conf_lower": 445.20,
      "conf_upper": 455.80,
      "top1_factor": "close",
      "top1_impact": 0.25,
      "top2_factor": "USD_Index",
      "top2_impact": 0.18,
      "top3_factor": "10Y_Yield",
      "top3_impact": 0.15,
      "model_type": "TFT_v2",
      "created_at": "2026-02-06T12:00:00"
    }
  ],
  "historical_prices": [
    {
      "date": "2026-01-07",
      "actual_price": 448.25
    },
    {
      "date": "2026-01-08",
      "actual_price": 449.50
    }
  ]
}
```

---

### 1-2. 특정 날짜 예측 조회

특정 날짜의 예측 데이터를 조회합니다.

```http
GET /api/predictions/{target_date}?commodity={commodity}
```

**Parameters:**
| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `target_date` | string | ✅ | 날짜 (YYYY-MM-DD) |
| `commodity` | string | ✅ | 품목명 |

**Response:**
```json
{
  "id": 1,
  "target_date": "2026-02-07",
  "commodity": "corn",
  "price_pred": 450.50,
  "conf_lower": 445.20,
  "conf_upper": 455.80,
  "top1_factor": "close",
  "top1_impact": 0.25,
  "top2_factor": "USD_Index",
  "top2_impact": 0.18,
  "top3_factor": "10Y_Yield",
  "top3_impact": 0.15,
  "top4_factor": "volume",
  "top4_impact": 0.12,
  "top5_factor": "news_pca_0",
  "top5_impact": 0.10,
  // ... top6 ~ top20
  "model_type": "TFT_v2",
  "created_at": "2026-02-06T12:00:00"
}
```

---

## 2️⃣ 설명 (Explanations)

### 2-1. 특정 날짜 예측 설명 조회

AI가 생성한 예측에 대한 자연어 설명을 조회합니다.

```http
GET /api/explanations/{target_date}?commodity={commodity}
```

**Parameters:**
| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `target_date` | string | ✅ | 날짜 (YYYY-MM-DD) |
| `commodity` | string | ✅ | 품목명 |

**Response:**
```json
{
  "id": 1,
  "pred_id": 1,
  "content": "2026년 2월 7일 옥수수 가격은 전날 대비 0.5% 상승할 것으로 예상됩니다. 주요 요인은 달러 지수 하락과 중국의 수요 증가입니다. 10년물 국채 금리가 안정세를 보이면서 투자 심리가 개선되었습니다.",
  "llm_model": "gpt-4",
  "impact_news": [
    {
      "source": "Reuters",
      "title": "중국, 옥수수 수입량 증가 전망",
      "impact_score": 8,
      "analysis": "중국의 축산업 성장으로 옥수수 수요가 증가하고 있습니다."
    },
    {
      "source": "Bloomberg",
      "title": "달러 지수 3개월 만에 최저치",
      "impact_score": 7,
      "analysis": "달러 약세로 원자재 가격 상승 압력이 커지고 있습니다."
    }
  ],
  "created_at": "2026-02-06T12:00:00"
}
```

---

## 3️⃣ 시뮬레이션 (Simulation)

### 3-1. What-If 시뮬레이션

특정 조건을 변경했을 때 예측 가격이 어떻게 변하는지 시뮬레이션합니다.

```http
POST /api/simulate
```

**Request Body:**
```json
{
  "commodity": "corn",
  "base_date": "2026-02-06",
  "feature_overrides": {
    "10Y_Yield": 4.5,
    "USD_Index": 105.0,
    "pdsi": -2.0
  }
}
```

**Parameters:**
| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `commodity` | string | ✅ | 품목명 |
| `base_date` | string | ✅ | 기준 날짜 (YYYY-MM-DD) |
| `feature_overrides` | object | ✅ | 변경할 Feature들 |

**조정 가능한 Features:**
| Feature | 설명 | 범위 |
|---------|------|------|
| `10Y_Yield` | 미국 10년물 국채 금리 (%) | 0 ~ 10 |
| `USD_Index` | 달러 인덱스 | 80 ~ 120 |
| `pdsi` | Palmer Drought Severity Index | -6 ~ 6 |
| `spi30d` | 30일 강수량 지수 | -3 ~ 3 |
| `spi90d` | 90일 강수량 지수 | -3 ~ 3 |

**Response:**
```json
{
  "original_forecast": 450.50,
  "simulated_forecast": 453.25,
  "change": 2.75,
  "change_percent": 0.61,
  "feature_impacts": [
    {
      "feature": "10Y_Yield",
      "current_value": 4.2,
      "new_value": 4.5,
      "value_change": 0.3,
      "contribution": 0
    },
    {
      "feature": "USD_Index",
      "current_value": 103.5,
      "new_value": 105.0,
      "value_change": 1.5,
      "contribution": 0
    },
    {
      "feature": "pdsi",
      "current_value": -1.0,
      "new_value": -2.0,
      "value_change": -1.0,
      "contribution": 0
    }
  ]
}
```

---

## 4️⃣ 뉴스 (News)

### 4-1. 뉴스 목록 조회

최신 뉴스 데이터를 조회합니다.

```http
GET /api/newsdb?skip={skip}&limit={limit}
```

**Parameters:**
| 이름 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| `skip` | integer | ❌ | 0 | 건너뛸 개수 |
| `limit` | integer | ❌ | 10 | 조회할 개수 |

**Response:**
```json
[
  {
    "id": 1,
    "title": "중국, 옥수수 수입량 증가 전망",
    "content": "중국의 축산업 성장으로 옥수수 수요가 증가하고 있습니다...",
    "source_url": "https://reuters.com/article/...",
    "created_at": "2026-02-06T10:30:00"
  },
  {
    "id": 2,
    "title": "미국 옥수수 재배 면적 감소",
    "content": "올해 미국의 옥수수 재배 면적이 전년 대비 5% 감소할 것으로...",
    "source_url": "https://bloomberg.com/article/...",
    "created_at": "2026-02-06T09:15:00"
  }
]
```

---

## 5️⃣ 시장 지표 (Market Metrics)

### 6-1. 특정 날짜 시장 지표 조회

특정 날짜의 모든 시장 지표를 조회합니다.

```http
GET /api/market-metrics?commodity={commodity}&date={date}
```

**Parameters:**
| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `commodity` | string | ✅ | 품목명 |
| `date` | string | ✅ | 날짜 (YYYY-MM-DD) |

**Response:**
```json
{
  "commodity": "corn",
  "date": "2026-02-06",
  "metrics": [
    {
      "metric_id": "10Y_Yield",
      "label": "미국 10년물 국채 금리",
      "value": "4.2%",
      "numeric_value": 4.2,
      "trend": 0.1,
      "impact": "neutral"
    },
    {
      "metric_id": "USD_Index",
      "label": "달러 인덱스",
      "value": "103.5",
      "numeric_value": 103.5,
      "trend": -0.5,
      "impact": "positive"
    },
    {
      "metric_id": "pdsi",
      "label": "Palmer 가뭄 지수",
      "value": "-1.0",
      "numeric_value": -1.0,
      "trend": -0.2,
      "impact": "negative"
    }
  ]
}
```

---

## ⚠️ 에러 처리

### 에러 응답 형식

```json
{
  "detail": "에러 메시지"
}
```

### 일반적인 에러

#### 404 Not Found
```json
{
  "detail": "corn의 최신 예측 데이터가 없습니다."
}
```

#### 400 Bad Request
```json
{
  "detail": "조정 불가능한 feature: {'invalid_feature'}. 가능한 features: {'10Y_Yield', 'USD_Index', ...}"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "시뮬레이션 예측에 실패했습니다."
}
```

---

## 📘 타입 정의

### TypeScript 타입 정의

```typescript
// 예측 데이터
interface Prediction {
  id: number;
  target_date: string;  // YYYY-MM-DD
  commodity: string;
  price_pred: number;
  conf_lower: number;
  conf_upper: number;
  top1_factor?: string;
  top1_impact?: number;
  top2_factor?: string;
  top2_impact?: number;
  top3_factor?: string;
  top3_impact?: number;
  top4_factor?: string;
  top4_impact?: number;
  top5_factor?: string;
  top5_impact?: number;
  // ... top6 ~ top20
  model_type: string;
  created_at: string;  // ISO 8601
}

// 설명 데이터
interface ImpactNews {
  source: string;
  title: string;
  impact_score: number;
  analysis: string;
}

interface Explanation {
  id: number;
  pred_id: number;
  content: string;
  llm_model: string;
  impact_news: ImpactNews[];
  created_at: string;
}

// 시뮬레이션
interface SimulationRequest {
  commodity: string;
  base_date: string;
  feature_overrides: {
    [key: string]: number;
  };
}

interface FeatureImpact {
  feature: string;
  current_value: number;
  new_value: number;
  value_change: number;
  contribution: number;
}

interface SimulationResponse {
  original_forecast: number;
  simulated_forecast: number;
  change: number;
  change_percent: number;
  feature_impacts: FeatureImpact[];
}

// 뉴스
interface News {
  id: number;
  title: string;
  content: string;
  source_url?: string;
  created_at: string;
}

// 실제 가격
interface HistoricalPrice {
  date: string;
  actual_price: number;
}

// 예측 + 실제 가격 통합 응답
interface PredictionsWithPricesResponse {
  predictions: Prediction[];
  historical_prices: HistoricalPrice[];
}

// 시장 지표
interface MarketMetric {
  metric_id: string;
  label: string;
  value: string;
  numeric_value: number;
  trend: number;
  impact: 'positive' | 'negative' | 'neutral';
}

interface MarketMetricsResponse {
  commodity: string;
  date: string;
  metrics: MarketMetric[];
}
```