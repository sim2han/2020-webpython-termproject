import requests
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup

seoulOpenDataKey = "64654e6c6d73696d3130396f49524671"

def GetHtmlFromInternet(url):
    """(str) -> str
    해당 url의 html을 str로 반환합니다.
    """
    req = requests.get(url)
    html = req.text
    return html

def GetSeoulUrl(dataType, startIndex, endIndex, date):
    """(str, int, int, int, int, int) -> str
    서울열린데이터 광장에 접근할 수 있는 url을 만듭니다.
    >>> GetSeoulUrl("DailyAverageAirQuality", 1, 5, "20200420")
    """
    url = "http://openAPI.seoul.go.kr:8088/" + seoulOpenDataKey + "/xml/"
    url +=  dataType + "/{0}/{1}/".format(startIndex, endIndex) + date
    return url

def Date2Date(dateStr):
    """
    문자열 date를 2020년 1월 1일 부터의 날짜로 환산하여 반환한다.
    """
    month = int(dateStr[4:6])
    date = int(dateStr[6:8])
    if month == 1:
        date += 0
    elif month == 2:
        date += 31
    elif month == 3:
        date += 60
    elif month == 4:
        date += 91
    elif month == 5:
        date += 121
    elif month == 6:
        date += 152
    elif month == 7:
        date += 182
    elif month == 8:
        date += 213
    elif month == 9:
        date += 244
    elif month == 10:
        date += 274
    elif month == 11:
        date += 305
    elif month == 12:
        date += 335
    return date
    

def GetNextDate(str):
    """
    문자열날짜를 넣으면 다음 날짜를 내보낸다. 2020년 기준으로 작성
    >>> GetNextDate("20200101")
    20200102
    """
    year = int(str[0:4])
    month = int(str[4:6])
    date = int(str[6:8])
    
    date += 1
    
    if (month==2 and date==30):
        month += 1
        date = 1
    elif ((month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12) and date==32):
        month += 1
        date = 1
    elif ((month==4 or month==6 or month==9 or month==11) and date==31):
        month += 1
        date = 1
        
    return "{0:04d}".format(year) + "{0:02d}".format(month) + "{0:02d}".format(date)

def ProcessCoronaData(startDate, endDate, dataType):
    """
    dateRange : 20200121 ~ 20200613
    dateType : 0:confirmed, 1:death, 2:released, 3:candidate, 4:negative
    """
    x = []
    y = []
    fileDictionary = {}
    fileTemp = []

    # csv파일로 부터 데이터를 받는다.
    # 이때 날짜를 넣으면 데이터리스트를 받는 딕셔너리 형태로 만든다.
    with open("kr_daily.csv") as fileRead:
        for lineContent in fileRead:
            fileTemp = lineContent.strip('\n').split(',')
            fileDictionary[fileTemp[0]] = fileTemp[1:]

    # dataType에 맞는 그래프를 그린다.
    curDate = startDate
    while (curDate != endDate):
        x.append(Date2Date(curDate) - Date2Date("20200201"))
        y.append(int(fileDictionary[curDate][dataType]))

        curDate = GetNextDate(curDate)

    plt.plot(x, y)
    plt.title("Corona Confimed Case")
    plt.show()

    return


def ProcessCoronaDataDay(startDate, endDate, dataType):
    """
    dateRange : 20200121 ~ 20200613
    dateType : 0:confirmed, 1:death, 2:released, 3:candidate, 4:negative
    """
    before = 0
    x = []
    y = []
    fileDictionary = {}
    fileTemp = []

    # csv파일로 부터 데이터를 받는다.
    # 이때 날짜를 넣으면 데이터리스트를 받는 딕셔너리 형태로 만든다.
    with open("kr_daily.csv") as fileRead:
        for lineContent in fileRead:
            fileTemp = lineContent.strip('\n').split(',')
            fileDictionary[fileTemp[0]] = fileTemp[1:]

    # dataType에 맞는 그래프를 그린다.
    curDate = startDate
    while (curDate != endDate):
        x.append(Date2Date(curDate) - Date2Date("20200201"))
        y.append(int(fileDictionary[curDate][dataType]) - before)
        before = int(fileDictionary[curDate][dataType])
        curDate = GetNextDate(curDate)

    plt.plot(x, y)
    plt.title("Corona Confimed Case")
    plt.show()

    return


def ProcessAirQualityData(startDate, endDate, dataType):
    """
    공기 그래프를 그린다. 시작부터 끝까지
    dataType: 'no2', 'o3', 'co', 'so2', 'pm10', 'pm25'
    """
    sum = 0.0

    x = []
    y = []
    
    curDate = startDate
    while (curDate != endDate) :
        sum = 0.0

        #온라인으로 데이터를 받는다.
        url = GetSeoulUrl("DailyAverageAirQuality", 1, 40, curDate)

        print("Read :", url)
        
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        
        all_data = soup.find_all(dataType)

        # 데이터가 있을 경우 데이터를 더하고 없으면 건너뛴다.
        for data in all_data:
            if (data.text != ""):
                sum += float(data.text)
            else:
                continue

        # 40으로 나눠 평균값을 구하고 그래프에 추가한다.
        x.append(Date2Date(curDate) - Date2Date("20200201"))
        y.append(sum / 40)
        
        curDate = GetNextDate(curDate)

    plt.plot(x, y)
    plt.title("Seoul Qir Quality Data (" + dataType + ")")
    plt.show()

    return


def ProcessBus(startDate, endDate):
    """
    서울시 버스 탑승객의 날짜별 그래프를 그린다.
    데이터가 너무 많기 때문에 처음 100개 정류장만을 수집한다.
    """
    x = []
    y = []
    
    curDate = startDate
    while (curDate != endDate) :
        sum = 0

        #온라인으로 데이터를 받는다. 100개만
        url = GetSeoulUrl("CardBusStatisticsServiceNew", 1, 100, curDate)

        print("READ :", url)
            
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        all_data = soup.find_all('ride_pasgr_num')

        # 데이터가 있을 경우 데이터를 더하고 없으면 건너뛴다.
        for data in all_data:
            if (data.text != ""):
                sum += int(data.text)
            else:
                continue

        # 평균 데이터를 그래프에 추가한다.
        x.append(Date2Date(curDate) - Date2Date("20200201"))
        y.append(sum / 100)
        
        curDate = GetNextDate(curDate)

    plt.plot(x, y)
    plt.title("Seoul Bus Ride Passenger")
    plt.show()

    return

def ProcessSubway(startDate, endDate):
    """
    지하철 탑승객의 날짜별 그래프를 그린다.
    데이터가 너무 많기 때문에 처음 100개 데이터만을 수집한다.
    """
    x = []
    y = []
    
    curDate = startDate
    while (curDate != endDate) :
        sum = 0

        #온라인으로 데이터를 받는다. 100개만
        url = GetSeoulUrl("CardSubwayStatsNew", 1, 100, curDate)

        print("READ :", url)
            
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        all_data = soup.find_all('ride_pasgr_num')

        # 데이터가 있을 경우 데이터를 더하고 없으면 건너뛴다.
        for data in all_data:
            if (data.text != ""):
                sum += int(data.text)
            else:
                continue

        # 평균 데이터를 그래프에 추가한다.
        x.append(Date2Date(curDate) - Date2Date("20200201"))
        y.append(sum / 100)
        
        curDate = GetNextDate(curDate)

    plt.plot(x, y)
    plt.title("Seoul Subway Ride Passenger")
    plt.show()

    return
