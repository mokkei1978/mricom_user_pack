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
  後の作業（地形・風・初期値）が先に作った `dz_cm.d`, `topo.d` を読める。4c の実験もそこから読む。
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
bash sample/make_dz-rectange-l10.sh         # → dz_cm.d, depth.txt
mv dz_cm.d depth.txt $D/                    # depth.txt は各層の深さ（確認用のテキスト）
cd ..

# (2) 地形
cd rectangle
ln -sf ../../setting/namelist/NAMELIST.MXE .
bash sample/make_topo.sh                    # → topo.d (+ topo.ctl, topo.gd)
mv topo.d $D/
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
cd ..

# (4) 初期値（水温: 表面 28℃ → 底 2℃ の線形、塩分 34 一様）
cd TRACER
ln -sf ../../setting/namelist/NAMELIST.MXE .
cp sample/make_restart.sh .
#   make_restart.sh: ln -sf sample/NAMELIST.MXE . と rm NAMELIST.MXE の 2 行を消す（下記）
bash make_restart.sh                        # → rs_t.19010101000000, rs_s.19010101000000 (+ .ctl, .gd)
mv rs_t.19010101000000 rs_s.19010101000000 $D/
cd ..

ls ../linkdir/data                          # depth.txt dz_cm.d rs_s.* rs_t.* topo.d wind_grid.d wind_x.ctl wind_x.gd zero.d
```

* **sample スクリプトの `NAMELIST.MXE` の扱いを消す**: FORCE, TRACER の sample の多くは、冒頭で
  `ln -s test/.../NAMELIST.MXE .`（MXE 同梱のテスト用）を張り、最後に `rm NAMELIST.MXE` で消す。
  そのまま使うと、自分で張った `setting/namelist/` へのリンクが使われない（または消される）ので、コピーしてこの 2 行を消す。
  なお、テスト用の `test/rect/NAMELIST.MXE` は `linkdir/mxe-data/` を指しており、clone しただけの MXE には無い（4a）。
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

* **風応力の振幅**: MXE の sample は `amplitude = 20.d0`（最大東西風応力 [dyn/cm²]）だが、
  rectangle_data は 1 dyn/cm²（= 0.1 N/m²、現実的な大きさ）で作られている。
  `name='U-wind'` は（`TAUBULK` オプションなしでは）風応力 [dyn/cm²] として読まれる（`README_Namelist.md` の "Specification of wind forcing"）。
* `rs_t` の不一致: 陸格子（`-9.99e33`）の配置は同じで、海域の差は最大 8×10⁻⁷ ℃。
  rectangle_data の `rs_t` は real(8) のファイルだが値が単精度に丸められている。
  ( MXE の出力を real(4) に丸めると完全に一致する)
* 入力ファイルの形式・単位は [../input-data.md](../input-data.md)。



4c. MXE の exp/ で実験に必要なファイルを用意する
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
* 実験用に本体の一部を修正するときは、`exp/MRICOM/` ではなく `exp/modsrc/` に修正版を置く（`exp/README-MXE.md`）。

`exp/src/`（コンパイルするディレクトリ）は `MRICOM/src/`, `modsrc/`, `config_files/` へのリンクで構成する（`exp/README-MXE.md`）。
<!-- TODO: src/ のリンクの張り方とコンパイル（./configure; make）を実際に確かめて記入 -->

### 入力・出力ディレクトリを用意する

1. MXE の `exp/` で実験ディレクトリを作り、4b の `configure.in` と入力データを使う
   （`exp/run/sample/` は MRICOM3 時代の古いもので、そのままでは使えない）
2. `NAMELIST.OGCM` は [../namelist-reference.md](../namelist-reference.md) を見ながら自分で書く
   （AI に下書きさせてもよい。下の頼み方の例）

### `configure.in` と `NAMELIST.OGCM`

`prep/rectangle/sample/configure.in`, `NAMELIST.OGCM` を型に、Step 3a の `log/configure.in`, `log/NAMELIST.OGCM`
（MRICOM-rect が実際に使ったもの）と見比べて作る。4c で使う。

TS以下のリスタートファイルを読まずに始めるには `README_Restart.md` を参照し `l_rst_*_in` を設定する。

**完了の確認**:
* [ ] 4b の入力ファイルが rectangle_data と一致する（一致しない場合は差の理由を説明できる）
* [ ] リスタート出力が Step 3 と一致する（`md5sum`）<!-- TODO: 要確認。MRICOM-rect 同梱は v5.5、MXE で使う MRI.COM は 5.4 なので、ビット一致を期待できるか。
     できない場合は何を比べて「再現できた」とするか（コンパイラ・MPI分割をそろえる条件も） -->


4d. 実験を行い再現を確かめる
--------

3. Step 3 と同じ期間を回し、結果を比べる


4e. 自分のトイモデルにする
--------

1 つずつ変えて、そのたびに 4c の手順で動作を確かめる。

1. 格子数・領域（`configure.in` の `IMUT`/`JMUT`/`KM` と `NAMELIST.MXE`、入力データを一緒に変える）
2. 地形（海嶺、陸棚、湾など。`prep/rectangle/` の `kida-ridge`, `shelf`, `bay` などが例）
3. 強制（風応力の形、熱フラックス `make_hflux.sh`）
4. 鉛直座標・層数（例: ALE 2層 `2layer-slope`。本リポジトリに描画ツールあり）

<!-- TODO: 推奨する例題（二重ジャイア、周期水路など）と、それぞれ見るべき結果 -->


落とし穴
--------

* 格子数（`configure.in`）と入力データ・`NAMELIST.MXE`・`NAMELIST.OGCM` のサイズが食い違う
  （[03-rectangle.md](03-rectangle.md)「落とし穴」）

<!-- 経験したら追記 -->


AIへの頼み方（例）
--------

```
doc/namelist-reference.md と doc/namelist-examples/rectangle/NAMELIST.OGCM を型にして、
格子を東西 2 倍にした矩形海実験の configure.in と NAMELIST.OGCM の変更点を挙げて。
不明なパラメータは ~/mricom/docs/README_Namelist.md で確認し、
そこにも書かれていなければ推測せず TODO として残すこと。
```
