RPIセットアップ
===

## SDカードにOSイメージを書き込む

Raspberry Pi Imager v1.7.1  
Raspberry Pi OS Full (32-bit) Released: 2022-01-28

SSH設定をしておく

## RaspberryPi OSのバージョン確認

```sh
$ lsb_release -a
No LSB modules are available.
Distributor ID:	Raspbian
Description:	Raspbian GNU/Linux 11 (bullseye)
Release:	11
Codename:	bullseye
```

## Raspberry Piライブラリ更新・追加

```sh
$ sudo apt update
$ sudo apt full-upgrade -y
$ sudo apt install -y tigervnc-standalone-server i2c-tools vim redis-server
```

## eth0を固定IPにする

```sh
$ sudo vim /etc/dhcpcd.conf
# 一番下に追記
interface eth0
static ip_address=192.168.0.10/24
```

## Macから画面共有できるようにする

```sh
$ tigervncpasswd
# 画面共有のパスワードを決める
password: raspberry

# 起動コマンド
$ tigervncserver -localhost no
```

## I2C有効化、パスワード・ホスト名変更、ファイルシステム拡張をする

```sh
$ sudo raspi-config
3 Interface Options
  I5 I2C
    <Yes>
  I6 Serial Port
    Would you like a login shell to be accessible over serial? <No>
    Would you like the serial port hardware to be enabled? <Yes>
1 System Options
  S3 Password
    iot
  S4 Hostname
    iotbox
6 Advanced Options
  A1 Expand Filesystem
```

設定後、再起動される

## Pythonのライブラリをインストールする

```sh
$ pip install pyserial SIP PyQt5 yapf redis
```

## 画面スリープを無効にする

```sh
$ sudo vim /etc/xdg/lxsession/LXDE/autostart
# 以下追記
# スクリーンセーバーをオフ
@xset s off
# X serverをオフ
@xset s noblank
# DPMS (Display Power Management Signaling) をオフ
@xset -dpms
$ sudo vim /etc/lightdm/lightdm.conf
# 以下追記
[SeatDefaults]
xserver-command=X -s 0 -dpms
```

## デスクトップ背景を単色（グレー）にする

* ラズパイにマウスをつなぐ
* 右クリック
* デスクトップの設定
* 以下を設定する
  * レイアウト：画像なし
  * 色：グレー
  * 文字色：黒
* OK 


## python自動起動設定

画面スクリプト

```sh
$ sudo vim ~/.config/lxsession/LXDE-pi/autostart
# 追記
@python /home/pi/iot/gui.py
```

メインスクリプト

```sh
$ sudo bash install.sh
```
