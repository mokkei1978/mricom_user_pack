#!/bin/sh
# 公開マニュアル（気象研究所技術報告第87号「気象研究所共用海洋モデル第5版」, MRI.COM v5.0）を取得する。
#   使い方: sh get_manual.sh    （このスクリプトと同じディレクトリに保存される）
set -e

url=https://www.mri-jma.go.jp/Publish/Technical/DATA/VOL_87/tech_rep_mri-v5.pdf
dir=$(cd "$(dirname "$0")" && pwd)

wget -N -P "${dir}" "${url}"
ls -l "${dir}/tech_rep_mri-v5.pdf"
