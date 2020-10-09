import json
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import requests
import slackweb

#SlackのIncomming webhookの設定に進み, URLをコピーする
webhook_url=""

#OpenWeatherMapにアクセスし, アカウントを作ってAPIキーを取得しコピーする
API_KEY=""

#ここ↓から予報を送信してほしい都市を選択し, そのidを入力する
#http://bulk.openweathermap.org/sample/city.list.json.gz
city_id="2110681"#Tsukuba

#日本語化するときに使う
#OpenWeatherMapに使われる予報用語はここから確認できる↓
#https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
weather_to_ja={
    "Thunderstorm":"雷雨",
    "Drizzle":"霧雨",
    "Rain":"雨",
    "Snow":"雪",
    "Mist":"もや",
    "Smoke":"煙っている",
    "Haze":"煙霧",
    "sand/ dust whirls":"砂塵旋風",
    "Fog":"霧",
    "Sand":"砂",
    "dust":"塵",
    "Ash":"火山灰",
    "Squall":"スコール",
    "Tornado":"トルネード",
    "Clear":"快晴"
}

def weather_to_ja_forecast(index,L):
    if L[index]["weather"][0]["main"]=="Clouds":
        cloudiness=L[index]["clouds"]["all"]
        if cloudiness<20:
            return "快晴"
        elif cloudiness<=80:
            return "晴れ"
        else:
            return "曇"
    elif L[index]["weather"][0]["main"]=="Dust":
        return weather_to_ja[L[index]["weather"][0]["description"]]
    elif L[index]["weather"][0]["main"] in weather_to_ja:
        return weather_to_ja[L[index]["weather"][0]["main"]]
    else:
        return L[index]["weather"][0]["main"]

def current_weather():
    #current weather
    api="http://api.openweathermap.org/data/2.5/weather?units=metric&id={city_id}&APPID={key}"

    url=api.format(city_id=city_id,key=API_KEY)
    response=requests.get(url)
    data=response.json()

    #アイコンの設定
    icon_url="http://openweathermap.org/img/wn/{icon_id}@2x.png"
    icon_url=icon_url.format(icon_id=data["weather"][0]["icon"])

    #送信するメッセージの作成
    message=str(datetime.fromtimestamp(data["dt"]))+"\n\ncurrent weather\n"
    message+="weather: "+data["weather"][0]["description"]+"\n"
    message+="temp: "+str(data["main"]["temp"])+"℃\n"
    message+="humidity: "+str(data["main"]["humidity"])+"%\n"
    message+="wind: "+str(data["wind"]["speed"])+"m/s, "+str(data["wind"]["deg"])+"deg"

    return icon_url,message

def weather_forecast():
    #5day weather forecast
    api="http://api.openweathermap.org/data/2.5/forecast?id={city_id}&appid={key}"

    url=api.format(city_id=city_id,key=API_KEY)
    response=requests.get(url)
    data=response.json()

    L=data["list"]
    message=""

    for i in range(4):
        #時間を取得
        time=datetime.fromtimestamp(L[i]["dt"])
        #天気(概況)を取得&日本語化する
        #weather=L[i]["weather"][0]["main"]
        weather=weather_to_ja_forecast(i,L)

        #気温を取得
        temp=L[i]["main"]["temp"]-273.15
        temp=str(Decimal(str(temp)).quantize(Decimal("0.1"),rounding=ROUND_HALF_UP))+"℃"
        
        #メッセージを作成
        message+=str(time.hour)+":00 天気: "+weather+", 気温: "+str(temp)

        #降水量があったらそれを追記
        if "rain" in L[i]:
            if "3h" in L[i]["rain"]:
                message+=", 降水量: "+str(Decimal(str(L[i]["rain"]["3h"]/3)).quantize(Decimal("0.1"),rounding=ROUND_HALF_UP))+"mm"

        if i!=3:
            message+="\n"

    return message

if __name__ == "__main__":
    #アイコンの取得&送信メッセージの作成
    icon_url,message=current_weather()

    #0時, 4時, 8時, 12時, 16時, 20時なら予報も送信
    #予報の送信間隔を変えたい場合はここのif文を書き換える
    #例えば3時間ごとに変えたい場合はdatetime.now().hour%3==0とする
    if datetime.now().hour%4==0:
        message+="\n\n予報\n"
        message+=weather_forecast()
        usename="Weather forecast"
    else:
        username="Current Weather information"

    #Slackに投稿する
    slack=slackweb.Slack(url=webhook_url)
    
    #このままだと#generalに投稿される
    #投稿するチャンネルを例えば#randomにしたいときには次のように書く
    #slack.notify(text=message,channel="#random",username=username,icon_url=icon_url)
    slack.notify(text=message,username=username,icon_url=icon_url)