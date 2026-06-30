[app]
title = GestorMasterS
package.name = gestormasters
package.domain = org.master.s
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 34
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
orientation = portrait

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
source.include_exts = py,png,jpg,kv,atlas,db
source.include_patterns = BaseDeDatos/**,ModelosIA/**,Respaldos/**
