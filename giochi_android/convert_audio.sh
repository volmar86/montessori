#!/usr/bin/env bash
# Wandelt alle .mp3 in <spielordner>/Music in .ogg um (Android und Web mögen .ogg lieber).
# Leerzeichen im Namen werden zu "_" ("bttf midi.mp3" -> "bttf_midi.ogg").
# Aufruf:  bash giochi_android/convert_audio.sh giochi_android/delorean_pygame
# Danach werden die .mp3 gelöscht, damit sie nicht in die APK / das Web-Paket kommen.
# NUR im Build-Runner von GitHub aufrufen, nicht auf dem eigenen Rechner (sonst sind die .mp3 weg)!
set -euo pipefail

ordner="${1:?Spielordner angeben, z.B. giochi_android/delorean_pygame}/Music"

shopt -s nullglob
for mp3 in "$ordner"/*.mp3; do
    name="$(basename "$mp3" .mp3)"
    ogg="$ordner/${name// /_}.ogg"
    echo "-> $mp3  =>  $ogg"
    ffmpeg -y -loglevel error -i "$mp3" -c:a libvorbis -q:a 2 "$ogg"
    rm "$mp3"
done
ls -la "$ordner"
