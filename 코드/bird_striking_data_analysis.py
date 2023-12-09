import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 데이터셋 불러오기
file_path = 'C:/Users/rkddn/OneDrive/바탕 화면/archive/STRIKE_REPORTS.csv'
bird_strike_data = pd.read_csv(file_path)

# 날짜 및 속도, 고도 형식으로 변환
bird_strike_data['INCIDENT_DATE'] = pd.to_datetime(bird_strike_data['INCIDENT_DATE'], errors='coerce')
bird_strike_data['SPEED'] = pd.to_numeric(bird_strike_data['SPEED'], errors='coerce')
bird_strike_data['HEIGHT'] = pd.to_numeric(bird_strike_data['HEIGHT'], errors='coerce')

# 연도별, 월별, 시간대별, 속도별, 고도별 그룹화 및 분석
yearly_incidents = bird_strike_data.groupby(bird_strike_data['INCIDENT_DATE'].dt.year).size()
monthly_incidents = bird_strike_data.groupby(bird_strike_data['INCIDENT_DATE'].dt.month).size()
hourly_incidents = bird_strike_data.groupby('TIME_OF_DAY').size()
speed_incidents_count = bird_strike_data.dropna(subset=['SPEED']).groupby('SPEED').size()
speed_incidents_mean = bird_strike_data.dropna(subset=['SPEED']).groupby('SPEED')['SPEED'].mean()
height_incidents_sum = bird_strike_data.dropna(subset=['HEIGHT']).groupby('HEIGHT').sum()
height_incidents_mean = bird_strike_data.dropna(subset=['HEIGHT']).groupby('HEIGHT')['HEIGHT'].mean()

# 연도별 그래프
plt.figure(figsize=(15, 5))
sns.lineplot(x=yearly_incidents.index, y=yearly_incidents.values)
plt.title('Yearly Bird Strikes Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Incidents')

# 월별 그래프
plt.figure(figsize=(15, 5))
sns.lineplot(x=monthly_incidents.index, y=monthly_incidents.values)
plt.title('Monthly Bird Strikes Over Time')
plt.xlabel('Month')
plt.ylabel('Number of Incidents')

# 시간대별 그래프
plt.figure(figsize=(15, 5))
sns.barplot(x=hourly_incidents.index, y=hourly_incidents.values)
plt.title('Bird Strikes by Time of Day')
plt.xlabel('Time of Day')
plt.ylabel('Number of Incidents')

# 속도별 그래프
plt.figure(figsize=(15, 6))
sns.lineplot(x=speed_incidents_count.index, y=speed_incidents_count.values, label='Number of Incidents')
sns.lineplot(x=speed_incidents_mean.index, y=speed_incidents_mean.values, label='Average Speed')
plt.title('Bird Strikes Analysis by Aircraft Speed')
plt.xlabel('Speed (knots)')
plt.ylabel('Count / Average Speed')
plt.legend()

# 고도별 그래프
plt.figure(figsize=(15, 6))
sns.lineplot(x=height_incidents_sum.index, y=height_incidents_sum.values, label='Sum of Incidents')
sns.lineplot(x=height_incidents_mean.index, y=height_incidents_mean.values, label='Average Height')
plt.title('Bird Strikes Analysis by Aircraft Height')
plt.xlabel('Height (feet)')
plt.ylabel('Sum of Incidents / Average Height')
plt.legend()

# 레이아웃 조정
plt.tight_layout()
plt.show()
