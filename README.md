# RoomSystemSensorConnector

## 想定環境
- Raspberry Pi 4B
  - オーディオジャック→アンプ→スピーカ

## 機能
[aoirint/RoomSystemSensorArduino](https://github.com/aoirint/RoomSystemSensorArduino)と組み合わせて使うことを想定しています。

シリアル通信を受け取ってFirebase Realtime Database、Teamsにセンサ情報を流します。

## 設定
Now Button、Wait Buttonが押されたときの効果音2種が必要です。
それぞれ、`./sounds/now_button.mp3`、`./sounds/wait_button.mp3`に配置してください。

## 起動
```bash
docker-compose up -d
```

## ログ
```bash
docker-compose logs -f
```
