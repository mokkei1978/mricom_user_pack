Step 2: 実行環境の構築と確認
========

**目標**: Fortran コンパイラ・MPI・ライブラリが MRI.COM / MXE の要求どおりに動くことを確かめる。

**前提**: [Step 1](01-get.md) で MRICOM-rect を取得済み。計算機に Fortran コンパイラと MPI がインストール済み。


確認するもの
--------

| 項目 | 確認方法 |
|---|---|
| Fortran コンパイラ、推奨オプション等 | サーバー管理者に聞く。例えば `gfortran --version`で確認する |
| MPI並列コンパイル、実行方法 | 管理者に聞く。例えば `mpif90 --version`, `mpirun --version` で確認する |
| `make`, `git`, `bc` | `command -v make git bc`（パスが表示されないものが未インストール）。Debian の最小構成には入っていないので、無ければ `sudo apt install make git bc`。`make` は MXE ライブラリとモデルのビルド、`git` は取得と `configure.in` の復元、`bc` は MRICOM-rect の `run_pre.sh` が使う |
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

* netCDF が使える場合(下記)は FFLAGS に `-DMXE_NETCDF` を加え、`INCLUDES` と `LDFLAGS` に netCDF-Fortran の指定を加える。
* Debian + gfortran では FFLAGS に `-DMXE_DOCKER` を加える（Docker を使わない場合も）。
  無いと、標準入力で namelist を渡すツールが何も表示せずに止まることがある
  （`lib/libmxe_system.F90` の注記: stdin の `rewind(5)` から返ってこなくなるのを回避。[Step 4b](04-own-toy.md) で経験）。

| サンプル | 環境 |
|---|---|
| [macros.make-gfortran-netcdf](../mxe-sample/macros.make-gfortran-netcdf) | gfortran + netCDF |

### MXE ライブラリ

`setting/macros.make`が設定できれば、MXEライブラリをビルドする。
```
cd lib/
make
```

### モデル用ビルド設定

`exp/config_files/configure.in` にMPI並列Fortranコンパイル設定を記述する。

ビルド設定の書き方は 2 通りある（`README_First.md` 3.1 節、`README_Advanced.md` 1 節）。

1. **コンパイル方法を直接指定する**: 次の項目を自分で書く。
   ```sh
   F90=        # Fortran コンパイラ（MPI 用のラッパー。例: mpif90）
   FFLAGS=     # コンパイルオプション
   INCLUDES=   # ライブラリ指定（MPI ライブラリを含む）
   LDFLAGS=    # リンクオプション
   POSTFC=     # コンパイル後の処理コマンド
   ```
2. **`MACHINE` で MRI.COM の推奨設定を使う**: MRI.COM の `machines/` にある設定名を指定する。
   gfortran + Open MPI であれば `MACHINE=linux86-gfortran` が使える。
   ```sh
   MACHINE=linux86-gfortran
   ```
   `linux86-gfortran` では次が設定される。
   ```sh
   F90=mpif90
   FFLAGS="-mcmodel=large -ffree-line-length-none -fconvert=big-endian -O3"
   INCLUDES="-I."
   LDFLAGS="-mcmodel=large"
   ```

MRICOM-rect（gfortran + Open MPI）では、`configure.in` の末尾に次を加える。

```bash
cd ~/rect/exp
cat >> config_files/configure.in << 'END'

MACHINE=linux86-gfortran
FFLAGS="-mcmodel=large -fconvert=big-endian -O3"
LDFLAGS="-mcmodel=large"
END
```

* `MACHINE` と `FFLAGS` など両方書いたときには
  `FFLAGS`, `LDFLAGS` の設定が優先される（コンパイルのログ先頭の
  `default build settings for MACHINE = ...` に続く表示で確かめられる）。
* `-fconvert=big-endian`: 入出力ファイルをビッグエンディアンで読み書きする（rectangle_data はビッグエンディアン）。
* MPI 分割数は `configure.in` の `NPARTX=2`, `NPARTY=2`（計 4）。実行時の `mpirun -np 4`（[Step 3a](03-rectangle.md)）と一致させる。
* `configure.in` は git 管理下のファイル。`git checkout -- config_files` をするとこの設定も消えるので、やり直すときは上を再実行する。
* OpenMP（`-fopenmp`）はここでは説明しない（MPI 並列のみ）。OpenMP による高速化は別のチュートリアルで扱う予定。
  `-fopenmp` の有無で Step 3a のリスタート出力は変わらない（ビット一致を確認）。

ビルド設定の例は [../configure.in-example/](../configure.in-example/) にある（`configure.in` の末尾に加える部分だけ）。

| サンプル | 環境 |
|---|---|
| [configure.in-gfortran-openmpi-noomp](../configure.in-example/configure.in-gfortran-openmpi-noomp) | gfortran + Open MPI（上の設定と同じ） |
| [configure.in-gfortran-openmpi](../configure.in-example/configure.in-gfortran-openmpi) | gfortran + Open MPI + OpenMP（上の設定に `-fopenmp` を加えたもの） |



Fortran で netCDF ライブラリを使う（任意）
--------

MRI.COM のヒストリーを netCDF で出力する（オプション `NETCDF`、[Step 3d](03-rectangle.md)）、
MXE ツールで netCDF を読み書きする（`-DMXE_NETCDF`）ときに必要。GrADS 形式だけで済ませるなら不要。

必要なのは **netCDF-Fortran**（Fortran モジュール `netcdf.mod` とライブラリ `libnetcdff`）。
C 版の netCDF（`libnetcdf`）だけでは足りない。

* Debian/Ubuntu: `sudo apt install libnetcdff-dev netcdf-bin`（`netcdf-bin` は `ncdump` 用）
* スパコン・共用サーバー: `module load netcdf-fortran` などで使えることが多い。管理者に聞く。
* `netcdf.mod` はコンパイラごとに形式が違う。**モデルと同じコンパイラ**（gfortran なら gfortran）で作られたものを使う。


### コンパイル方法を調べる: `nf-config`

netCDF-Fortran に付属する `nf-config` が、コンパイル・リンクに必要なオプションを教えてくれる。

```bash
nf-config --version   # netCDF-Fortran 4.5.4
nf-config --fflags    # コンパイル時（netcdf.mod の場所）: -I/usr/include
nf-config --flibs     # リンク時: -L/usr/lib/x86_64-linux-gnu -lnetcdff -Wl,-z,relro -Wl,-z,now -lnetcdf -lnetcdf -lm
```

（実行する場所は問わない。出力は Debian 13 の例。`nf-config` が見つからなければ netCDF-Fortran が入っていないか、パスが通っていない。）


### 小さなプログラムで確かめる

テスト用サンプル・プログラム [../fortran/nctest.f90](../fortran/nctest.f90) を実行することで確かめる。
カレントディレクトリに `test.nc` を書くので、作業用ディレクトリにコピーして実行する。
手順の例。

```bash
mkdir -p ~/nctest   # 適当な作業ディレクトリ
cd ~/nctest
cp ~/mricom_user_pack/doc/fortran/nctest.f90 .
gfortran $(nf-config --fflags) nctest.f90 $(nf-config --flibs) -o nctest
./nctest          # ok:  4.9.3 of ...（netCDF C ライブラリの版）
ncdump test.nc    # data = 1, 2, 3 ;
```

コンパイラは`mpif90` に替えても同じように通る（MRI.COM は `mpif90` でコンパイルする）。

よくあるエラー:

| エラー | 原因 |
|---|---|
| `Cannot open module file 'netcdf.mod'` | コンパイル時に `-I`（`nf-config --fflags`）が無い、または別コンパイラ用の `netcdf.mod` |
| `undefined reference to '__netcdf_MOD_nf90_...'` | リンク時に `-lnetcdff`（`nf-config --flibs`）が無い |

ここで調べたオプションを、MXE は `setting/macros.make`（上記「MXE ツール用ビルド設定」）、
MRI.COM は `configure.in`（下の「MRI.COM で netCDF を使う」）に書く。


### MRI.COM で netCDF を使う

MRI.COMでnetCDF出力を使うには、`configure.in`に netCDF-Fortran の指定を次の 3 つで与える。
`nf-config --fflags`の内容を`NETCDF_INCLUDES`に設定することに注意。
実際の使い方は [Step 3d](03-rectangle.md) を、詳細は`README_Options.md` の `NETCDF` の項を参照せよ。

| 項目 | 内容 | `nf-config` との対応 |
|---|---|---|
| `NETCDF_FFLAGS` | MRI.COM の netCDF 入出力部分をコンパイルするオプション | （`FFLAGS` と同様） |
| `NETCDF_INCLUDES` | `netcdf.mod` の場所（例: `-I/usr/local/include`） | `nf-config --fflags` |
| `NETCDF_LDFLAGS` | ライブラリの場所とリンク指定（例: `-L/usr/local/lib -lnetcdff`） | `nf-config --flibs` |

* `MACHINE=linux86-gfortran` では既定値が入るので、netCDF-Fortran が標準の場所にあれば**書かなくてよい**。
  例えば Debian 13 では次のようになる（コンパイルのログ先頭に表示される）。
  ```
  NETCDF_FFLAGS    = -mcmodel=large -ffree-line-length-none -fconvert=big-endian -O3
  NETCDF_INCLUDES  = -I/usr/include
  NETCDF_LDFLAGS   = -L/usr/lib -lnetcdff -fPIE -pie -Wl,-z,relro -Wl,-z,now
  ```
  <!-- TODO: この既定値がどう決まるかを記載。 -->
* netCDF-Fortran が別の場所にある（`module load` で入れたなど）、または既定値でコンパイル・リンクに失敗するときは、
  `configure.in` の末尾に書いて上書きする。`configure.in` はシェルスクリプトとして読まれるので `$(...)` が使える。
  ```sh
  NETCDF_INCLUDES="$(nf-config --fflags)"
  NETCDF_LDFLAGS="$(nf-config --flibs)"
  ```
  反映されていることをコンパイルのログで確認する。



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
* [ ] `exp/config_files/configure.in` にビルド設定を加えた
* [ ] Python 解析環境の import 確認が `ok` になる
* [ ] （netCDF を使う場合）`nctest.f90` を `mpif90` でコンパイル・実行でき、`ncdump test.nc` で中身が見える

動作実績（Debian 13）: gfortran 14.2.0、Open MPI 5.0.7、netCDF-Fortran 4.5.4 で [Step 3a](03-rectangle.md) が通った。Python は上表のライブラリを入れた venv で Step 3b が描けた。


落とし穴
--------

<!-- 経験したら追記 -->


AIへの頼み方（例）
--------

```
doc/tutorial/02-environment.md を読んで、Step 3 の矩形海を（Docker ではなく）このマシンで
コンパイル・実行するのに足りないツール・ライブラリを、コマンドを実行して確かめて教えて。
解析用の Python 環境は除く。
```
