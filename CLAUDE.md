# mricom_user_pack

気象研海洋モデルMRI.COMのユーザー向けツール集（前処理 `prep/`、解析・描画 `anl/`、ライブラリ `lib/`）。
MRI.COM実験（設定・namelist・入力データ・実行・解析）を手伝うときは、まず `doc/README.md` を読むこと。

## 情報源のルール（厳守）

- MRI.COMモデル本体のソースコードは参照禁止。読んでよいのは README 類のみ:
  `~/mricom/README_First.md`, `~/mricom/docs/README_*.md`（MRICOM-rect 同梱の `exp/MRICOM/` も同様）。
  `src/`, `samples/`, `tools/`, `ChangeLog*` などは Read でも Bash（cat, grep 等）でも読まない。
- 公開マニュアルは参照してよい: 気象研究所技術報告第87号「気象研究所共用海洋モデル第5版」
  https://www.mri-jma.go.jp/Publish/Technical/DATA/VOL_87/index.html
- MRICOM-rect（矩形海パッケージ。このマシンでは `~/myrect`）の本体以外（`exp/run/` のスクリプト、`run.conf`、namelistテンプレート、
  `nml_monitor/`, `option/`）は参照してよい。`exp/src*/`, `exp/modsrc/` は本体ソースなので不可。
- README に書かれていないこと（既定値など）は推測で埋めず、「README に記載なし」と明示する。

## ドキュメント集 `doc/`

MRI.COM 習熟のためのチュートリアル（`doc/tutorial/`, Step 0〜5）とリファレンス。

- `doc/README.md` — 目次と AI への頼み方
- `doc/tutorial/` — 00 概要・マニュアル, 01 取得, 02 実行環境, 03 rectangle 実行, 04 MXE で矩形海を自作, 05 独自モデル
- `doc/workflow.md` — 実験手順（MRICOM-rect の exp/run/）
- `doc/mricom-readme-map.md` — 目的別の README 参照先
- `doc/input-data.md` — 入力データの形式・単位
- `doc/namelist-reference.md`, `doc/namelist-examples/` — namelist の解説・実例

新しい知見（落とし穴、確認できた TODO など）が得られたら、該当する doc ファイルへの追記を提案すること。

## コード

- Python スクリプトは `lib/mricom.py` の `open_history()` / `open_grads()` で MRI.COM 出力を xarray として読む。
- データは `link/data`（シンボリックリンク）経由でアクセスする。
- 各 `anl/<対象>/` に README.md があり、スクリプトを追加したら一覧に追記する。
