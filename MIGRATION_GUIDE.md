# 데이터베이스 마이그레이션 가이드

## 변경 사항: Top 5 → Top 20 Factor 확장

### 📋 개요
- **대상 테이블**: `tft_pred`
- **추가 컬럼**: `top6_factor` ~ `top20_factor` 및 각각의 `impact` (총 30개 컬럼)
- **목적**: 예측 모델의 영향 요인을 5개에서 20개로 확장

---

## 🔧 마이그레이션 실행 방법

### 방법 1: SQL 파일 실행 (권장)

```bash
# PostgreSQL에 연결
psql -U your_username -d your_database

# SQL 파일 실행
\i migrations/add_top6_to_top20_factors.sql

# 또는 커맨드 라인에서 직접 실행
psql -U your_username -d your_database -f migrations/add_top6_to_top20_factors.sql
```

### 방법 2: Python 스크립트로 실행

```python
from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # SQL 파일 읽기
    with open('migrations/add_top6_to_top20_factors.sql', 'r') as f:
        sql = f.read()
    
    # 실행
    conn.execute(text(sql))
    conn.commit()
    
print("마이그레이션 완료!")
```

### 방법 3: SQLAlchemy 자동 생성 (개발 환경)

```python
# 개발 환경에서만 사용 (데이터 손실 주의!)
from app.database import engine
from app.datatable import Base

# 모든 테이블 재생성
Base.metadata.drop_all(bind=engine)  # 주의: 기존 데이터 삭제됨!
Base.metadata.create_all(bind=engine)
```

---

## 📊 변경된 스키마

### Before (5 factors)
```sql
CREATE TABLE tft_pred (
    id INTEGER PRIMARY KEY,
    target_date DATE,
    commodity VARCHAR(50),
    price_pred NUMERIC(10,2),
    conf_lower NUMERIC(10,2),
    conf_upper NUMERIC(10,2),
    
    top1_factor VARCHAR(255),
    top1_impact FLOAT,
    top2_factor VARCHAR(255),
    top2_impact FLOAT,
    top3_factor VARCHAR(255),
    top3_impact FLOAT,
    top4_factor VARCHAR(255),
    top4_impact FLOAT,
    top5_factor VARCHAR(255),
    top5_impact FLOAT,
    
    created_at TIMESTAMP
);
```

### After (20 factors)
```sql
-- 위 컬럼들 +
    top6_factor VARCHAR(255),
    top6_impact FLOAT,
    top7_factor VARCHAR(255),
    top7_impact FLOAT,
    ...
    top20_factor VARCHAR(255),
    top20_impact FLOAT
```

---

## ✅ 마이그레이션 확인

### 1. 컬럼 추가 확인
```sql
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'tft_pred' 
  AND column_name LIKE 'top%'
ORDER BY column_name;
```

**예상 결과**: 40개 컬럼 (top1_factor ~ top20_factor, top1_impact ~ top20_impact)

### 2. 서버 재시작 및 테스트
```bash
# 서버 재시작
uvicorn main:app --reload

# 테스트 요청
curl http://localhost:8000/api/predictions?commodity=Corn&start_date=2026-01-01&end_date=2026-01-31
```

### 3. API 응답 확인
```json
{
  "id": 1,
  "target_date": "2026-02-10",
  "commodity": "Corn",
  "price_pred": 452.30,
  "conf_lower": 440.00,
  "conf_upper": 465.00,
  "top1_factor": "WTI_Crude_Oil",
  "top1_impact": 3.6,
  ...
  "top20_factor": "Supply_Estimate",
  "top20_impact": 0.1,
  "created_at": "2026-02-04T10:00:00Z"
}
```

---

## 🔄 롤백 방법 (필요시)

```sql
-- top6~top20 컬럼 제거
ALTER TABLE tft_pred 
DROP COLUMN top6_factor,
DROP COLUMN top6_impact,
DROP COLUMN top7_factor,
DROP COLUMN top7_impact,
DROP COLUMN top8_factor,
DROP COLUMN top8_impact,
DROP COLUMN top9_factor,
DROP COLUMN top9_impact,
DROP COLUMN top10_factor,
DROP COLUMN top10_impact,
DROP COLUMN top11_factor,
DROP COLUMN top11_impact,
DROP COLUMN top12_factor,
DROP COLUMN top12_impact,
DROP COLUMN top13_factor,
DROP COLUMN top13_impact,
DROP COLUMN top14_factor,
DROP COLUMN top14_impact,
DROP COLUMN top15_factor,
DROP COLUMN top15_impact,
DROP COLUMN top16_factor,
DROP COLUMN top16_impact,
DROP COLUMN top17_factor,
DROP COLUMN top17_impact,
DROP COLUMN top18_factor,
DROP COLUMN top18_impact,
DROP COLUMN top19_factor,
DROP COLUMN top19_impact,
DROP COLUMN top20_factor,
DROP COLUMN top20_impact;
```

---

## 📝 AI 서버 코드 예시

### 예측 데이터 저장 (20개 factors)
```python
from app.database import SessionLocal
from app.datatable import TftPred
from datetime import date

# Top 20 factors 준비
top_factors = [
    ("WTI_Crude_Oil", 3.6),
    ("Net_Long", 2.1),
    ("Dollar_Index", 1.8),
    ("Weather_Index", 1.2),
    ("Supply_Estimate", 0.9),
    ("Export_Volume", 0.8),
    ("Import_Demand", 0.7),
    ("Storage_Level", 0.6),
    ("Fuel_Cost", 0.5),
    ("Labor_Cost", 0.4),
    ("Transportation", 0.35),
    ("Currency_Rate", 0.3),
    ("Policy_Change", 0.25),
    ("Climate_Pattern", 0.2),
    ("Market_Sentiment", 0.18),
    ("Tech_Innovation", 0.15),
    ("Competition", 0.12),
    ("Regulation", 0.1),
    ("Consumer_Trend", 0.08),
    ("Global_Event", 0.05),
]

# DB에 저장
db = SessionLocal()
try:
    pred_obj = TftPred(
        target_date=date(2026, 2, 10),
        commodity="Corn",
        price_pred=452.30,
        conf_lower=440.00,
        conf_upper=465.00,
        # 동적으로 top1~top20 설정
        **{
            f"top{i+1}_factor": factor
            for i, (factor, _) in enumerate(top_factors)
        },
        **{
            f"top{i+1}_impact": impact
            for i, (_, impact) in enumerate(top_factors)
        }
    )
    db.add(pred_obj)
    db.commit()
    db.refresh(pred_obj)
    
    print(f"예측 저장 완료: ID={pred_obj.id}")
finally:
    db.close()
```

---

## ⚠️ 주의사항

1. **기존 데이터**: 기존 예측 데이터의 top6~top20은 NULL로 설정됨
2. **백업**: 마이그레이션 전 반드시 데이터베이스 백업
3. **프로덕션**: 스테이징 환경에서 먼저 테스트 후 프로덕션 적용
4. **AI 서버 동기화**: AI 서버도 동일한 스키마 사용하므로 함께 업데이트

---

## 📅 마이그레이션 체크리스트

- [ ] 데이터베이스 백업 완료
- [ ] `migrations/add_top6_to_top20_factors.sql` 실행
- [ ] 컬럼 추가 확인 (40개 컬럼)
- [ ] 백엔드 서버 재시작
- [ ] API 테스트 완료
- [ ] AI 서버 스키마 동기화
- [ ] 프론트엔드 테스트 완료

---

**작성일**: 2026-02-04  
**버전**: 1.0.0
