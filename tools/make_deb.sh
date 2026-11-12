#!/usr/bin/env bash
# Wraps a Linux build of Exchange Tides into a .deb.
#
# Usage: tools/make_deb.sh PACKAGE.zip VERSION OUT.deb LIBROOT
#   PACKAGE  the zip from `gm-cli package --target=linux --runtime=vm -o PACKAGE.zip` (needs `zip` on PATH)
#   VERSION  package version, e.g. 1.0.0
#   LIBROOT  folder with the extracted libssl1.0.0 .deb (the GameMaker runner links against OpenSSL 1.0,
#            which current distributions no longer ship; it is bundled privately in /opt/exchange-tides/lib)
#
# Installs to /opt/exchange-tides, a launcher in /usr/games/exchange-tides and a menu entry.
# Saves and settings live in ~/.config/ExchangeTides.
set -euo pipefail
PKG=$1; VERSION=$2; OUT=$3; LIBROOT=$4
STAGE=$(mktemp -d)
chmod 755 "$STAGE"
trap 'rm -rf "$STAGE"' EXIT

mkdir -p "$STAGE/DEBIAN" "$STAGE/opt/exchange-tides/lib" "$STAGE/usr/games" \
	"$STAGE/usr/share/applications" "$STAGE/usr/share/icons/hicolor/64x64/apps" "$STAGE/usr/share/doc/exchange-tides"

python3 -I -c 'import sys, zipfile; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])' "$PKG" "$STAGE/opt/exchange-tides"
chmod -R u=rwX,go=rX "$STAGE/opt/exchange-tides"
rm -f "$STAGE/opt/exchange-tides/assets/game.yydebug"
for l in libssl.so.1.0.0 libcrypto.so.1.0.0; do
	cp "$LIBROOT/usr/lib/x86_64-linux-gnu/$l" "$STAGE/opt/exchange-tides/lib/"
done
cp "$STAGE/opt/exchange-tides/assets/icon.png" "$STAGE/usr/share/icons/hicolor/64x64/apps/exchange-tides.png"

cat > "$STAGE/usr/games/exchange-tides" <<'SH'
#!/bin/sh
# Exchange Tides launcher: the runner looks for its assets next to itself.
cd /opt/exchange-tides || exit 1
LD_LIBRARY_PATH=/opt/exchange-tides/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH} exec ./ExchangeTides "$@"
SH
chmod 755 "$STAGE/usr/games/exchange-tides" "$STAGE/opt/exchange-tides/ExchangeTides"

cat > "$STAGE/usr/share/applications/exchange-tides.desktop" <<DESK
[Desktop Entry]
Type=Application
Name=Exchange Tides
Comment=A pirate-era trading game
Exec=/usr/games/exchange-tides
Icon=exchange-tides
Terminal=false
Categories=Game;StrategyGame;
DESK

cat > "$STAGE/usr/share/doc/exchange-tides/copyright" <<'TXT'
Exchange Tides - https://github.com/MarAvFe/exchange-tides
Music: Kevin MacLeod (incompetech.com), Creative Commons Attribution 4.0
Fonts: Alegreya and Pirata One, SIL Open Font License 1.1
Bundled: OpenSSL 1.0.2 libraries (OpenSSL License / SSLeay License), needed by the GameMaker runner.
Built with GameMaker.
TXT

SIZE=$(du -sk "$STAGE" | cut -f1)
cat > "$STAGE/DEBIAN/control" <<CTRL
Package: exchange-tides
Version: $VERSION
Section: games
Priority: optional
Architecture: amd64
Depends: libc6, libglu1-mesa, libopenal1, libpulse0
Installed-Size: $SIZE
Maintainer: MarAvFe <MarAvFe@users.noreply.github.com>
Homepage: https://github.com/MarAvFe/exchange-tides
Description: Exchange Tides, a pirate-era trading game
 Trade goods between Caribbean-style ports, take governors' contracts, build a
 fleet of up to five ships and fight real-time sea battles. Campaign and free
 trade modes, Spanish and English.
CTRL

dpkg-deb --root-owner-group --build "$STAGE" "$OUT" >/dev/null
echo "built $OUT ($(du -h "$OUT" | cut -f1))"
