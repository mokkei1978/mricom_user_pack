Step 4: MXE で矩形海モデルを自作する
========

**目標**: MXE の前処理ツールを使い、Step 3 の MRICOM-rect と同じ設定を自分で一から作って再現する。
再現できたら、格子・地形・強制を変えた自分のトイモデルに発展させる。

**前提**: [Step 3](03-rectangle.md) を終え、MRICOM-rect の結果（入力ファイル・出力）が手元にある。
MXE を取得し（[Step 1](01-get.md)）、`setting/macros.make` を作って `lib/` をコンパイル済み（[Step 2](02-environment.md)）。


4a. 自分の実験パッケージを作る
--------

MXE を `git clone` し、それを自分の実験パッケージとして育てる（前処理・実行・解析を 1 か所にまとめる）。
MRICOM-rect も MXE をもとにしたパッケージで、ディレクトリ構成（`prep/`, `exp/`, `anl/` など）は共通。
ここでは名前を `~/myrect` とする（名前・場所は自由）。

Step 1 で取得した `~/mxe` は参照用（sample を見る、更新を取り込む）としてそのまま残し、作業は `~/myrect` で行う。

```bash
cd ~
git clone git@github.com:mri-ocean/MXE.git myrect
cd myrect

# マシンの環境設定と MXE ライブラリ（Step 2 と同じ。~/mxe の設定をコピーしてよい）
cp ~/mxe/setting/macros.make setting/
cd lib
make
```

* `setting/macros.make` は git 管理外（clone 直後には無い）なので、clone するたびに作る。
* Debian + gfortran では、`setting/macros.make` の `FFLAGS` に `-DMXE_DOCKER` を加える。
  無いと、標準入力で namelist を渡すツール（4b の初期値作成 `restart_unit_ctl` など）が、
  何も表示せずに止まる（`lib/libmxe_system.F90` の注記: stdin の `rewind(5)` から返ってこなくなるのを回避）。
  加えたら `lib/` で `make clean; make` し直す。
* clone 直後の `linkdir/` には `sample/` しかない。MXE 同梱のテスト用 `NAMELIST.MXE`
  （`prep/*/test/rect/NAMELIST.MXE` など）は `linkdir/mxe-data/` のファイルを指しているので、そのままでは使えない。
  4b では自分で作る `setting/namelist/NAMELIST.MXE` を使う。
* 以降の変更（スクリプト・namelist・`configure.in`）を git で管理するなら、自分のブランチを作っておくとよい
  （`git switch -c myrect`）。

### 実験入力・出力ディレクトリ

`linkdir/` に、入力データ置き場 `data` と実験出力置き場 `result` へのシンボリック・リンクを作る
（MRICOM-rect の `linkdir/data`, `linkdir/result` と同じ役割。[Step 2](02-environment.md)）。
入力データも実験出力も大きくなるので、リンク先は home 領域ではなく外部ディスク（RAID などのデータ置き場）にする
（[Step 1](01-get.md) の「配置」）。

```bash
D=<外部ディスク>/myrect                     # 例: /data01/$USER/myrect
mkdir -p $D/data $D/result

cd ~/myrect/linkdir
ln -s $D/data   data
ln -s $D/result result
ls -l                                       # data -> .../myrect/data, result -> .../myrect/result
```

* `linkdir/sample/link.sh` は気象研のマシン用の例なので使わず、手で作る。
* `data`, `result` は MXE の `linkdir/.gitignore` に含まれないので、git では未追跡（`??`）と表示される。
  気になるなら `linkdir/.gitignore` に `/data`, `/result` を加える。


4b. MRICOM-rect と同じ入力データを作る
--------

矩形海実験を実行するために必要な、最低限の入力ファイルを作成する。


### 作成ファイル

MRICOM-rect の標準設定（Step 3a）が使う入力ファイルを以下の順番で作成する。
具体的にはStep 1で取得した rectangle_data 中のファイルを自分で作る。

| ファイル | rectangle_data | 内容 | 対応する MRI.COM namelist（`NAMELIST.OGCM`） |
|---|---|---|---|
| `dz_cm.d` | `main.14/` | 鉛直層厚（10 層） | `&nml_vert_grid` `file_dz_cm` |
| `topo.d` | `main.03/` | 海底地形（62×52 のうち周囲 1 格子が陸、海域は水深 6000 m の平底） | `&nml_topo` `file_topo` |
| `wind_x.gd` | `wind_2gyre.01/` | 東西風応力（二重ジャイア型、real(4)） | `&nml_force_data` `name='U-wind'` |
| `zero.d` | `wind_2gyre.01/` | 一様値 0（real(8) 1 個） | `name='V-wind'`（`luniform=.true.`, `ldouble=.true.`） |
| `rs_[ts].19010101000000` | `main.23/` | 水温・塩分初期値 | `&nml_restart` |

 `rectangle_data/main.23/` には `rs_t`, `rs_s` のほか `rs_u`, `rs_v`, `rs_ssh`, `rs_uml`, `rs_vml` や鉛直混合用のファイルも入っているが、
`rs_t`（線形成層）と `rs_s`（一様 34）以外は、速度・SSH がゼロ、鉛直混合関係が一様値（0.1 など）で、場としての情報はない。
MXE で作るのは `rs_t` と `rs_s` だけ。


### 手順

各ツールは `prep/<ツール>/sample/` のスクリプトを使う（必要ならコピー・編集する。MXE の作法）。
実行は各ディレクトリで行い、生成物もそこにできる。

* 格子の情報は `NAMELIST.MXE` 1 つにまとめ、`setting/namelist/` に置く。
  各ツールのディレクトリにはそれへのシンボリック・リンクを張る（MRICOM-rect も `setting/namelist/` に置いている）。
* できた入力ファイルはすぐに `linkdir/data/`（4a）へ移す。`NAMELIST.MXE` が指すのはそこなので、
  後の作業（地形・風・初期値）が先に作った `dz_cm.d`, `topo.d` を読める。実験もそこから読む（4d）。
* sample スクリプトは `#!/bin/bash` なので `bash` で実行する。

#### (0) NAMELIST.MXE を作る

`prep/rectangle/sample/NAMELIST.MXE`（62×52×10 の矩形海の格子）をコピーし、ファイルのパスを `linkdir/data/` に書き換える。

```bash
cd ~/myrect
mkdir -p setting/namelist
cp prep/rectangle/sample/NAMELIST.MXE setting/namelist/
```

`setting/namelist/NAMELIST.MXE` の変更箇所:

```
&nml_vert_grid
  file_dz_cm            = "../../linkdir/data/dz_cm.d",
/
...
&nml_topo
  file_topo             = "../../linkdir/data/topo.d",
/
```

* パスは `NAMELIST.MXE` を読むディレクトリ（`prep/<ツール>/`）からの相対パス。
  `prep/<ツール>/`, `exp/run/`, `anl/<ツール>/` はどれも 2 階層下なので、同じ書き方でどこからでも使える。
* この時点では `dz_cm.d`, `topo.d` はまだ無い。下の (1)(2) で作る。

#### (1)〜(4) 入力ファイルを作る

```bash
cd ~/myrect/prep
D=../../linkdir/data                        # 各ツールのディレクトリから見た linkdir/data

# (1) 鉛直格子: 各層の底の深さ 20, 50, 100, 200, 400, 600, 1000, 2000, 4000, 6000 m
cd DZ
cp sample/make_dz-rectange-l10.sh .
bash make_dz-rectange-l10.sh                # → dz_cm.d, depth.txt
mv dz_cm.d depth.txt $D/                    # depth.txt は各層の深さ（確認用のテキスト）
make clean
cd ..

# (2) 地形
cd rectangle
ln -sf ../../setting/namelist/NAMELIST.MXE .
cp sample/make_topo.sh .
bash make_topo.sh                    # → topo.d (+ topo.ctl, topo.gd)
mv topo.d $D/
make clean
cd ..

# (3) 風応力と一様値 0
cd FORCE
ln -sf ../../setting/namelist/NAMELIST.MXE .
cp sample/make_wind.sh sample/make_const.sh .
#   make_wind.sh:  ln -s test/rect/NAMELIST.MXE . と rm NAMELIST.MXE の 2 行を消す（下記）
#                  amplitude = 20.d0 → 1.d0 に変える（下記）
#   make_const.sh: value = 100.d0 → 0.d0 に変える
bash make_wind.sh                           # → wind_x.gd, wind_x.ctl, wind_grid.d
bash make_const.sh                          # → " 0.000E+00.d"（ファイル名は値の書式から作られ、先頭に空白が付く）
mv wind_x.gd wind_x.ctl wind_grid.d $D/        # wind_x.ctl は GrADS で見るため（wind_x.gd と同じ場所に置く）
mv " 0.000E+00.d" $D/zero.d
make clean
cd ..

# (4) 初期値（水温: 表面 28℃ → 底 2℃ の線形、塩分 34 一様）
cd TRACER
ln -sf ../../setting/namelist/NAMELIST.MXE .
cp sample/make_restart.sh .
#   make_restart.sh: ln -sf sample/NAMELIST.MXE . と rm NAMELIST.MXE の 2 行を消す（下記）
bash make_restart.sh                        # → rs_t.19010101000000, rs_s.19010101000000 (+ .ctl, .gd)
mv rs_t.19010101000000 rs_s.19010101000000 $D/
make clean
cd ..

ls ../linkdir/data                          # depth.txt dz_cm.d rs_s.* rs_t.* topo.d wind_grid.d wind_x.ctl wind_x.gd zero.d
```

* sample スクリプトの `NAMELIST.MXE` の扱い: FORCE, TRACER の sample の多くは、冒頭で
  `ln -s test/.../NAMELIST.MXE .`（MXE 同梱のテスト用）を張り、最後に `rm NAMELIST.MXE` で消す。
  そのまま使うと、自分で張った `setting/namelist/` へのリンクが使われない（または消される）ので、コピーしてこの 2 行を消す。
* `wind_grid.d` は風データの格子で、README では `linterp = .true.`（水平補間する）のときに必要とされる。
  Step 3a の `NAMELIST.OGCM` は `linterp = .false.` だが `file_data_grid` にこのファイルを指定しているので、同じ namelist を使えるよう一緒に移す。
* ほかの GrADS 用ファイル（`topo.ctl`, `topo.gd`, `rs_*.ctl`, `rs_*.gd`）は `prep/` に残す（モデルは読まない。下の「比べる」で使う）。


### 比べる

作ったファイルが rectangle_data と同じ内容になっているかを確かめる。

**(a) バイナリで比べる**

```bash
R=~/rect/linkdir/data                       # rectangle_data
D=~/myrect/linkdir/data                     # (1)〜(4) で置いたもの
cmp $D/dz_cm.d     $R/main.14/dz_cm.d
cmp $D/topo.d      $R/main.03/topo.d
cmp $D/wind_x.gd   $R/wind_2gyre.01/wind_x.gd
cmp $D/wind_grid.d $R/wind_2gyre.01/wind_grid.d
cmp $D/zero.d      $R/wind_2gyre.01/zero.d
cmp $D/rs_s.19010101000000 $R/main.23/rs_s.19010101000000
cmp $D/rs_t.19010101000000 $R/main.23/rs_t.19010101000000
```

実績（2026-10、Debian 13 + gfortran 14.2）: `rs_t` 以外はすべて一致（`rs_t` が一致しない理由は下記）。

**バイナリ一致しなくてもよい。** 実質的な内容（格子・値の分布・単位）が合っていれば、4c に進んでよい。
コンパイラや最適化オプション、計算機が違うと、計算した値の最後の桁が変わることがあり、
`rs_t` 以外のファイルも一致しない可能性がある。
一致しないファイルは (b) で中身を確かめる。

**(b) 中身を確かめる**

鉛直格子は `depth.txt`（各層の厚さ・深さの表）で確かめる。

```bash
cat $D/depth.txt
```

* 層数が 10、`dep`（各層の上端の深さ [m]）が 0, 20, 50, 100, 200, 400, 600, 1000, 2000, 4000、
  `dz`（層厚 [m]）が 20, 30, 50, 100, 200, 200, 400, 1000, 2000, 2000 になっていること
  （1 つの層が 2 行に分かれて表示される。`dep`, `dp` は各層の上端・中心の深さ）。

地形・風・初期値は GrADS の図で確かめる（`prep/` で `grads -l` を起動）。

```
ga-> open rectangle/topo.ctl                # 地形
ga-> set mpdraw off
ga-> set gxout grfill
ga-> d ho4/100                              # 水深 [m]
ga-> reinit
ga-> open ../linkdir/data/wind_x.ctl        # 東西風応力 [dyn/cm²]
ga-> set x 30
ga-> d wind
ga-> reinit
ga-> open TRACER/rs_t.19010101000000.ctl    # 水温の初期値 [℃]（rs_s も同様）
ga-> set x 30
ga-> set y 25
ga-> set z 1 10
ga-> set yflip on
ga-> d d
```

* 地形: 海域は一様に 6000 m（等値線で描くと `Constant field.  Value = 6000`）、周囲 1 格子が陸（空白）。
* 風応力: 南北方向に cos 型で、35°N で +1、両端（10°N, 60°N）で −1（二重ジャイア型）。
  rectangle_data の `wind_2gyre.01/wind_x.ctl`（変数名 `uo`）でも同じ図を描いて比べるとよい
  （カレンダーの設定が違うので、同じ GrADS セッションでは両方を開けない。`reinit` してから開く）。
* 水温: 表面 28℃ から海底（6000 m）2℃ まで深さに比例して下がる。値は各層の中心の深さでのものなので、
  第 1 層（10 m）は 27.96℃、最下層（5000 m）は 6.33℃。塩分は全層で 34。

補足:

* 風応力の振幅: MXE の sample は `amplitude = 20.d0`（最大東西風応力 [dyn/cm²]）だが、
  rectangle_data は 1 dyn/cm²（= 0.1 N/m²、現実的な大きさ）で作られている。
  MRI.COMの入力データ(`name='U-wind'`) は（`TAUBULK` オプションなしでは）
  風応力 [dyn/cm²] として読まれる（`README_Namelist.md` の "Specification of wind forcing"）。
* `rs_t` の不一致: 陸格子（`-9.99e33`）の配置は同じで、海域の差は最大 8×10⁻⁷ ℃。
  rectangle_data の `rs_t` は real(8) のファイルだが値が単精度に丸められている。
  ( MXE の出力を real(4) に丸めると完全に一致する)
* 入力ファイルの形式・単位の詳細は [../input-data.md](../input-data.md)。
* ファイルをどのように作っているかは各スクリプトが実行するFortranプログラムを参照。



4c. MRI.COM をコンパイルする
--------

### MRI.COM を展開する

MXE の `exp/` は MRI.COM 実験の標準的なディレクトリ構成で（`exp/README-MXE.md`）、
`exp/MRICOM/` に MRI.COM 本体の**コピー**を置く（リンクではなく、`.git/` など不要なものを除いたコピー）。
実験に使った本体をパッケージ内に固定しておくため、`~/mricom` を更新しても実験には影響しない。

```bash
cd ~/mricom
git switch 5_4                 # 使うバージョン（Step 1）
git status                     # 未コミットの変更がないこと
git log -1 --oneline           # コピーする版を記録しておく（コピーには .git/ が無いので後から分からない）

rsync -a --exclude=.git ~/mricom/ ~/myrect/exp/MRICOM/
ls ~/myrect/exp/MRICOM         # README_First.md, docs/, src/, samples/, tools/ など
```

* clone 直後の `exp/MRICOM/` は空（`.gitkeep` だけ）。
* コピーした本体は `~/myrect` の git では未追跡（`??`）になる。パッケージに含めて commit するかは自分で決める。
* MRI.COM を更新するときは、`~/mricom` を更新してから同じ `rsync` をやり直す
  （`~/mricom` から消えたファイルも消すなら `--delete` を付ける）。
* 実験用に本体の一部を修正するときは、`exp/MRICOM/` ではなく `exp/modsrc/` に修正版を置く（`exp/README-MXE.md`）。(Step 5へ移す？)

### `configure.in` を作る

`configure.in` には、モデルのオプション・格子数・MPI 分割数と、ビルド設定（コンパイラなど）を書く
（`README_First.md` の 3.1）。`exp/config_files/` に置く。

Step 3 の結果と比べるので、Step 3a で MRICOM-rect が使った `configure.in`（`log/configure.in`）と同じモデル設定にする。
そのモデル設定を抜き出した雛形 [../sample_ogcm/rectangle/configure.in](../sample_ogcm/rectangle/configure.in) に、
[Step 2](02-environment.md) と同じビルド設定を末尾に加える。

```bash
cd ~/myrect/exp/config_files
E=~/mricom_user_pack/doc/sample_ogcm
cat $E/rectangle/configure.in $E/configure.in-gfortran-openmpi-noomp > configure.in
```


### コンパイルする

MRI.COMのコンパイルは `exp/src/` で行うため、そのディレクトリ内に `MRICOM/src/`, `config_files/configure.in` へのリンクを作成する（`exp/README-MXE.md`）。
コンパイルは `./configure` と `make` で行う（`README_First.md` の 3.2）。

```bash
cd ~/myrect/exp/src
ln -s ../MRICOM/src/* .                     # MRI.COM 本体
ln -sf ../config_files/configure.in .       # 上で作ったもの
./configure                                 # ビルド設定が表示される
make -j 4                                   # → ogcm (4並列でコンパイル)
ls -l ogcm
```

実績（2026-10、Debian 13 + gfortran 14.2 + Open MPI、MRI.COM 5_4）: `make -j 4` で約 20 秒。

* `MRICOM/src/` には `configure.in` が無いので、`config_files/configure.in` へのリンクが上書きになることはない。
* `./configure` の表示（`default build settings for MACHINE = linux86-gfortran` に続く `F90`, `FFLAGS` など）で、
  ビルド設定が [Step 2](02-environment.md) のとおりかを確かめる。
* `modsrc/` に修正版を置いたときは、そのファイルを `ln -sf ../modsrc/<ファイル> .` で上書きする（本体のリンクと差し替わる）。
* `exp/src/` のリンク・生成物と `config_files/configure.in` は、git では未追跡（`??`）と表示される。

**完了の確認**:
* [ ] `exp/src/ogcm` ができる


4d. 実行に必要なファイルを用意する
--------

実行は `exp/run/` で行う。モデルは `exp/run/` からの相対パスで、地形等の入力データを `exp/data/`、リスタートを `exp/restart/` から読み書きする。
（MRICOM-rect とほぼ同じ構成。）


### 入力データへのリンクを作る

`exp/data/` は入力データへのシンボリック・リンク集（`exp/README-MXE.md`。データ自体は置かない）。
4b で `linkdir/data/` に置いたファイルへのリンクを張る。

```bash
cd ~/myrect/exp/data
for f in dz_cm.d topo.d wind_x.gd wind_grid.d zero.d; do
  ln -sf ../../linkdir/data/$f .
done
ls -lL                                      # リンク先のファイルが見えること
```


### リスタートの置き場を作る

リスタート（初期値の入力と、計算終了時の出力）の置き場を、実験出力置き場 `linkdir/result/`（4a）の下に実験ごとに作り、
`exp/restart` からリンクする。初期値（4b の `rs_t`, `rs_s`）はそこへリンクする。

```bash
EXP=test4                                   # 実験名（自由）
cd ~/myrect
mkdir -p linkdir/result/$EXP/restart
cd exp
ln -sfn ../linkdir/result/$EXP/restart restart
cd restart
ln -sf $(readlink -f ../../linkdir/data)/rs_[ts].19010101000000 .
ls -l                                       # rs_s.19010101000000, rs_t.19010101000000
```

* 初期値のリンクは絶対パスで張る（`restart` 自体がリンクなので、相対パスだと `linkdir/result/$EXP/restart/` から辿ることになる）。
* 実験を変えるときは `EXP` を変えて作り直せば、前の実験の出力が残る。


### `NAMELIST.OGCM` を作る

[../sample_ogcm/rectangle/NAMELIST.OGCM](../sample_ogcm/rectangle/NAMELIST.OGCM) を `exp/run/` にコピーする。

```bash
cd ~/myrect/exp/run
cp ~/mricom_user_pack/doc/sample_ogcm/rectangle/NAMELIST.OGCM .
```

これは Step 3a の `log/NAMELIST.OGCM`（MRICOM-rect が実際に使ったもの）を次のように変えたもの。
各パラメータは [../namelist-reference.md](../namelist-reference.md) を見ながら確かめるとよい。

* 初期値として水温・塩分だけを読む。MRICOM-rect は全変数のリスタートを読むが（`l_rst_in = .true.`）、
  4b で作ったのは `rs_t`, `rs_s` だけなので次のようにする。
  ```
  &nml_run_ini_state
    l_rst_in        = .false.,   ! 速度・SSH はゼロ（静止）から始める
    ...
  /
  &nml_tracer_run
    l_rst_tracer_in = .true.,    ! 水温・塩分はリスタートファイルから読む
  /
  &nml_vmix_run
    l_rst_vmix_out  = .true.,    ! 鉛直混合係数のリスタートも書く（下の注意）
  /
  ```
  MRICOM-rectで読む `rs_u` などは値がゼロ（4b）なので、読まなくても同じ初期状態になる。
* 詳細は `~/mricom/docs/README_Restart.md`

注意: `README_Restart.md` では `l_rst_vmix_out` の既定値は `l_rst_out`（既定 `.true.`）とあるが、
実際には `.false.` で、省くと `rs_vmix_avd`, `rs_vmix_avm` が書かれない（標準出力に `l_rst_vmix_out = F (same as default)` と出る）。
<-- TODO: fix MRI.COM -->

**完了の確認**:
* [ ] `exp/data/` の 5 つのリンク、`exp/restart/` の初期値 2 つ、`exp/run/NAMELIST.OGCM` がある


4e. 実験を行い再現を確かめる
--------

Step 3a と同じく 10 日間（`nstep_total = 240`、`dt_sec = 3600`）回し、リスタート出力とヒストリー出力を比べる。

### ヒストリー出力を加える

4d の `NAMELIST.OGCM` だけでは、出力はリスタートと標準出力だけになる。
解析用の時系列（ヒストリー出力）は、別のファイル `NAMELIST.OGCM.MONITOR` に `&nml_history` を並べて指定する（`README_Monitor.md`）。
ここでは基本的な水温・塩分・流速（東西・南北）・SSH と、鉛直積分した流量（東西・南北）の日平均だけを出力する
[../sample_ogcm/rectangle/NAMELIST.OGCM.MONITOR](../sample_ogcm/rectangle/NAMELIST.OGCM.MONITOR) を使う。

```bash
EXP=test4                                   # 4d と同じ実験名
cd ~/myrect
mkdir -p linkdir/result/$EXP/hst_day
cd exp
ln -sfn ../linkdir/result/$EXP/hst_day hst_day

cd run
cp ~/mricom_user_pack/doc/sample_ogcm/rectangle/NAMELIST.OGCM.MONITOR .
```

1 つの出力は次のように書く（水温の例）。

```
&nml_history
  name                          = 'temperature',          ! 出力する量（README_Monitor.md の "Available outputs"）
  file_base                     = '../hst_day/hs_t',      ! 出力ファイル名（.ctl と .1901 が付く）
  interval_step                 = -2,                     ! 出力間隔。-2 = 1 日ごと
  suffix                        = "year",                 ! ファイルを年ごとに分ける（.1901）
/
```

* `interval_step` は正ならステップ数（`dt_sec = 3600` なら 24 で 1 日）、0 以下ならカレンダーに沿った間隔
  （0: 1 年, -1: 1 か月, -2: 1 日, -3: 1 時間など。`README_Monitor.md`）。`dt_sec` を変えても書き直さなくてよい。
* `sampling` を省くと間隔内の平均（`"mean"`）になる。
* MRICOM-rect（Step 3a）はほかにも保存量・地点・強制などを出力している（`log/NAMELIST.OGCM.MONITOR`。
  `run/nml_monitor/hs_*.nml` を `run.conf` の設定に従ってつなげたもの。[rect_workflow.md](rect_workflow.md)）。
  必要になったら `README_Monitor.md` を見て加える。

### 実行する

```bash
cd ~/myrect/exp/run
cp ../src/ogcm .
mpirun -np 4 ./ogcm > mpirun.log 2>&1      # 4 = NPARTX×NPARTY。数秒で終わる
tail -3 OGCM-19010101-stdout.0000           # 標準出力（プロセスごとに .0000〜.0003）
ls ../restart                               # rs_*.19010111000000 が 12 個
ls ../hst_day                               # hs_{t,s,u,v,ssh,sfc_um,sfc_vm}.ctl, .1901
```

### 比べる

リスタート出力とヒストリー出力を、Step 3a のものとバイナリで比べる。

```bash
R=~/rect/exp                                # Step 3a の出力（restart-main, hst_day-main）
cd ~/myrect/exp
for f in restart/rs_*.19010111000000; do
  cmp -s $f $R/restart-main/${f#restart/} && echo "same $f" || echo "DIFF $f"
done
for v in t s u v ssh sfc_um sfc_vm; do
  f=hs_$v.1901
  cmp -s hst_day/$f $R/hst_day-main/$f && echo "same $f" || echo "DIFF $f"
done
```

実績（2026-10、Debian 13 + gfortran 14.2 + Open MPI、MRI.COM 5_4。Step 3a は MRICOM-rect 同梱の 5.5）:

* リスタート出力は `rs_density`, `rs_vmix_avd`, `rs_vmix_avm` が一致、ほかは一致しない。
  差は最大で水温 8×10⁻⁷ ℃、流速 2×10⁻⁶ cm/s と小さい。ヒストリー出力も `hs_s` 以外は一致しない。
* 初期値 `rs_t` だけを rectangle_data のもの（`main.23/`）に替えて回すと、リスタート出力・ヒストリー出力ともすべてビット一致する。
  つまり差の原因は 4b の `rs_t` の不一致（単精度への丸め）だけで、MRI.COM の版（5_4 と 5.5）・
  初期値の読み方（全変数を読む / 水温・塩分だけ読む）・`interval_step` の書き方（24 / -2）の違いは結果に影響しない。
* `.ctl` の時間軸（`TDEF`）は違う。Step 3a（`interval_step = 24`）は 1 月 1 日 23 時から 10 個、
  ここ（`-2`）は 1 月 1 日 0 時から 365 個（1 年分）。日付で選べば（下の `1901-01-10`）同じ日のデータになる。

Step 3b と同じ図を描いて見比べる（差が小さいので、図では区別できない）。

```bash
source ~/venv/bin/activate
cd ~/mricom_user_pack/anl/rectangle
python contour_ssh_um_grads.py  ~/myrect/exp/hst_day 1901-01-10 test4   # (1) SSH + 鉛直積分速度（hs_sfc_um/vm）→ temp.png
python contour_ssh_vel_grads.py ~/myrect/exp/hst_day 1901-01-10 test4   # (2) SSH + 第 1 層の速度（hs_u/v）→ temp.png
```

* `interval_step` が 0 以下だと `.ctl` は 1 年分の `TDEF` を持つが、データは回した 10 日分しかない。
  xgrads はそのままでは `no enough files for 365 time records` で止まる。
  本リポジトリの `lib/mricom.py` の `open_grads()` は、データファイルにある分だけ読むようにしてある。

**完了の確認**:
* [ ] 4b の入力ファイルが rectangle_data と一致する（一致しない場合は差の理由を説明できる）
* [ ] リスタート出力・ヒストリー出力が Step 3a と一致する。一致しない場合は、初期値を rectangle_data のものに替えると一致することを確かめる
* [ ] Step 3b と同じ図が描ける


4f. 自分のトイモデルにする
--------

1 つずつ変えて、そのたびに 4c〜4e の手順で動作を確かめる。

1. 格子数・領域（`configure.in` の `IMUT`/`JMUT`/`KM` と `NAMELIST.MXE`、入力データを一緒に変える）
2. 地形（海嶺、陸棚、湾など。`prep/rectangle/` の `kida-ridge`, `shelf`, `bay` などが例）
3. 強制（風応力の形、熱フラックス `make_hflux.sh`）
4. 鉛直座標・層数（例: ALE 2層 `2layer-slope`。本リポジトリに描画ツールあり）

<!-- TODO: 推奨する例題（二重ジャイア、周期水路など）と、それぞれ見るべき結果 -->


落とし穴
--------

* 格子数（`configure.in`）と入力データ・`NAMELIST.MXE`・`NAMELIST.OGCM` のサイズが食い違う
  （[03-rectangle.md](03-rectangle.md)「落とし穴」）
* `&nml_vmix_run` の `l_rst_vmix_out` を省くと、鉛直混合係数のリスタートが書かれない
  （`README_Restart.md` の既定値の記述と違う。4d）。エラーにはならない。

<!-- 経験したら追記 -->


トラブルシューティング
--------

* 実行直後に `mpirun` が exit code 2 で止まり、Backtrace に `ogfile_open_fmtseq` と `read_stations_and_register` が出る
  → 地点モニターの地点リスト（`NAMELIST.OGCM.MONITOR` の `file_stations_csv`）が無い。
  標準出力 `OGCM-*-stdout.0000` の末尾に、読もうとした `file_stations_csv` が出ている。
  → そのパスに地点リストを置く（MRICOM-rect では `exp/run/namelist/stations.csv`）か、地点モニターの `&nml_history` を消す。


AIへの頼み方（例）
--------

```
doc/namelist-reference.md と doc/sample_ogcm/rectangle/NAMELIST.OGCM をひな型にして、
格子を東西 2 倍にした矩形海実験の configure.in と NAMELIST.OGCM の変更点を挙げて。
不明なパラメータは ~/mricom/docs/README_Namelist.md で確認し、
そこにも書かれていなければ推測せず TODO として残すこと。
```
