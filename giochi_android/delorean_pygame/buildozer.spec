[app]
title = DeLorean 88
package.name = delorean88
package.domain = org.volmar86

source.dir = .
# nur diese Dateitypen kommen in die APK (die .mp3 werden vor dem Build in .ogg umgewandelt)
source.include_exts = py,ogg,ttf
source.exclude_dirs = build, bin, .buildozer

version = 1.0
requirements = python3,pygame

orientation = landscape
fullscreen = 1

android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.accept_sdk_license = True

# Feste, zusammenpassende Versionen. Die neueste python-for-android ("master") baut Python 3.14, und dazu passt
# das alte pygame 2.1.0 nicht ("longintrepr.h file not found"). Die Version v2024.01.21 nutzt Python 3.11.
p4a.branch = v2024.01.21
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
