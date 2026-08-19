#!/bin/bash
#- NOAAサイトから WOA 硝酸塩気候値データをダウンロードする

set -e

for year in `seq 2001 2019`; do
for mon in `seq -w 1 12` ; do
    wget2 "https://www.jamstec.go.jp/jagdas/fileServer/fora/NP/Monthly-mean/Basic-2D/${year}/nc_ssh.${year}${mon}"
done
done

exit 0
