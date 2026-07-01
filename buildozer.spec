
[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.scropio
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json,ttf
version = 0.1
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.3.0
fullscreen = 0
android.permissions = INTERNET
android.api = 31
android.build_tools_version = 34.0.0
android.minapi = 21
android.sdk = 31
android.ndk = 21e
android.archs = arm64-v8a
android.accept_sdk_license = True
android.private_storage = True
android.allow_backup = False
p4a.branch = develop
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r21e
android.clean_build = True

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
