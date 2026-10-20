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

[buildozer]
log_level = 2
warn_on_root = 1
