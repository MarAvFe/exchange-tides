#!/usr/bin/env bash
# Build Exchange Tides for Linux with gm-cli and run the automated self-test headlessly (Xvfb).
# Needs: node/npx, Xvfb, and the runner's shared libraries. Without root, unpack them locally:
#   apt-get download libglu1-mesa libopenal1 libpulse0 libsndio7.0 libsndfile1 libasyncns0 libflac14 \
#     libogg0 libvorbis0a libvorbisenc2 libopus0 libmpg123-0t64 libmp3lame0
#   curl -O http://archive.ubuntu.com/ubuntu/pool/main/o/openssl1.0/libssl1.0.0_1.0.2n-1ubuntu5_amd64.deb
#   for d in *.deb; do dpkg-deb -x "$d" "$LIBROOT"; done
# gm-cli's packaging step needs `unzip` and `linuxdeploy`; provide an unzip shim on PATH (UNZIP_SHIM_DIR).
# The linuxdeploy failure is expected: the runner is already installed into ~/GameMakerStudio2/vm/ by then.
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
LIBROOT=${LIBROOT:?set LIBROOT to the folder the .debs were extracted into}
WORK=${WORK:-/tmp/et-selftest}
mkdir -p "$WORK"
# Register every script/sound/datafile folder first: a script missing from the .yyp compiles but its
# functions are silently unavailable at runtime.
python3 -I "$ROOT/tools/gen_project.py" > /dev/null
cd "$WORK"
PATH=${UNZIP_SHIM_DIR:-$WORK/bin}:$PATH npx --yes @gamemaker/gm-cli@latest run "$ROOT/game/ExchangeTides/ExchangeTides.yyp" \
  --target=linux --runtime=vm > build.log 2>&1
grep -q 'Compilation finished\|Transferring Assets' build.log || { echo "build failed, see $WORK/build.log"; exit 1; }
pgrep -f 'Xvfb :99' >/dev/null || (Xvfb :99 -screen 0 1280x800x24 >/dev/null 2>&1 &)
sleep 1
LIB=$LIBROOT/usr/lib/x86_64-linux-gnu:$LIBROOT/usr/lib/x86_64-linux-gnu/pulseaudio
cd ~/GameMakerStudio2/vm/ExchangeTides/AppDir/usr/bin
LD_LIBRARY_PATH=$LIB DISPLAY=:99 WAYLAND_DISPLAY= ET_SELFTEST=1 timeout 300 ./ExchangeTides > "$WORK/run.log" 2>&1
grep -E '\[SELFTEST\]|ERROR|############' "$WORK/run.log"
echo "screenshots: ~/.config/ExchangeTides/shot_*.png"
grep -q 'done, fails=0' "$WORK/run.log"
