Step 2: 実行環境の構築と確認
========

**目標**: Fortran コンパイラ・MPI・ライブラリが MRI.COM / MXE の要求どおりに動くことを確かめる。

**前提**: [Step 1](01-get.md) で MRICOM-rect を取得済み。


確認するもの
--------

| 項目 | 確認方法 |
|---|---|
| Fortran コンパイラ、推奨オプション等 | サーバー管理者に聞く。例えば `gfortran --version`で確認する |
| MPI並列コンパイル、実行方法 | 管理者に聞く。例えば `mpif90 --version`, `mpirun --version` で確認する |
| Fortran で netCDFライブラリを使う方法（任意） | Fortranコンパイル時のオプション。 `nf-config`で確認できる |
| Python 解析環境 (モデル実行には不要) | 各自の環境で下記「Python 解析環境」のライブラリをインストールする |


MRI.COM-rectの環境設定
--------

Step 3 で矩形海パッケージを実行するための事前準備。`~/rect/`で作業する。

### 実験入力・出力ディレクトリ

```
cd linkdir/
sh link.sh
```
表示を参考に以下のリンクを設定する。
* data   - 取得した rectangle_data へのシンボリック・リンク (入力データ)
* result - 実験出力を書き出すディレクトリへのリンク

### MXE ツール用ビルド設定

Fortran で作られたツールをコンパイルするのに必要な設定ファイル。makeで参照される。
```
cd setting/
sh make_macros.make.sh
```

上記のシェル・スクリプトを実行すると `setting/macros.make` が作られる。Fortranコンパイル設定を記載する。
詳細は `setting/README-MXE.md`, サンプルは `setting/machine/`を参照する。

* netCDF が使える場合は FFLAGS に -DMXE_NETCDF を加える。

<!-- TODO: macros.make の解説付きサンプルをこのリポジトリに加える -->

### MXE ライブラリ

`setting/macros.make`が設定できれば、MXEライブラリをビルドする。
```
cd lib/
make
```

### モデル用ビルド設定

`exp/config_files/configure.in` にMPI並列Fortranコンパイル設定を記述する。

<!-- TODO: gfortran + MPI の解説付きサンプルを加える -->


Python 解析環境
--------

本リポジトリ `mricom_user_pack` のスクリプト用。venv や conda で 1 つ環境を作っておく。

| ライブラリ | 用途 | 動作実績 |
|---|---|---|
| numpy | 配列計算 | 2.3.5 |
| xarray | データを Dataset として扱う（`lib/mricom.py`） | 2025.12.0 |
| dask | `xarray.open_mfdataset()`（`open_history()`）に必要 | 2025.11.0 |
| netCDF4 | netCDF 形式ヒストリーの読み込み（xarray のバックエンド） | 1.7.2 |
| xgrads | GrADS 形式（`.ctl`）の読み込み（`open_grads()`） | 0.2.7 |
| matplotlib | 描画 | 3.10.7 |
| cartopy | 地図投影・海岸線（`anl/` のほぼ全スクリプト） | 0.25.0 |
| docopt | スクリプトの引数解析（`anl/` のほぼ全スクリプト） | 0.6.2 |
| pandas | 時系列処理（`anl/japan_sea`, `transport` など一部） | 2.3.3 |
| cmocean | 海洋用カラーマップ（`anl/japan_sea` など一部） | 4.0.3 |

動作実績は Python 3.13.5。作り方の例（venv の場合）:

```bash
python3 -m venv ~/venv
source ~/venv/bin/activate
pip install numpy xarray dask netCDF4 xgrads matplotlib cartopy docopt pandas cmocean
```

確認:

```bash
source ~/venv/bin/activate
python -c "import numpy, xarray, dask, netCDF4, xgrads, matplotlib, cartopy, docopt, pandas, cmocean; print('ok')"
```

* cartopy は初回の描画で Natural Earth の海岸線データをダウンロードする（ネットワークが必要）。


Docker を使う場合
--------

ローカル環境の構築で詰まったら、テストマシンと同じ Docker + Debian + gfortran (MPI) 環境を使える。
MRICOM-rect の `docker/README.md`、mxe-docker の README を参照。


完了の確認
--------

* [ ] `setting/macros.make` が作られ、`lib/` の make が通る
* [ ] Python 解析環境の import 確認が `ok` になる

動作実績（Debian 13）: gfortran 14.2.0、Open MPI 5.0.7、netCDF-Fortran 4.5.4 で [Step 3a](03-rectangle.md) が通った。Python は上表のライブラリを入れた venv で Step 3b が描けた。


落とし穴
--------

<!-- 経験したら追記 -->
