# mricom_user_pack

気象研海洋モデルMRI.COMのユーザー向けツール集（前処理 `prep/`、解析・描画 `anl/`、ライブラリ `lib/`）。
MRI.COM実験（設定・namelist・入力データ・実行・解析）を手伝うときは、まず `doc/README.md` を読むこと。

## 情報源のルール（厳守）

- MRI.COMモデル本体のソースコードは参照禁止。読んでよいのは README 類のみ:
  `<MRICOM>/README_First.md`, `<MRICOM>/docs/README_*.md`（MRICOM-rect 同梱の `exp/MRICOM/` も同様）。
  `src/`, `samples/`, `tools/`, `ChangeLog*` などは Read でも Bash（cat, grep 等）でも読まない。
- 公開マニュアルは参照してよい: 気象研究所技術報告第87号「気象研究所共用海洋モデル第5版」（v5.0 対応）
  https://www.mri-jma.go.jp/Publish/Technical/DATA/VOL_87/index.html
- 資料が食い違うときは `docs/README_*.md` を優先する（技術報告は v5.0 用で少し古い。`README_First.md` 冒頭の「version 4.3」は誤り）。
- MRICOM-rect（矩形海パッケージ）の本体以外（`exp/run/` のスクリプト、`run.conf`、namelistテンプレート、
  `nml_monitor/`, `option/`）は参照してよい。`exp/src*/`, `exp/modsrc/` は本体ソースなので不可。
- README に書かれていないこと（既定値など）は推測で埋めず、「README に記載なし」と明示する。

## 各自の環境

doc では展開先を `~/mricom`, `~/mxe`, `~/rect`（MRICOM-rect）、`~/myrect`（Step 4 で MXE から作る自分の実験パッケージ）と書く（`doc/tutorial/01-get.md`）。
実際の場所はユーザーごとに異なるので、`CLAUDE.local.md` に書かれていればそれに読み替える。
書かれていなければ推測せずユーザーに聞き、`CLAUDE.local.md` への記入を提案する。

## ドキュメント集 `doc/`

MRI.COM 習熟のためのチュートリアル（`doc/tutorial/`, Step 0〜5）とリファレンス。

- `doc/README.md` — 目次と AI への頼み方
- `doc/tutorial/` — 00 概要・マニュアル, 01 取得, 02 実行環境, 03 rectangle 実行, 04 MXE で矩形海を自作, 05 独自モデル
- `doc/tutorial/rect_workflow.md` — MRICOM-rect の実験手順（exp/run/、Step 3 の詳細版）
- `doc/mricom-readme-map.md` — 目的別の README 参照先
- `doc/input-data.md` — 入力データの形式・単位
- `doc/namelist-reference.md` — namelist の解説
- `doc/sample_ogcm/` — MRI.COM の設定例: configure.in のビルド設定（Step 2 から参照）、モデル設定の雛形と namelist の実例（Step 4 から参照）
- `doc/sample_mxe/` — MXE の設定例: macros.make（Step 2 から参照）
- `doc/manual/` — 公開マニュアル（技術報告第87号）PDF の取得スクリプト `get_manual.sh`（Step 1）。取得済みなら `tech_rep_mri-v5.pdf` を読んでよい
- `doc/fortran/` — 環境確認用 Fortran テストプログラム（netCDF の nctest.f90。Step 2 から参照）

新しい知見（落とし穴、確認できた TODO など）が得られたら、該当する doc ファイルへの追記を提案すること。

## コード

- Python スクリプトは `lib/mricom.py` の `open_history()` / `open_grads()` で MRI.COM 出力を xarray として読む。
- データは `link/data`（シンボリックリンク）経由でアクセスする。
- 各 `anl/<対象>/` に README.md があり、スクリプトを追加したら一覧に追記する。
