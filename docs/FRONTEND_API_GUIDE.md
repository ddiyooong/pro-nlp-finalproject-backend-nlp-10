# 🌐 프론트엔드 API 가이드

**버전**: 1.0.0  
**최종 업데이트**: 2026-02-06  
**Base URL**: `http://localhost:8000` (개발) / `https://api.yourdomain.com` (프로덕션)

---

## 📋 목차

1. [시작하기](#-시작하기)
2. [API 개요](#-api-개요)
3. [인증](#-인증)
4. [공통 응답 형식](#-공통-응답-형식)
5. [API 엔드포인트](#-api-엔드포인트)
   - [예측 (Predictions)](#1️⃣-예측-predictions)
   - [설명 (Explanations)](#2️⃣-설명-explanations)
   - [시뮬레이션 (Simulation)](#3️⃣-시뮬레이션-simulation)
   - [뉴스 (News)](#4️⃣-뉴스-news)
   - [실제 가격 (Historical Prices)](#5️⃣-실제-가격-historical-prices)
   - [시장 지표 (Market Metrics)](#6️⃣-시장-지표-market-metrics)
6. [에러 처리](#-에러-처리)
7. [타입 정의](#-타입-정의)
8. [코드 예시](#-코드-예시)

---

## 🚀 시작하기

### API 문서 접속

서버 실행 후 브라우저에서 다음 주소로 접속:

```
http://localhost:8000/docs          # Swagger UI
http://localhost:8000/redoc         # ReDoc
```

### 빠른 테스트

```bash
# 최신 예측 조회
curl "http://localhost:8000/api/predictions?commodity=corn"

# 특정 날짜 예측 조회
curl "http://localhost:8000/api/predictions/2026-02-06?commodity=corn"
```

---

## 📡 API 개요

### 기본 정보

| 항목 | 값 |
|------|-----|
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

```javascript
// 향후 예상 형식
headers: {
  'Authorization': 'Bearer YOUR_API_KEY'
}
```

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

### 1-1. 최신 예측 목록 조회

가장 최근 배치에서 생성된 예측 데이터를 조회합니다.  
범위: 오늘 기준 과거 30일 ~ 미래 60일

```http
GET /api/predictions?commodity={commodity}
```

**Parameters:**
| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `commodity` | string | ✅ | 품목명 (예: "corn") |

**Response:**
```json
[
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
  },
  // ... more predictions
]
```

**사용 예시:**
```javascript
// JavaScript/TypeScript
const response = await fetch(
  'http://localhost:8000/api/predictions?commodity=corn'
);
const predictions = await response.json();

console.log(`총 ${predictions.length}개의 예측 데이터`);
predictions.forEach(pred => {
  console.log(`${pred.target_date}: $${pred.price_pred}`);
});
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

**사용 예시:**
```javascript
const targetDate = '2026-02-07';
const response = await fetch(
  `http://localhost:8000/api/predictions/${targetDate}?commodity=corn`
);
const prediction = await response.json();

console.log(`${targetDate} 예측 가격: $${prediction.price_pred}`);
console.log(`신뢰 구간: $${prediction.conf_lower} ~ $${prediction.conf_upper}`);

// Top 5 영향 요인 표시
for (let i = 1; i <= 5; i++) {
  const factor = prediction[`top${i}_factor`];
  const impact = prediction[`top${i}_impact`];
  if (factor && impact) {
    console.log(`${i}. ${factor}: ${(impact * 100).toFixed(2)}%`);
  }
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

**사용 예시:**
```javascript
const targetDate = '2026-02-07';
const response = await fetch(
  `http://localhost:8000/api/explanations/${targetDate}?commodity=corn`
);
const explanation = await response.json();

console.log('📊 AI 분석:', explanation.content);
console.log('\n📰 영향력 있는 뉴스:');
explanation.impact_news.forEach((news, index) => {
  console.log(`${index + 1}. [${news.source}] ${news.title}`);
  console.log(`   영향도: ${news.impact_score}/10`);
  console.log(`   분석: ${news.analysis}`);
});
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
| `close` | 종가 | > 0 |
| `open` | 시가 | > 0 |
| `high` | 고가 | > 0 |
| `low` | 저가 | > 0 |
| `volume` | 거래량 | > 0 |
| `news_count` | 뉴스 개수 | >= 0 |

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

**사용 예시:**
```javascript
// 금리 인상 시나리오 시뮬레이션
const simulateRateHike = async () => {
  const response = await fetch('http://localhost:8000/api/simulate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      commodity: 'corn',
      base_date: '2026-02-06',
      feature_overrides: {
        '10Y_Yield': 5.0,  // 금리 5%로 상승
        'USD_Index': 110.0  // 달러 강세
      }
    })
  });
  
  const result = await response.json();
  
  console.log('원본 예측:', result.original_forecast);
  console.log('시뮬레이션 예측:', result.simulated_forecast);
  console.log('변화:', `${result.change > 0 ? '+' : ''}${result.change}`);
  console.log('변화율:', `${result.change_percent}%`);
  
  return result;
};

// 가뭄 시나리오
const simulateDrought = async () => {
  const response = await fetch('http://localhost:8000/api/simulate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      commodity: 'corn',
      base_date: '2026-02-06',
      feature_overrides: {
        'pdsi': -3.0,      // 심한 가뭄
        'spi30d': -2.0,
        'spi90d': -1.5
      }
    })
  });
  
  return await response.json();
};
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

**사용 예시:**
```javascript
// 페이지네이션
const fetchNews = async (page = 1, pageSize = 10) => {
  const skip = (page - 1) * pageSize;
  const response = await fetch(
    `http://localhost:8000/api/newsdb?skip=${skip}&limit=${pageSize}`
  );
  const news = await response.json();
  
  return {
    items: news,
    page,
    pageSize,
    hasMore: news.length === pageSize
  };
};

// 무한 스크롤
let currentPage = 1;
const loadMoreNews = async () => {
  const data = await fetchNews(currentPage, 20);
  currentPage++;
  return data;
};
```

---

## 5️⃣ 실제 가격 (Historical Prices)

### 5-1. 기간별 실제 가격 조회

특정 기간의 실제 거래 가격을 조회합니다.

```http
GET /api/historical-prices?commodity={commodity}&start_date={start_date}&end_date={end_date}
```

**Parameters:**
| 이름 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `commodity` | string | ✅ | 품목명 |
| `start_date` | string | ✅ | 시작 날짜 (YYYY-MM-DD) |
| `end_date` | string | ✅ | 종료 날짜 (YYYY-MM-DD) |

**Response:**
```json
{
  "commodity": "corn",
  "start_date": "2026-01-01",
  "end_date": "2026-01-31",
  "prices": [
    {
      "date": "2026-01-01",
      "actual_price": 448.25
    },
    {
      "date": "2026-01-02",
      "actual_price": 449.50
    },
    // ... more prices
  ]
}
```

**사용 예시:**
```javascript
// 차트 데이터 준비
const fetchPriceChartData = async (startDate, endDate) => {
  const response = await fetch(
    `http://localhost:8000/api/historical-prices?` +
    `commodity=corn&start_date=${startDate}&end_date=${endDate}`
  );
  const data = await response.json();
  
  // Chart.js 형식으로 변환
  return {
    labels: data.prices.map(p => p.date),
    datasets: [{
      label: '실제 가격',
      data: data.prices.map(p => p.actual_price),
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  };
};

// 최근 30일 가격
const getRecentPrices = async (days = 30) => {
  const endDate = new Date().toISOString().split('T')[0];
  const startDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000)
    .toISOString().split('T')[0];
  
  return await fetchPriceChartData(startDate, endDate);
};
```

---

## 6️⃣ 시장 지표 (Market Metrics)

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

**사용 예시:**
```javascript
// 시장 지표 대시보드
const fetchMarketDashboard = async (date) => {
  const response = await fetch(
    `http://localhost:8000/api/market-metrics?commodity=corn&date=${date}`
  );
  const data = await response.json();
  
  // 영향도별 분류
  const positive = data.metrics.filter(m => m.impact === 'positive');
  const negative = data.metrics.filter(m => m.impact === 'negative');
  const neutral = data.metrics.filter(m => m.impact === 'neutral');
  
  return {
    positive,
    negative,
    neutral,
    all: data.metrics
  };
};

// 특정 지표 추적
const trackMetric = async (metricId, days = 7) => {
  const metrics = [];
  const today = new Date();
  
  for (let i = 0; i < days; i++) {
    const date = new Date(today - i * 24 * 60 * 60 * 1000)
      .toISOString().split('T')[0];
    
    const response = await fetch(
      `http://localhost:8000/api/market-metrics?commodity=corn&date=${date}`
    );
    const data = await response.json();
    const metric = data.metrics.find(m => m.metric_id === metricId);
    
    if (metric) {
      metrics.push({
        date,
        value: metric.numeric_value,
        trend: metric.trend
      });
    }
  }
  
  return metrics.reverse();
};
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

### 에러 처리 예시

```javascript
// TypeScript
interface ApiError {
  detail: string;
}

const fetchWithErrorHandling = async (url: string) => {
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.detail);
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      console.error('API 에러:', error.message);
      // 사용자에게 친절한 메시지 표시
      if (error.message.includes('없습니다')) {
        alert('요청하신 데이터를 찾을 수 없습니다.');
      } else {
        alert('오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
      }
    }
    throw error;
  }
};
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

interface HistoricalPricesResponse {
  commodity: string;
  start_date: string;
  end_date: string;
  prices: HistoricalPrice[];
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

---

## 💻 코드 예시

### React 예시

```typescript
// hooks/usePredictions.ts
import { useState, useEffect } from 'react';

export const usePredictions = (commodity: string) => {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        setLoading(true);
        const response = await fetch(
          `http://localhost:8000/api/predictions?commodity=${commodity}`
        );
        
        if (!response.ok) {
          throw new Error('예측 데이터를 불러오는데 실패했습니다.');
        }
        
        const data = await response.json();
        setPredictions(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : '알 수 없는 오류');
      } finally {
        setLoading(false);
      }
    };

    fetchPredictions();
  }, [commodity]);

  return { predictions, loading, error };
};

// components/PredictionChart.tsx
import React from 'react';
import { Line } from 'react-chartjs-2';
import { usePredictions } from '../hooks/usePredictions';

export const PredictionChart: React.FC = () => {
  const { predictions, loading, error } = usePredictions('corn');

  if (loading) return <div>로딩 중...</div>;
  if (error) return <div>에러: {error}</div>;

  const chartData = {
    labels: predictions.map(p => p.target_date),
    datasets: [
      {
        label: '예측 가격',
        data: predictions.map(p => p.price_pred),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
      },
      {
        label: '신뢰 구간 (상한)',
        data: predictions.map(p => p.conf_upper),
        borderColor: 'rgba(255, 99, 132, 0.5)',
        borderDash: [5, 5],
      },
      {
        label: '신뢰 구간 (하한)',
        data: predictions.map(p => p.conf_lower),
        borderColor: 'rgba(255, 99, 132, 0.5)',
        borderDash: [5, 5],
      },
    ],
  };

  return <Line data={chartData} />;
};
```

### Vue 예시

```vue
<!-- components/SimulationForm.vue -->
<template>
  <div class="simulation-form">
    <h2>가격 시뮬레이션</h2>
    
    <form @submit.prevent="runSimulation">
      <div class="form-group">
        <label>기준 날짜:</label>
        <input type="date" v-model="baseDate" required />
      </div>
      
      <div class="form-group">
        <label>10년물 국채 금리 (%):</label>
        <input type="number" v-model.number="features.yield" step="0.1" />
      </div>
      
      <div class="form-group">
        <label>달러 인덱스:</label>
        <input type="number" v-model.number="features.usd" step="0.1" />
      </div>
      
      <div class="form-group">
        <label>PDSI (가뭄 지수):</label>
        <input type="number" v-model.number="features.pdsi" step="0.1" />
      </div>
      
      <button type="submit" :disabled="loading">
        {{ loading ? '계산 중...' : '시뮬레이션 실행' }}
      </button>
    </form>
    
    <div v-if="result" class="result">
      <h3>시뮬레이션 결과</h3>
      <p>원본 예측: ${{ result.original_forecast }}</p>
      <p>시뮬레이션 예측: ${{ result.simulated_forecast }}</p>
      <p :class="result.change >= 0 ? 'positive' : 'negative'">
        변화: {{ result.change >= 0 ? '+' : '' }}${{ result.change }}
        ({{ result.change_percent }}%)
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const baseDate = ref(new Date().toISOString().split('T')[0]);
const features = ref({
  yield: null,
  usd: null,
  pdsi: null,
});
const loading = ref(false);
const result = ref<SimulationResponse | null>(null);

const runSimulation = async () => {
  loading.value = true;
  
  try {
    const featureOverrides: any = {};
    if (features.value.yield !== null) featureOverrides['10Y_Yield'] = features.value.yield;
    if (features.value.usd !== null) featureOverrides['USD_Index'] = features.value.usd;
    if (features.value.pdsi !== null) featureOverrides['pdsi'] = features.value.pdsi;
    
    const response = await fetch('http://localhost:8000/api/simulate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        commodity: 'corn',
        base_date: baseDate.value,
        feature_overrides: featureOverrides,
      }),
    });
    
    if (!response.ok) {
      throw new Error('시뮬레이션 실행 실패');
    }
    
    result.value = await response.json();
  } catch (error) {
    console.error('에러:', error);
    alert('시뮬레이션 실행 중 오류가 발생했습니다.');
  } finally {
    loading.value = false;
  }
};
</script>
```

### Axios 래퍼 예시

```typescript
// api/client.ts
import axios, { AxiosError } from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// 에러 인터셉터
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response) {
      const data = error.response.data as { detail: string };
      console.error('API 에러:', data.detail);
    } else if (error.request) {
      console.error('네트워크 에러: 응답 없음');
    } else {
      console.error('에러:', error.message);
    }
    return Promise.reject(error);
  }
);

// API 함수들
export const predictionApi = {
  getLatest: (commodity: string) =>
    apiClient.get<Prediction[]>(`/api/predictions`, { params: { commodity } }),
  
  getByDate: (commodity: string, targetDate: string) =>
    apiClient.get<Prediction>(`/api/predictions/${targetDate}`, { params: { commodity } }),
};

export const simulationApi = {
  run: (data: SimulationRequest) =>
    apiClient.post<SimulationResponse>('/api/simulate', data),
};

export const newsApi = {
  getList: (skip = 0, limit = 10) =>
    apiClient.get<News[]>('/api/newsdb', { params: { skip, limit } }),
};

export const priceApi = {
  getHistorical: (commodity: string, startDate: string, endDate: string) =>
    apiClient.get<HistoricalPricesResponse>('/api/historical-prices', {
      params: { commodity, start_date: startDate, end_date: endDate },
    }),
};

export const metricsApi = {
  getByDate: (commodity: string, date: string) =>
    apiClient.get<MarketMetricsResponse>('/api/market-metrics', {
      params: { commodity, date },
    }),
};

// 사용 예시
const loadDashboard = async () => {
  try {
    const [predictions, news, prices] = await Promise.all([
      predictionApi.getLatest('corn'),
      newsApi.getList(0, 5),
      priceApi.getHistorical('corn', '2026-01-01', '2026-02-06'),
    ]);
    
    return {
      predictions: predictions.data,
      news: news.data,
      prices: prices.data,
    };
  } catch (error) {
    console.error('대시보드 로드 실패:', error);
    throw error;
  }
};
```

---

## 🔗 추가 리소스

### API 문서
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 관련 문서
- [프로젝트 README](../README.md)
- [TFT 구현 상세](./TFT_IMPLEMENTATION_SUMMARY.md)
- [환경 설정 가이드](./ENV_SETUP_GUIDE.md)

### 지원
- 이슈 제보: GitHub Issues
- 문의: dev@example.com

---

**작성일**: 2026-02-06  
**버전**: 1.0.0  
**라이선스**: MIT
