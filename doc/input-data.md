MRI.COM 入力データの形式
========

MRI.COMに与える入力ファイルの形式・単位のまとめ。一次情報は `~/mricom/README_First.md` Sec.4 と
`~/mricom/docs/README_Namelist.md`（各 `&nml_*` の説明）。本リポジトリの `prep/` で入力を作るときに参照する。


共通事項
--------

* ファイルは **Fortran unformatted**（書式なしバイナリ）。ファイルによって
  **順次アクセス（sequential、レコードマーカー付き）** と **直接アクセス（direct、マーカーなし）** が違うので注意。
* 精度も real(4) と real(8) が混在する（下表）。
* 単位は基本 **cgs**（水深・層厚は cm、拡散係数は cm²/s、風応力は dyn/cm²）。
  一部の表層過程（海氷・海面フラックス）は MKS。
* エンディアン: <!-- TODO: 要確認。入力ファイルのエンディアンはコンパイラ設定（FFLAGS）依存と思われる。
  ヒストリー出力は既定でbig endian（README_Namelist.md &nml_grads_ctl/l_big_endian）。
  本リポジトリの prep/jra3q/make_wind.py は big endian で書いている。 -->
* 格子点数（`IMUT`, `JMUT`, `KM`）は `configure.in` で決まる。入力ファイルのサイズと一致させること。


格子・地形（README_First.md Sec.4.1–4.3）
--------

| データ | namelist | アクセス | 内容（読み込み順） | 単位 |
|---|---|---|---|---|
| 鉛直層厚 | `nml_vert_grid/file_dz_cm` | sequential | `integer km` → `real(8) dz(km)` | cm（トレーサ点が層の中心） |
| 水平格子間隔（不等間隔時） | `nml_horz_grid/file_dxdy_tbox_deg` | sequential | `integer imut, jmut` → `real(8) dxtdeg(imut)` → `real(8) dytdeg(jmut)` | 度 |
| 海底地形 | `nml_topo/file_topo` | sequential | `integer(4) ho4(imut,jmut), exnn(imut,jmut)`（1レコード） | ho4: cm、exnn: 海底のある層番号（最上層=1） |
| スケールファクタ（`SPHERICAL` でない時） | `nml_grid_scale` | sequential | `real(8)` の a_bl…dy_tr を12レコード | 面積 cm²、長さ cm |
| 背景鉛直拡散の鉛直分布 | `nml_diff_vert_bg/file_diff_vert_1d_cm2ps` | sequential | `integer km` → `real(8) vdbg(km)` | cm²/s |

等間隔格子なら水平格子ファイルは不要で、`dx_const_deg`/`dy_const_deg` を指定する（ファイル指定とは排他）。

**落とし穴**:
* `exnn` と `ho4` の整合（`exnn` 層の範囲内に `ho4` が入っているか）。陸は `exnn=0`
  <!-- TODO: 要確認。陸格子の値の約束を README で確認できていない -->。
* 層厚ファイルの `km` が `configure.in` の `KM` と違うとエラー。


海面強制データ（README_First.md Sec.4.5, README_Namelist.md `&nml_force_data`）
--------

* **1ファイル1要素**、**direct access**、1レコードが `real(4) :: data(imfrc, jmfrc)`
  （`ldouble = .true.` なら real(8)）。
* 要素ごとに `&nml_force_data` を1つ書く。主な指定:

| 変数 | 意味 |
|---|---|
| `name` | 要素名（下表） |
| `file_data` | データファイル |
| `imfrc`, `jmfrc` | データの格子数 |
| `interval` | データの時間間隔 [秒]。`-999` = 定常、`-1` = 月別 |
| `num_data_max` | ファイル中のレコード数 |
| `ifstart` | 最初のレコードの**期間の開始**日時（中心ではない）`y,m,d,h,m,s` |
| `lrepeat` | 気候値として繰り返し使うか |
| `linterp` | モデル格子へ水平内挿するか（`.true.` なら `file_data_grid` が必要） |
| `luniform` | 水平一様データか（例: ゼロ場を1点で与える） |
| `lfactor`/`factor`, `loffset`/`offset` | 読み込み後の単位換算・オフセット |

* 要素名とオプションの対応:

| `name` | 内容 | 必要な条件 | 単位（換算後） |
|---|---|---|---|
| `'U-wind'`, `'V-wind'` | 風応力（`TAUBULK` 時は風速） | 常に | dyn/cm²（風速なら cm/s） |
| `'ShortWave'`, `'LongWave'` | 短波（上向き+下向き）・下向き長波 | `HFLUX` | README_Namelist.md 参照 |
| `'TempAir'`, `'SphAir'`, `'ScalarWind'`, `'SeaLevelPressure'` | 気温・比湿（`TDEW` 時は露点）・スカラー風速・海面気圧 | `HFLUX` | 同上 |
| `'Precipitation'` | 降水 | `WFLUX` | 同上 |
| `'RiverDischargeRate'` | 河川流量 | `RUNOFF`（通常 `WFLUX` と併用） | 同上 |
| `'IceConcentrationClimatology'` | 海氷密接度 | `ICECLIM` | 同上 |

**内挿用の格子ファイル（`file_data_grid`）の精度について — READMEの記述が食い違っている**:
* `README_First.md` Sec.4.4–4.5: `real(4) :: alonf(imf), alatf(jmf)` を1レコード
* `README_Namelist.md` `&nml_tracer_data` の `trcref_conf%file_data_grid`: `real(8) x, y` → `z` （sequential）、
  かつ「地理座標ではなくモデル格子座標」
* 本リポジトリの `prep/jra3q/make_wind.py` は real(8) big endian で書いている

<!-- TODO: 要確認。force_data の格子ファイルが real(4)/real(8) のどちらか、モデル開発者に確認して確定させる -->
`linterp = .false.`（モデル格子と同じ格子のデータを与える）なら格子ファイルは使われない。


トレーサのレストア・初期値（README_First.md Sec.4.4, README_Namelist.md `&nml_tracer_data`）
--------

トレーサごとに `&nml_tracer_data` を書き、参照値（初期値・ナッジング先）とレストア係数を与える。

| データ | アクセス | 1レコード | 単位 |
|---|---|---|---|
| 表層の参照値 | direct | `real(4) t_surf(imfd, jmfd)` | 水温 ℃、塩分 psu <!-- TODO: 要確認 --> |
| 表層のレストア係数 | direct | `real(8) t_surf_restore(imfd, jmfd)` | 1/s |
| 内部の参照値 | direct | `real(4) t_intr(imfd, jmfd, kmfd)` | 同上 |
| 内部のレストア係数 | direct | `real(8) t_restore_intr(imfd, jmfd, kmfd)` | 1/s |

参照値ファイルの作成ツールは `README_Namelist.md` では `MXE/prep/TRACER/` とされている。


本リポジトリでの作成ツール
--------

| ツール | 作るもの |
|---|---|
| `prep/jra3q/make_wind.py` | JRA-3Q気候値から月別風応力（`U-wind`/`V-wind` 用、big endian + GrADS ctl + 格子ファイル） |
| `prep/jra3q/make_wind-ave.py` | 同・年平均1レコード |

新しい前処理ツールを作ったらこの表に追加する。
