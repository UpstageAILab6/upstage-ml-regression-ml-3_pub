[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/pjJxrz8e)
# 3조 (Go-Getters)
## Team

| ![손봉교](image/001.png) | ![김연준](image/002.png) | ![노지연](image/003.png) | ![박인수](image/004.png) | ![하선영](image/005.png) |
| :--------------------------------------------------------------: | :--------------------------------------------------------------: | :--------------------------------------------------------------: | :--------------------------------------------------------------: | :--------------------------------------------------------------: |
|            [손봉교(팀장)](https://github.com/imsonn94/)             |            [김연준(팀원)](https://github.com/Kim-Yeon-Jun)             |            [노지연(팀원)](https://github.com/jy239847)             |            [박인수(팀원)](https://github.com/insu97)             |            [하선영(팀원)](https://github.com/oohna-na)             |
|                            데이터 전처리, 모델 학습 (LightGBM), github 관리 및 회의록 작성                             |                        데이터 전처리, 모델 학습(LightGBM), 하이퍼파라미터 테스트   |                        데이터 전처리, 모델 학습(Random Forest)                  |                        데이터 전처리, 모델 학습 (Xgboost), 코드리뷰, 변수 통계분석  |                            데이터 전처리, Feature Engineering, 코드리뷰                             |

## 0. Overview
### Environment
- Python Version: 3.10.13

### Requirements
- lightgbm : 4.5.0
- numpy : 1.23.5
- pandas : 1.5.3
- scikit-learn : 1.2.2
- xgboost : 2.1.3

## 1. Competiton Info

### Overview

- 서울 아파트 실거래가 데이터를 기반으로 아파트 가격 예측 

### Timeline

- Start Date : 2024 / 12 / 23
- Final submission deadline : 2025 / 01 / 07

## 2. Components

### Directory

```
|-- README.md
|-- bkson
|   |-- model_light_gbm-4_by3_parameter_del-3.ipynb
|   |-- model_light_gbm-4_by3_parameter_del-kfold.ipynb
|   `-- preprocess3.ipynb
|-- image
|   |-- 001.png
|   |-- 002.png
|   |-- 003.png
|   |-- 004.png
|   `-- 005.png
|-- ispark
|   |-- code
|   |   |-- model.ipynb
|   |   |-- model_01.ipynb
|   |   |-- model_02.ipynb
|   |   |-- preprocess.ipynb
|   |   |-- preprocess_02.ipynb
|   |   |-- preprocess_03.ipynb
|   |   `-- preprocess_06.ipynb
|   `-- data
|       |-- pre_test.csv
|       |-- pre_train.csv
|       |-- target.csv
|       |-- test.csv
|       `-- train.csv
|-- jynoh
|   |-- test2ny.py
|   `-- testny1.py
|-- schools.csv
|-- schools_new.csv
|-- syhah
|   |-- code
|   |   `-- add_school_coordinates.ipynb
|   `-- data
|       |-- seoul_high_school_with_coords.csv
|       `-- seoul_middle_school_with_coords.csv
`-- yjkim
    |-- 0_EDA.ipynb
    |-- 1_Preprocessing.ipynb
    |-- 1_Preprocessing_subbus.ipynb
    |-- 2_Model_Train.ipynb
    |-- data.md
    `-- testfile
        `-- base_lgbm.ipynb
```

## 3. Data descrption

### 사전 데이터 분석

- 데이터 분석 방법 : 피어슨 상관계수, p-value 활용
- 데이터 시각화 작업
- 결측치/이상치 처리방안 모색

### EDA

- 결측치 과다 feature 제거 : 결측치가 전체 데이터 70% 넘으면 feature 삭제
- 카카오맵 API 사용 X,Y 좌표(위경도) 복원
- 주소
    - 시군구(구 / 동) : One-Hot Encoding / Label Encoding
    - 도로명 : Label Encoding
    - 본번, 부번 : 결측치 있는 row 제거
    - 번지 : 중복 데이터로 제거 
- 아파트명 : Label Encoding (아파트명 결측치의 경우 동일한 도로명 주소로 기타1~337 아파트로 rename 먼저 수행)
- 층 : 데이터내 음수 값 이상치로 판단
- 전용면적 : 400 제곱미터의 아파트가 실제로 존재함을 확인
- 평수 : 전용면적에 3.3을 나누어 계산
- Target(Y ;시세) : 모델 학습시에 이상치에 덜 민감하게 하기위한 Log Transform 수행

### 파생변수 생성

- 계약년월일 (년도, 월) 분리 
- 건축년도별 평균거래가 가중치
- 계약년도별 평균거래가 가중치
- 인접 지하철거리
- 인접 학군

## 4. Modeling

### 모델 선택 및 수행

- LightGBM : 머신러닝 대회에서 가장 많이 사용되는 범용성 있는 모델 (빠르고 복잡한 데이터에서 성능 보장됨)
- 기본 하이퍼 파라미터 세팅 : GBDT, RMSE, 트리깊이=8, 리프노드_최대=31, 학습률=0.05...
- Trainig/Valid Ratio = `7 : 3`
- Total Feature Number : `41`

## 5. Result
- Scenario 1 : 학습률 조정 (0.05 ->  0.01)
    - 모델 학습시간 증가 / Iteration 증가 / RMSE 소폭 감소
- Scenario 2 : 평가지표 수정 (RMSE -> MAE)
    - 모델 학습시간 증가 / Iteration 증가 / RMSE 유의미한 차이 없음
- Scenario 3 : 앙상블 적용 (5개 앙상블 평균)
    - 모델 학습시간 큰 폭으로 증가 / Iteration 증가 / RMSE 소폭 증가
- `Scenario 4 : 데이터 선택시 K-fold 분할 적용 (fold 개수 5개)`
    - 모델 학습시간 큰 폭으로 증가 / Iteration 증가 / RMSE 감소 (학습률을 낮출 경우 RMSE는 더 떨어짐)


### Leader Board
- Public RMSE Score : `12,678 / 12,736`
- Private RMSE Score (최종) : `11,041 / 11,107`
- diff : `1,637 / 1,629`

### Presentation
- [Notion 업로드 발표자료](https://www.notion.so/3-_Go-Getters-2b8713409cb94250b85ceba968888adf?pvs=4#34083ead316b45d7b6dc015b5cbf78e1)

### Meeting Log
- [회의록](https://www.notion.so/3-_Go-Getters-2b8713409cb94250b85ceba968888adf?pvs=4)
- [인사이트 공유 및 Q&A](https://www.notion.so/Q-A-48e5b50ec4ee4745b66dbf8f45c0a6e2?pvs=4)

