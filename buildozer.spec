[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.scorpiomaster
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,ttf,db
version = 0.1
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,sqlite3
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

[app:android]
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
