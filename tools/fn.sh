#!/bin/sh
# usage: fn.sh NAME...  -> print decompiled function(s) from re/decomp.c
for n in "$@"; do awk -v n="$n" '/^\/\/ ==== /{p=($3==n)} p' /home/mavila/exchange-tides/re/decomp.c; done
