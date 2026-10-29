Step 0: MRI.COM とは
========

**目標**: MRI.COM がどんなモデルか、どの資料に何が書いてあるかを把握する。

本チュートリアルの対象バージョンは **MRI.COM 5.4**。

**前提**: Linux のシェル操作、Fortran、海洋物理の基礎


MRI.COM の概要
--------

気象研究所共用海洋モデル（Meteorological Research Institute Community Ocean Model）。
自由表面・z* 鉛直座標・ブシネスク・静水圧近似の海洋海氷モデルで、
水平は一般直交座標上の Arakawa B 格子。MRI-ESM や気象庁の海洋予報システムに使われている。


資料
--------

| 資料 | 内容 | 使いどころ |
|---|---|---|
| [気象研究所技術報告 第87号「気象研究所共用海洋モデル第5版」](https://www.mri-jma.go.jp/Publish/Technical/DATA/VOL_87/index.html)（坂本ほか, 2023, [doi:10.11483/mritechrepo.87](https://doi.org/10.11483/mritechrepo.87)） | 公開マニュアル（MRI.COM v5.0 対応。5.4 から見ると少し古い）。支配方程式、格子、時間積分、各物理過程、結合（海氷・潮汐・生態系・ネスティング）、数値手法、利用者向け情報 | 物理・数値スキームの理解。namelist パラメータの物理的意味を調べるとき |
| [MRI.COM web page](https://mri-ocean.github.io/mricom/) | 概要、MRICOM-rect・MXE の案内、利用申請（申請書類・送付先） | 入口 |
| MRI.COMリポジトリ (以下、mricomと表記)の`README_First.md` | ディレクトリ構成、ビルド、入力データ、実行の概要 | Step 1〜3 |
| `mricom/docs/README_*.md` | Namelist, Options, Monitor, Restart, Surfflux など機能別の説明 | 設定を変えるとき。目的別の参照先は [../mricom-readme-map.md](../mricom-readme-map.md) |
| MRICOM-rect の `README.md`, `README-MXE.md` と各ディレクトリの README | MRICOM-rect・MXE の使い方 | Step 1〜4 |

資料どうしで記述が食い違うときは、**`mricom/docs/README_*.md` を最も正しいものとして優先する**。

* 技術報告第87号は MRI.COM v5.0 用なので、5.4 から見ると少し古い。
* `README_First.md` の冒頭にある版表記「version 4.3」は誤り（5.4 の README である）。


用語: MRI.COM / MXE / MRICOM-rect
--------

気象研究所が提供するリポジトリ。

```
|名前        | 内容 |
|MRI.COM     |モデル本体（ソース・README）|
|MXE         |「MRI.COM実験環境」。前処理(prep)・実行(exp)・後処理(postp)・解析(anl, anlpy)・lib |
|MRICOM-rect |矩形海テスト用パッケージ。MXE + MRI.COM 開発版（v5.5）+ 矩形海の実験設定 |
```

本リポジトリ（mricom_user_pack）は、これらとは別の坂本によるユーザー向けツール集
（Python による解析・描画 `anl/`、前処理 `prep/`）。


実行に使うツールと事前知識
--------

MRI.COM の実行に使う計算機のツール。どれも手順の中で使うので、何のためのものかを理解しておくこと。
インストールと動作確認は [Step 2](02-environment.md) で行う。

| ツール | MRI.COM での用途 | 必須か | 使うステップ |
|---|---|---|---|
| Fortran コンパイラ | モデル本体と MXE ツールのコンパイル | 必須 | 2〜 |
| MPI | 領域分割による並列計算 | 必須 | 2〜 |
| make | モデル・MXE ライブラリ・ツールのビルド | 必須 | 2〜 |
| シェル（sh/bash） | 実験の設定・実行スクリプト | 必須 | 2〜 |
| git | パッケージの取得、設定ファイルの変更確認・復元 | 必須（無ければ web からダウンロード） | 1〜 |
| netCDF | ヒストリーの netCDF 出力、Python での読み込み | 任意 | 3d〜 |
| Python（venv か conda） | 結果の解析・描画（本リポジトリの `anl/`） | 実行には不要 | 3b〜 |

### Fortran コンパイラ

MRI.COM と MXE は Fortran で書かれている。チュートリアルでは gfortran を使う。
コンパイラごとにオプションの書き方が違うので、スパコンや共用サーバーでは推奨設定を管理者に聞く。

* 入出力ファイルのバイト順（エンディアン）をコンパイルオプションで指定する
  （gfortran では `-fconvert=big-endian`）。入力データと合っていないと、エラーにならずに値が化けることがある。

参考:
* [Fortran 入門](https://www.nag-j.co.jp/fortran/)（日本NAG）— Fortran 90/95 の入門 Web テキスト。演習付き
* [書籍・Web ページ紹介](https://degawa.github.io/fortran-jp.org/knowledge/book_and_web.html)（fortran-jp.org）— モダン Fortran を学ぶための書籍・Web の一覧
* 書籍: 冨田博之・齋藤泰洋『Fortran90/95 プログラミング 改訂新版』培風館, 2011 — 例題形式の入門書

### MPI 並列

MRI.COM は計算領域を東西・南北に分割し、各領域を別のプロセスで同時に計算する（領域分割）。
プロセス間の通信に MPI ライブラリ（Open MPI など）を使う。

* コンパイルは MPI 用のラッパー（`mpif90`。中身は gfortran などに MPI ライブラリの指定を加えたもの）で行う。
* 実行は `mpirun -np 4 ./ogcm` のように、プロセス数を指定して起動する。
* MRI.COM では分割数をコンパイル時に `configure.in` の `NPARTX`, `NPARTY` で決める。
  `mpirun -np` のプロセス数は `NPARTX × NPARTY` と一致させる。
* OpenMP（1 プロセス内のスレッド並列）と組み合わせることもできるが、本チュートリアルでは MPI のみを使う。

参考:
* [東京大学情報基盤センター 講習会教育教材](https://www.cc.u-tokyo.ac.jp/events/lectures/materials/) — 並列処理の基礎、MPI プログラミングの基礎などの解説動画
* [東京大学情報基盤センター 講習会](https://www.cc.u-tokyo.ac.jp/events/lectures/) — 「お試しアカウント付き並列プログラミング講習会」の MPI 基礎編。スパコンを使った演習付き

### make

ソースファイルのコンパイル手順（依存関係・オプション）を `Makefile` に書いておき、`make` 1 回でビルドするツール。

* MRI.COM 本体: `./configure` で `configure.in` の設定（オプション、格子数、MPI 分割数、コンパイラ）から
  `Makefile` を作り、`make` でビルドする（`README_First.md` 3.2 節）。
* MXE: コンパイラの設定を `setting/macros.make` に書き、各ディレクトリの `Makefile` がそれを読む。
* 設定を変えたら再コンパイルが必要。MRI.COM ではオプションや格子数を変えるたびに作り直す。

参考 (コンパクトな入門サイトがあれば教えてください):
* [GNU make マニュアル](https://www.gnu.org/software/make/manual/make.html)（英語）— 第 2 章 "An Introduction to Makefiles" が入門
* 書籍: Robert Mecklenburg 著, 菊池彰 訳『GNU Make 第3版』オライリー・ジャパン, 2005 (少し分かりにくく詳しすぎるが)

### シェルスクリプト

MRICOM-rect・MXE の実験手順は sh/bash のスクリプト（`exp/run/*.sh` など）で書かれている。
変数・`if`・`for`・リダイレクト・ヒアドキュメント（`cat << END`）程度が読めればよい。
`configure.in` もシェルスクリプトとして読まれる。

参考:
* 書籍: 三宅英明・大角祐介『新しいLinuxの教科書 第2版』SBクリエイティブ, 2024 — シェルの基礎・コマンド操作からシェルスクリプトまで

### git

バージョン管理システム。MRI.COM, MXE, MRICOM-rect は GitHub のリポジトリとして配布される。

* 取得: `git clone`、バージョンの切り替え: `git checkout 5_4`（[Step 1](01-get.md)）
* 自分が変えた設定ファイルの確認・復元: `git status`, `git diff`, `git checkout -- <ファイル>`。
  実験で `configure.in` や namelist テンプレートを書き換えるので、元に戻す手段として使う。

参考:
* [サル先生のGit入門](https://git-tutorial.backlog.com/)（Backlog）— 図解の入門
* [Pro Git 日本語版](https://git-scm.com/book/ja/v2)（Git 公式サイト）— 定番の解説書。無料で全文が読める

### netCDF

自己記述的（変数名・単位・座標を含む）な科学データ用のファイル形式とライブラリ。

* MRI.COM のヒストリー（解析用出力）は、標準では GrADS 形式（バイナリ + 説明ファイル `.ctl`）。
  オプション `NETCDF` を加えると netCDF でも出力できる（[Step 3d](03-rectangle.md)）。
* そのためには Fortran 用の netCDF-Fortran ライブラリが必要（C 版だけでは足りない）。
* `ncdump -h` でファイルの中身（変数・次元・属性）を確認できる。

GrADS 形式だけで済ませるなら不要。`README_Options.md` で netCDF を使うのはヒストリー出力
（`NETCDF`, `NETCDF4PARALLEL` など）で、本チュートリアルの入力データ・リスタートファイルはバイナリ。

参考（定番の日本語資料は見当たらないので英語）:
* [Unidata netCDF](https://www.unidata.ucar.edu/software/netcdf/) — 開発元。データモデルの説明、ライブラリ・`ncdump` のマニュアル
* [NetCDF Overview](https://climatedataguide.ucar.edu/climate-data-tools-and-analysis/netcdf-overview)（NCAR Climate Data Guide）— 気候データ利用者向けの概要

### Python の venv か conda

解析・描画用。モデル実行には不要。本リポジトリの `anl/` のスクリプトは xarray, matplotlib などを使う。
venv（Python 標準）か conda で専用の環境を 1 つ作り、ライブラリをそこに入れる（システムの Python を汚さない）。
使う前に環境を有効にする（venv なら `source ~/venv/bin/activate`）のを忘れないこと。

参考:
* [Python チュートリアル](https://docs.python.org/ja/3/tutorial/)（Python 公式、日本語）— 12 章「仮想環境とパッケージ」が venv

### Docker（任意）

上のツール一式が入ったテスト環境（Debian + gfortran + Open MPI）を Docker で使うこともできる。
自分の計算機での環境構築に詰まったときの代替（[Step 2](02-environment.md) の「Docker を使う場合」）。

参考:
* [Docker ドキュメント日本語化プロジェクト](https://docs.docker.jp/)（有志による公式ドキュメントの翻訳。最新は [docs.docker.com](https://docs.docker.com/)）


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
```
doc/ 以下のドキュメントを読んで、MRI.COM 実行に必要なツール、ライブラリを教えて。
```
