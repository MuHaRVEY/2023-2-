#버드 스트라이킹 데이터 분석
# import os
# print(os.getcwd())
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 데이터셋 불러오기
file_path = 'C:/Users/rkddn/OneDrive/바탕 화면/archive/STRIKE_REPORTS.csv'
bird_strike_data = pd.read_csv(file_path)

# 데이터셋의 첫 몇 줄을 출력하여 구조 확인
# print(bird_strike_data.head())

# 초기 분석을 위한 준비
# INCIDENT_DATE를 datetime 객체 형식으로 변환
bird_strike_data['INCIDENT_DATE'] = pd.to_datetime(bird_strike_data['INCIDENT_DATE'], errors='coerce') # 연도, 월, 일 모든 정보를 포함 


# 연도별, 월별, 시간대별 그룹화
yearly_incidents = bird_strike_data.groupby(bird_strike_data['INCIDENT_DATE'].dt.year).size()
monthly_incidents = bird_strike_data.groupby(bird_strike_data['INCIDENT_DATE'].dt.month).size()

# 시간대별 그룹화 (TIME_OF_DAY 열 사용)
hourly_incidents = bird_strike_data.groupby('TIME_OF_DAY').size()

# 연도별 그래프
plt.figure(figsize=(15, 5))
sns.lineplot(x=yearly_incidents.index, y=yearly_incidents.values)
plt.title('Yearly Bird Strikes Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Incidents')
plt.show()

# 월별 그래프
plt.figure(figsize=(15, 5))
sns.lineplot(x=monthly_incidents.index, y=monthly_incidents.values)
plt.title('Monthly Bird Strikes Over Time')
plt.xlabel('Month')
plt.ylabel('Number of Incidents')
plt.show()

# 시간대별 그래프
plt.figure(figsize=(15, 5))
sns.barplot(x=hourly_incidents.index, y=hourly_incidents.values)
plt.title('Bird Strikes by Time of Day')
plt.xlabel('Time of Day')
plt.ylabel('Number of Incidents')
plt.show()

# 추가 분석을 위한 데이터 전처리
# INCIDENT_DATE가 NaT인 행 삭제
bird_strike_data_cleaned = bird_strike_data.dropna(subset=['INCIDENT_DATE'])

# 공항별 분석
airport_incidents = bird_strike_data_cleaned.groupby('AIRPORT').size().sort_values(ascending=False).head(10)

# 조류 크기별 분석
size_incidents = bird_strike_data_cleaned.groupby('SIZE').size()

# 추가 그래프를 위한 Matplotlib 설정
plt.figure(figsize=(18, 6))

# 첫 번째 서브플롯: 가장 많은 버드 스트라이킹이 발생한 상위 10개 공항
plt.subplot(1, 3, 1)
sns.barplot(x=airport_incidents.values, y=airport_incidents.index)
plt.title('Top 10 Airports with Most Bird Strikes')
plt.xlabel('Number of Incidents')
plt.ylabel('Airport')

# 두 번째 서브플롯: 조류 크기별 버드 스트라이킹 발생 건수
plt.subplot(1, 3, 2)
size_incidents.plot(kind='bar')
plt.title('Bird Strikes by Bird Size')
plt.xlabel('Bird Size')
plt.ylabel('Number of Incidents')


#코드 추가 버드 스타라이킹 발생 평균 속도 구하기
bird_strike_data['SPEED'] = pd.to_numeric(bird_strike_data['SPEED'], errors='coerce')
bird_strike_data_speed = bird_strike_data.dropna(subset=['SPEED'])

speed_incidents_count = bird_strike_data_speed.groupby('SPEED').size()
speed_incidents_mean = bird_strike_data_speed.groupby('SPEED')['SPEED'].mean()

plt.figure(figsize=(15, 6))

sns.lineplot(x=speed_incidents_count.index, y=speed_incidents_count.values, label='Number of Incidents')

sns.lineplot(x=speed_incidents_mean.index, y=speed_incidents_mean.values, label='Average Speed')

plt.title('Bird Strikes Analysis by Aircraft Speed')
plt.xlabel('Speed (knots)')
plt.ylabel('Count / Average Speed')
plt.xticks(rotation=45)
plt.legend()

#고도 관련 코드 추가 
bird_strike_data['HEIGHT'] = pd.to_numeric(bird_strike_data['HEIGHT'], errors='coerce')
bird_strike_data_height = bird_strike_data.dropna(subset=['HEIGHT'])

height_incidents_sum = bird_strike_data_height.groupby('HEIGHT')['HEIGHT'].sum()
height_incidents_mean = bird_strike_data_height.groupby('HEIGHT')['HEIGHT'].mean()

plt.figure(figsize=(15, 6))

sns.lineplot(x=height_incidents_sum.index, y=height_incidents_sum.values, label='Sum of Incidents')

sns.lineplot(x=height_incidents_mean.index, y=height_incidents_mean.values, label='Average Height')

plt.title('Bird Strikes Analysis by Aircraft Height')
plt.xlabel('Height (feet)')
plt.ylabel('Sum of Incidents / Average Height')
plt.xticks(rotation=45)
plt.legend()

#레이아웃 조정 
plt.tight_layout()
plt.show()


