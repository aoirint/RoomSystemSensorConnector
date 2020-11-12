# RoomSystemSensorConnector

## 想定環境
- Raspberry Pi 4B
  - Raspberry Pi OS Lite
  - オーディオジャック→アンプ→スピーカ

### 注意
PulseAudioを使うため、コンテナ作成時にホスト側ユーザのUID・GIDが必要です。
これは、`docker-compose`コマンドの代わりに`./compose.sh`を使うことで`id`コマンドから自動設定されます。

また、コンテナ作成時のユーザでPulseAudioデーモンが起動している必要があります。

Raspberry Pi OS Liteなど、デスクトップ環境のないOSを使用している場合、デフォルトで
PulseAudioがインストールされていないことが考えられます。
`sudo apt install pulseaudio`などでインストールしておいてください。

また、PulseAudioデーモンがOS起動時に起動しない場合があります。
一般ユーザ権限でsystemdを使ってサービスを起動するには、
`systemctl --user`を使いますが、これが実行できない（`Failed to connect to bus: No such file or directory`など）可能性があります。
これは、`sudo loginctl enable-linger $USER`を実行して再起動することで解消する場合があります。
その後、`systemctl --user`が実行できることを確認し、
`mkdir -p ~/.config/systemd/user`します。
そして、以下のGistの手順通りにホスト上にPulseAudioの起動設定をします。

- [Pulseaudio via systemd --user | Gist by @kafene](https://gist.github.com/kafene/32a07cac0373409e31f5bfe981eefb19)

~/.config/systemd/user/pulseaudio.service
```
[Unit]
Description=Pulseaudio Sound Service
Requires=pulseaudio.socket

[Service]
Type=notify
ExecStart=/usr/bin/pulseaudio --verbose --daemonize=no
ExecStartPost=/usr/bin/pactl load-module module-alsa-sink
Restart=on-failure

[Install]
Also=pulseaudio.socket
WantedBy=default.target
```

~/.config/systemd/user/pulseaudio.socket
```
[Unit]
Description=Pulseaudio Sound System

[Socket]
Priority=6
Backlog=5
ListenStream=%t/pulse/native

[Install]
WantedBy=sockets.target
```

```bash
pulseaudio --kill
systemctl --user daemon-reload
systemctl --user enable pulseaudio.service
systemctl --user enable pulseaudio.socket
systemctl --user start pulseaudio.service
```


## 機能
[aoirint/RoomSystemSensorArduino](https://github.com/aoirint/RoomSystemSensorArduino)と組み合わせて使うことを想定しています。

シリアル通信を受け取ってFirebase Realtime Database、Teamsにセンサ情報を流します。

## 設定
Now Button、Wait Buttonが押されたときの効果音2種が必要です。
それぞれ、`./sounds/now_button.mp3`、`./sounds/wait_button.mp3`に配置してください。

## 起動
```bash
./compose.sh up -d
```

## ログ
```bash
./compose.sh logs -f
```
