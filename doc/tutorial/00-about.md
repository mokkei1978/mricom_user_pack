Step 0: MRI.COM とは
========

**目標**: MRI.COM がどんなモデルか、どの資料に何が書いてあるかを把握する。

本チュートリアルの対象バージョンは **MRI.COM 5.4**。

**前提**: なし。Linux のシェル操作、Fortran の読み書き、海洋物理の基礎（プリミティブ方程式、
B格子、split-explicit 法などの用語）を知っていると以降が楽になる。


MRI.COM の概要
--------

気象研究所共用海洋モデル（Meteorological Research Institute Community Ocean Model）。
自由表面・z* 鉛直座標・ブシネスク・静水圧近似の海洋海氷モデルで、
水平は一般直交座標上の Arakawa B 格子。MRI-ESM や気象庁の海洋予報システムに使われている。
（`~/mricom/README_First.md` Sec.1 より）


資料
--------

| 資料 | 内容 | 使いどころ |
|---|---|---|
| [気象研究所技術報告 第87号「気象研究所共用海洋モデル第5版」](https://www.mri-jma.go.jp/Publish/Technical/DATA/VOL_87/index.html)（坂本ほか, 2023, [doi:10.11483/mritechrepo.87](https://doi.org/10.11483/mritechrepo.87)） | 公開マニュアル（MRI.COM 第5版）。支配方程式、格子、時間積分、各物理過程、結合（海氷・潮汐・生態系・ネスティング）、数値手法、利用者向け情報 | 物理・数値スキームの理解。namelist パラメータの物理的意味を調べるとき |
| [MRI.COM web page](https://mri-ocean.github.io/mricom/) | 概要、MRICOM-rect・MXE の案内、利用申請 <!-- TODO: 要確認 --> | 入口 |
| `~/mricom/README_First.md` | ディレクトリ構成、ビルド、入力データ、実行の概要 | Step 1〜3 |
| `~/mricom/docs/README_*.md` | Namelist, Options, Monitor, Restart, Surfflux など機能別の説明 | 設定を変えるとき。目的別の参照先は [../mricom-readme-map.md](../mricom-readme-map.md) |
| MRICOM-rect の `README.md`, `README-MXE.md` と各ディレクトリの README | MRICOM-rect・MXE の使い方 | Step 1〜4 |

<!-- TODO: 要確認。README_First.md の冒頭は「version 4.3 (February 2017)」となっており、
     技術報告（第5版）・対象の 5.4 より古い記述が残っている可能性がある。食い違ったときにどちらを優先するか -->


用語: MRI.COM / MXE / MRICOM-rect
--------

```
MRI.COM    モデル本体（ソース・README）
  ↑ 実行・前処理・解析のツールで包む
MXE        MRI.COM eXecution Environment。前処理(prep)・実行(exp)・後処理(postp)・解析(anl, anlpy)・lib
  ↑ 矩形海に必要な最小限を切り出し、MRI.COM 開発版を同梱
MRICOM-rect 矩形海テスト用パッケージ。MXE と同じディレクトリ構成
```

本リポジトリ（mricom_user_pack）は、これらとは別のユーザー向けツール集
（Python による解析・描画 `anl/`、前処理 `prep/`）。


AI に手伝わせるときの約束
--------

AI が参照してよいのは README 類と公開マニュアルだけで、モデル本体のソースは読ませない
（[../README.md](../README.md) の「情報源のルール」）。


AIへの頼み方（例）
--------

```
doc/tutorial/00-about.md を読んで、MRI.COM の鉛直座標 z* とは何か、
技術報告第87号のどの章を読めばよいか教えて。
```
