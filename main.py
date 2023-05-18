from MyFunctions import *

# 수집할 날짜는 "20200201" ~ "20200601"

#ProcessCoronaData("20200201", "20200601", 0)
#ProcessCoronaDataDay("20200201", "20200601", 0)
#ProcessAirQualityData("20200201", "20200601", 'no2')
#ProcessAirQualityData("20200201", "20200601", 'o3')
#ProcessAirQualityData("20200201", "20200601", 'co')
#ProcessAirQualityData("20200201", "20200601", 'so2')
#ProcessAirQualityData("20200201", "20200601", 'pm10')
#ProcessAirQualityData("20200201", "20200601", 'pm25')
ProcessBus("20200201", "20200601")
ProcessSubway("20200201", "20200601")
