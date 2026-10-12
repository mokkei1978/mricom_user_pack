Step 4: MXE で矩形海モデルを自作する
========

**目標**: MXE の前処理ツールを使い、Step 3 の MRICOM-rect と同じ設定を自分で一から作って再現する。
再現できたら、格子・地形・強制を変えた自分のトイモデルに発展させる。

**前提**: [Step 3](03-rectangle.md) を終え、MRICOM-rect の結果（入力ファイル・出力）が手元にある。
MXE を取得し（[Step 1](01-get.md)）、`lib/` をコンパイル済み（[Step 2](02-environment.md)）。


4a. rectangle と同じ入力データを作る
--------

MXE の `prep/rectangle/README-MXE.md` の順（鉛直格子 → `NAMELIST.MXE` → 地形 → 風 → 初期値）に作り、
Step 3 で MRICOM-rect が実際に読んだファイルと比べる。

### 作る対象を確かめる

MRICOM-rect の `exp/data/` にあるリンクと `run.conf` を見ると、標準設定（Step 3a）が使う入力は次のとおり
（リンク先は rectangle_data、MRICOM-rect では `linkdir/data/`）。

| ファイル | rectangle_data | 内容 | namelist（Step 3a の `log/NAMELIST.OGCM`） |
|---|---|---|---|
| `dz_cm.d` | `main.14/` | 鉛直層厚（10 層） | `&nml_vert_grid` `file_dz_cm` |
| `topo.d` | `main.03/` | 海底地形（62×52 のうち周囲 1 格子が陸、海域は水深 6000 m の平底） | `&nml_topo` `file_topo` |
| `wind_x.gd` | `wind_2gyre.01/` | 東西風応力（二重ジャイヤ型、real(4)） | `&nml_force_data` `name='U-wind'` |
| `wind_grid.d` | `wind_2gyre.01/` | 風データの格子（`linterp=.true.` のときだけ使う） | 同上 `file_data_grid` |
| `zero.d` | `wind_2gyre.01/` | 一様値 0（real(8) 1 個） | `name='V-wind'`（`luniform=.true.`, `ldouble=.true.`） |
| `rs_*.19010101000000` | `main.23/` | 初期値（`run.conf` の `initial_main`） | `&nml_restart` |

初期値 `main.23/` には `rs_t`, `rs_s` のほか `rs_u`, `rs_v`, `rs_ssh`, `rs_uml`, `rs_vml` や鉛直混合用のファイルも入っているが、
`rs_t`（線形成層）と `rs_s`（一様 34）以外は、速度・SSH がゼロ、鉛直混合関係が一様値（0.1 など）で、場としての情報はない。
MXE で作るのは `rs_t` と `rs_s` だけ。残りを読まずに始める方法は 4b で扱う（`README_Restart.md` の `l_rst_*_in`）。

### 手順

各ツールは `prep/<ツール>/sample/` のスクリプトをコピー・編集して使う（MXE の作法）。
実行は各ディレクトリで行い、生成物もそこにできる。

```bash
cd ~/mxe/prep

# (1) 鉛直格子: 各層の底の深さ 20, 50, 100, 200, 400, 600, 1000, 2000, 4000, 6000 m
cd DZ
sh sample/make_dz-rectange-l10.sh           # → dz_cm.d, depth.txt
cd ..

# (2) NAMELIST.MXE: sample を置き、dz と topo のパスを (1)(3) の出力に書き換える
cd rectangle
cp sample/NAMELIST.MXE .
#   file_dz_cm = "../DZ/dz_cm.d",   file_topo = "../rectangle/topo.d"
# (3) 地形
sh sample/make_topo.sh                      # → topo.d (+ topo.ctl, topo.gd)
cd ..

# (4) 風応力と一様値 0
cd FORCE
#   sample/make_wind.sh をコピーし amplitude = 20.d0 → 1.d0 に変える（下記）
sh make_wind.sh                             # → wind_x.gd, wind_x.ctl, wind_grid.d
#   sample/make_const.sh をコピーし value = 100.d0 → 0.d0 に変える
sh make_const.sh                            # → " 0.000E+00.d"（ファイル名は値の書式から作られ、先頭に空白が付く）
mv " 0.000E+00.d" zero.d
cd ..

# (5) 初期値（水温: 表面 28℃ → 底 2℃ の線形、塩分 34 一様）
cd TRACER
ln -sf ../rectangle/NAMELIST.MXE sample/NAMELIST.MXE   # 下記
sh sample/make_restart.sh                   # → rs_t.19010101000000, rs_s.19010101000000 (+ .ctl, .gd)
rm sample/NAMELIST.MXE
```

* `FORCE/sample/make_wind.sh` は `test/rect/NAMELIST.MXE`（MXE 同梱のテスト用。中身は (2) と格子が同じ）をリンクして使う。
* `TRACER/sample/make_restart.sh` は存在しない `sample/NAMELIST.MXE` をリンクしようとするので、
  上のように (2) の `NAMELIST.MXE` を `sample/` に置いてから実行する。

### 比べる

```bash
R=~/rect/linkdir/data                       # rectangle_data
M=~/mxe/prep
cmp $M/DZ/dz_cm.d        $R/main.14/dz_cm.d
cmp $M/rectangle/topo.d  $R/main.03/topo.d
cmp $M/FORCE/wind_x.gd   $R/wind_2gyre.01/wind_x.gd
cmp $M/FORCE/wind_grid.d $R/wind_2gyre.01/wind_grid.d
cmp $M/FORCE/zero.d      $R/wind_2gyre.01/zero.d
cmp $M/TRACER/rs_s.19010101000000 $R/main.23/rs_s.19010101000000
cmp $M/TRACER/rs_t.19010101000000 $R/main.23/rs_t.19010101000000   # ← 一致しない（下記）
```

実績（2026-10）: `rs_t` 以外はすべて一致。

* **風応力の振幅**: MXE の sample は `amplitude = 20.d0`（最大東西風応力 [dyn/cm²]）だが、
  rectangle_data は 1 dyn/cm²（= 0.1 N/m²、現実的な大きさ）で作られている。
  `name='U-wind'` は（`TAUBULK` オプションなしでは）風応力 [dyn/cm²] として読まれる（`README_Namelist.md` の "Specification of wind forcing"）。
* **`rs_t` の不一致は丸め誤差**: 陸格子（`-9.99e33`）の配置は同じで、海域の差は最大 8×10⁻⁷ ℃。
  rectangle_data の `rs_t` は real(8) のファイルだが値が単精度に丸められている
  （`main.23/README.md`: 旧版のデータ `main.07` に陸の値を入れて作り直したもの）。
  MXE の出力を real(4) に丸めると完全に一致する:
  ```python
  import numpy as np
  a = np.fromfile("rs_t.19010101000000", ">f8")                                   # MXE
  b = np.fromfile("/path/to/rectangle_data/main.23/rs_t.19010101000000", ">f8")
  print((a.astype("f4").astype("f8") == b).all())                                 # True
  ```
  このため、MXE の `rs_t` で 4b を回すと Step 3 とはビット一致しない。
  4b で Step 3 との一致を確かめるときは `main.23/` の初期値を使う。

入力ファイルの形式・単位は [../input-data.md](../input-data.md)。

### `configure.in` と `NAMELIST.OGCM`

`prep/rectangle/sample/configure.in`, `NAMELIST.OGCM` を型に、Step 3a の `log/configure.in`, `log/NAMELIST.OGCM`
（MRICOM-rect が実際に使ったもの）と見比べて作る。4b で使う。


4b. MXE の exp/ で実験を立ち上げて再現を確かめる
--------

1. MXE の `exp/` で実験ディレクトリを作り、4a の `configure.in` と入力データを使う
2. `NAMELIST.OGCM` は [../namelist-reference.md](../namelist-reference.md) を見ながら自分で書く
   （AI に下書きさせてもよい。下の頼み方の例）
3. Step 3 と同じ期間を回し、結果を比べる

**完了の確認**:
* [ ] 4a の入力ファイルが rectangle_data と一致する（一致しない場合は差の理由を説明できる）
* [ ] リスタート出力が Step 3 と一致する（`md5sum`）<!-- TODO: 要確認。MRICOM-rect 同梱は v5.5、MXE で使う MRI.COM は 5.4 なので、ビット一致を期待できるか。
     できない場合は何を比べて「再現できた」とするか（コンパイラ・MPI分割をそろえる条件も） -->


4c. 自分のトイモデルにする
--------

1 つずつ変えて、そのたびに 4b の手順で動作を確かめる。

1. 格子数・領域（`configure.in` の `IMUT`/`JMUT`/`KM` と `NAMELIST.MXE`、入力データを一緒に変える）
2. 地形（海嶺、陸棚、湾など。`prep/rectangle/` の `kida-ridge`, `shelf`, `bay` などが例）
3. 強制（風応力の形、熱フラックス `make_hflux.sh`）
4. 鉛直座標・層数（例: ALE 2層 `2layer-slope`。本リポジトリに描画ツールあり）

<!-- TODO: 推奨する例題（二重ジャイヤ、周期水路など）と、それぞれ見るべき結果 -->


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
