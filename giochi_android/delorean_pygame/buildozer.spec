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

# Feste, zusammenpassende Versionen. Das Android-pygame in python-for-android ist 2.1.0 (von 2021) und passt nur
# zu Python 3.9: bei neueren Versionen kommt "longintrepr.h file not found" (master = Python 3.14,
# v2024.01.21 = Python 3.11 mit falschem Header-Pfad "python3.1"). Die Version v2022.12.20 nutzt Python 3.9.9
# und verlangt genau den NDK 25b.
p4a.branch = v2022.12.20
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
