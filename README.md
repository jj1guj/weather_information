# weather_information
Slackに1時間おきに現在の気象情報や気象予報を投稿するボット  
毎時0分に現在の気象情報が, 0時から4時間おきにこれに加え3時間おきの気象予報が投稿されます. 
実際に投稿されている様子は[こちら](https://twitter.com/jj1guj/status/1312793663160815617?s=20)
# 動作環境
- UNIX系OS(raspbianでの動作を確認済)
- Python3(Python3.7での動作を確認済)
# 使用ライブラリ
- json
- datetime
- decimal
- requests
- slackweb
# 使い方
1. 以下のコマンドを実行しslackwebをインストールする(pip3が入っていない場合は先にインストールすること)  
```
pip3 install slackweb
```
2. このボットを使用したいSlackのワークスペースでIncomming webhookを使えるようにし, そのURLをコピーしてソースコードの8行目にペーストする.  
3. [OpenWeatherMap](https://openweathermap.org/)にアクセスし, アカウントを作成し, APIキーをコピーしてソースコードの11行目にペーストする.  
4. [このページ](http://bulk.openweathermap.org/sample/)からcity.list.json.gzをダウンロードして解凍し, 予報を送信してほしい都市のcity_idをコピーしてソースコードの15行目にペーストする.  (デフォルトではつくば市つくば駅付近になっている)
5. 投稿するチャンネルを#generalから別のチャンネルに変えたい場合はソースコードの130行目を書き換える(デフォルトだと#generalに投稿される)  
6. 以下のコマンドを実行し, cronの編集を行う.  
```
crontab -e
```
7. これで編集画面がひらくので以下を入力し保存する.  
```
0 * * * * python [ソースコードのフルパス]
```
