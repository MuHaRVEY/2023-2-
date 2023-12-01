#머신러닝 모델 만들기

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder

# 데이터셋 불러오기
file_path = 'C:/Users/rkddn/OneDrive/바탕 화면/archive/STRIKE_REPORTS.csv'
bird_strike_data = pd.read_csv(file_path) 
bird_strike_data = bird_strike_data.dropna(subset=['TIME_OF_DAY'])
# 원-핫 인코딩으로 범주형 데이터 변환
encoder = OneHotEncoder()
time_of_day_encoded = encoder.fit_transform(bird_strike_data[['TIME_OF_DAY']]).toarray()
time_of_day_encoded_df = pd.DataFrame(time_of_day_encoded, columns=encoder.get_feature_names_out(['TIME_OF_DAY']))


# 'INCIDENT_DATE' 열을 datetime 형식으로 변환하는 것을 추가해야함. 
bird_strike_data['INCIDENT_DATE'] = pd.to_datetime(bird_strike_data['INCIDENT_DATE'], errors='coerce')

# 연도, 월 데이터 추가 
# 이제 'INCIDENT_DATE' 열에서 연도와 월을 추출할 수 있음.
bird_strike_data['INCIDENT_YEAR'] = bird_strike_data['INCIDENT_DATE'].dt.year
bird_strike_data['INCIDENT_MONTH'] = bird_strike_data['INCIDENT_DATE'].dt.month


# 타겟 변수 정의 (DAMAGE 열 존재 여부를 바탕으로)
# INDICATED_DAMAGE 열을 이진 타입(0과 1)으로 변환
bird_strike_data['STRIKE_OCCURRED'] = bird_strike_data['INDICATED_DAMAGE'].notnull().astype(int) 

# 모델에 사용할 특성 선택
X = pd.concat([time_of_day_encoded_df, bird_strike_data[['INCIDENT_YEAR', 'INCIDENT_MONTH']]], axis=1)
y = bird_strike_data['STRIKE_OCCURRED']

# 데이터 길이 확인
assert len(X) == len(y), "X와 Y의 길이가 맞지 않음." #현재 자꾸 호출되는 중임

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# 모델 초기화 및 훈련
model = LogisticRegression()
model.fit(X_train, y_train)

# 모델 테스트 및 성능 평가
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
