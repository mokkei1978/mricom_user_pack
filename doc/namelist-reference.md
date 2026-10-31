MRI.COM Namelist リファレンス（雛形）
========

MRI.COMの実行に必要なNamelist（`NAMELIST.OGCM`）作成をAIに手伝ってもらうための参照ドキュメント。
人間が読むためだけでなく、Claude等のAIアシスタントに読ませて
「妥当なnamelistを提案させる／レビューさせる」ことを主目的とする。

対象バージョン: MRI.COM 安定版 v5.4（ブランチ `5_4`）の `docs/README_Namelist.md` に基づく。

> **情報源のルール**: AIが参照してよいのはMRI.COMのREADME類のみ。モデル本体のソース（`src/` など）は
> 参照禁止（[README.md](README.md)）。READMEに無い情報は推測で埋めず、TODOとして残すこと。


このドキュメントの使い方
--------

**人間向け**：各グループの意味を調べる辞書として使う。埋まっていない項目は
`~/mricom/docs/README_Namelist.md`（全namelistの一次情報源）を見て追記する。

**AI向け**：namelist作成・レビューを頼むときは、このファイルとリポジトリ内の
実例（後述）を読ませたうえで依頼する。例:

```
doc/namelist-reference.md を読んで、水平1度・鉛直40層・矩形海領域の
1年spin-up run用のNAMELIST.OGCMを作って。
```

AIが自力で正しく埋められるのは「このドキュメントに書いてある範囲」だけ。
未記載のグループを使う場合は、まずこのファイルに追記してから依頼するか、
モデル本体の `README_Namelist.md` を合わせて渡すこと。

**このドキュメントの限界（重要）**：
AIが生成したnamelistは実行前に必ず人間がレビューすること。
namelistの誤りはクラッシュではなく「エラーなく走るが物理的に不正な結果」を生むことが多い
（単位取り違え、CFL条件違反、マスク不整合など）。「AIは下書き係、投入前チェックは人間」という運用を徹底する。


Namelistファイルの基本
--------

* 実行ディレクトリに置く `NAMELIST.OGCM` というファイル名のFortran namelist形式ファイル
  （`configure.in` で `NAME_MODEL` を指定した場合はファイル名が変わる）。
* 1ファイルの中に `&nml_xxx ... /` の形のグループを必要な数だけ並べる。
* **同じグループ名を複数回書けるものがある**（例: `&nml_force_data` を強制項目ごとに、
  `&nml_tracer_data` をトレーサごとに、`&nml_restart` を出力変数ごとに繰り返す）。
  AIに生成させる際はこの繰り返しパターンを崩さないよう注意する。
* リスタート関連（`README_Restart`）・出力/モニタ関連（`README_Monitor`）は
  別ドキュメントに詳細がある。このファイルでは概要のみ扱う。


グループ一覧（カテゴリ別・整備状況）
--------

進捗管理用。「済」はこのファイルに詳細テーブルがあるもの、「未」は名前だけ把握していて
中身は本体の `README_Namelist.md` を都度参照する必要があるもの。

### 格子・地形

| グループ | 内容 | 状態 |
|---|---|---|
| `nml_horz_grid` | 水平格子（範囲・間隔） | 済 |
| `nml_vert_grid` | 鉛直格子（層厚） | 済 |
| `nml_poles` | モデル座標系の極位置 | 未 |
| `nml_grid_scale` | 座標変換のスケールファクタ（非SPHERICAL時） | 未 |
| `nml_topo` | 海底地形ファイル | 済 |

### 時間積分

| グループ | 内容 | 状態 |
|---|---|---|
| `nml_time_step` | 時間刻み幅など | 済 |
| `nml_exp_start` | 実験全体の開始時刻 | 済 |
| `nml_run_ini` | この run の開始時刻 | 済 |
| `nml_run_period` | この run の総ステップ数 | 済 |
| `nml_run_ini_state` | 初期値をリスタートから読むか | 済 |
| `nml_barotropic_model` | 順圧モードの時間刻み | 済 |
| `nml_calendar` | 閏年の強制指定 | 未 |

### 力学・混合

| グループ | 内容 | 状態 |
|---|---|---|
| `nml_baroclinic_visc_horz` | 傾圧粘性（水平） | 済 |
| `nml_smagor` | Smagorinsky 粘性（`SMAGOR`） | 済 |
| `nml_hvisc_add` | ラプラシアン粘性の追加 | 済 |
| `nml_tracer_diff_horz` | トレーサ水平拡散 | 未 |
| `nml_barotropic_diff` | 順圧SSH拡散 | 未 |
| `nml_visc_vert_bg`, `nml_diff_vert_bg`, `nml_vmbg3d` | 鉛直粘性・拡散（背景値） | 未 |
| `nml_gls` | GLS鉛直混合スキーム | 未 |
| `nml_gmvar*`, `nml_tracer_diff_isopy*` | GM/等密度面混合 | 未 |

### 外部強制

| グループ | 内容 | 状態 |
|---|---|---|
| `nml_force_data` | 外部強制データ（風応力など、変数ごとに複数回） | 済（最小限） |
| `nml_bulkecmwf`, `nml_bulkkara` | バルク法による海面フラックス | 未 |
| `nml_sss_restore` | 海面塩分のレストア | 未 |

### トレーサ

| グループ | 内容 | 状態 |
|---|---|---|
| `nml_tracer_data` | 水温・塩分などトレーサ初期値/移流スキーム（トレーサごとに複数回） | 済（最小限） |
| `nml_tracer_run` | トレーサ初期化方法 | 未 |

### 海氷・生態系・潮汐・ネスティング・フロート

| グループ | 内容 | 状態 |
|---|---|---|
| `nml_seaice_*` | 海氷モデル一式 | 未 |
| `nml_bioNPZD`, `nml_bioNEMURO` | 生態系モデル | 未 |
| `nml_tide_*` | 潮汐強制 | 未 |
| `nml_nest_*` | ネスティング | 未 |
| `nml_oflt` | 粒子追跡（フロート） | 未 |

### 出力・実行制御

| グループ | 内容 | 状態 |
|---|---|---|
| `nml_stdout` | 標準出力の扱い | 済 |
| `nml_mpi` | MPI実行設定 | 済（最小限） |
| `nml_budget_oc` | 熱・塩分収支の出力間隔 | 未 |
| `nml_restart` | リスタートファイル入出力（変数ごとに複数回） | 済（最小限。詳細はREADME_Restart） |

> 「未」の行を使う場合は、`~/mricom/docs/README_Namelist.md` から
> 該当グループの説明を写経してこの表と下の詳細セクションに追記していく運用とする。


各グループの記述フォーマット（テンプレート）
--------

新しいグループを追記するときはこの形式に合わせる。AIが構造的に読み取りやすいよう
表形式を基本とし、依存関係・注意点は表の外に文章で書く。

```markdown
### `&nml_グループ名` (ソースファイル名.F90)

<この設定が何を制御するかを1-2行で>

| パラメータ | 型 | 単位 | デフォルト | 説明 |
|---|---|---|---|---|
| param_name | real(8) | cm/s | (必須) | ... |

**依存・注意点**:
- 他のグループとの排他/依存関係（例: AとBは同時に指定できない）
- 単位の取り違えやすさ、桁の目安
- 実行時エラーになりやすい条件
```


詳細: 格子・時間積分グループ
--------

まず使用頻度が高い格子・時間積分系のグループを埋めた例を示す。

### `&nml_horz_grid` (gridm.F90)

水平格子の範囲と間隔を指定する。

| パラメータ | 型 | 単位 | デフォルト | 説明 |
|---|---|---|---|---|
| lon_west_end_of_core | real(8) | 度 | (必須) | モデル領域（バッファ域を除くコア域）の西端経度 |
| lat_south_end_of_core | real(8) | 度 | (必須) | モデル領域の南端緯度 |
| dx_const_deg | real(8) | 度 | - | 東西格子間隔（等間隔格子の場合） |
| dy_const_deg | real(8) | 度 | - | 南北格子間隔（等間隔格子の場合） |
| file_dxdy_tbox_deg | character | - | - | 不等間隔格子の間隔を与えるファイル |

**依存・注意点**:
- `file_dxdy_tbox_deg` と `dx_const_deg`/`dy_const_deg` は同時指定不可（どちらか一方）。
- 格子点数（nx, ny）はnamelistではなくコンパイル時パラメータで決まる。地形ファイル・
  強制データファイルと格子点数が食い違うと実行時エラーまたはサイレントな異常になる。

### `&nml_vert_grid` (gridm.F90)

鉛直層構成を指定する。

| パラメータ | 型 | 単位 | デフォルト | 説明 |
|---|---|---|---|---|
| file_dz_cm | character | - | - | 層厚を与えるファイル（不等間隔層） |
| dz_const_cm | real(8) | cm | - | 等間隔層厚 |

**依存・注意点**:
- `file_dz_cm` と `dz_const_cm` は同時指定不可。
- 層数（km）はコンパイル時パラメータ。`file_dz_cm` の行数と一致していないとエラー。

### `&nml_topo` (topo.F90)

| パラメータ | 型 | 単位 | デフォルト | 説明 |
|---|---|---|---|---|
| file_topo | character | - | (必須) | 海底地形（水深・陸海マスク）ファイル |

### `&nml_time_step` (time.F90)

| パラメータ | 型 | 単位 | デフォルト | 説明 |
|---|---|---|---|---|
| dt_sec | real(8) | 秒 | (必須) | 運動方程式・トレーサ方程式の基本時間刻み |
| alpha_bryan_1984 | real(8) | - | - | Bryan (1984) のalphaパラメータ |
| l_monitor_time | logical | - | .true. | 標準出力に時間ステップを表示するか |
| l_semi_implicit_coriolis | logical | - | .false. | コリオリ項をsemi-implicitで計算するか |

**依存・注意点**:
- `dt_sec` は水平格子間隔・想定流速からCFL条件を満たすように決める
  （格子を細かくするときは自動的に短くする必要がある）。
- `nml_barotropic_model/dt_barotropic_sec` は通常 `dt_sec` よりかなり小さい値
  （順圧重力波のCFL条件のため）。両者の比が整数になっているか確認する。

### `&nml_exp_start` (time.F90)

実験全体（複数runにまたがる）の開始時刻。

| パラメータ | 型 | デフォルト | 説明 |
|---|---|---|---|
| year | integer(4) | -999 | 年 |
| month | integer(4) | 1 | 月 |
| day | integer(4) | 1 | 日 |
| hour / minute / second | integer(4) | 0 | 時分秒 |

### `&nml_run_ini` (time.F90)

この run（リスタートの1区間）の開始時刻。`nml_exp_start` とは別概念。

```
  1回目run   2回目run   3回目run   4回目run...   （実験全体）
 *---------*---------*---------*-------...  => 時間
 ^                   ^
 exp_start           run_ini（2回目以降の各run開始点）
```

| パラメータ | 型 | デフォルト | 説明 |
|---|---|---|---|
| year / month / day / hour / minute / second | integer(4) | 1/1/1/0/0/0 | このrunの開始時刻 |

**依存・注意点**:
- 初回runでは通常 `nml_exp_start` と同じ値にする。2回目以降のrunではリスタートを
  読み込む時刻に合わせる（間違えるとリスタートの時刻とnamelist上の時刻がずれる）。

### `&nml_run_period` (time.F90)

| パラメータ | 型 | 単位 | デフォルト | 説明 |
|---|---|---|---|---|
| nstep_total | integer(4) | ステップ数 | (必須) | このrunの総タイムステップ数 |

**依存・注意点**:
- 「run期間（年・月）」から `nstep_total` を出すには `dt_sec` との掛け算が必要。
  AIに依頼するときは「〇〇年分」ではなく `dt_sec` と合わせて計算させること
  （閏年・月末日数の扱いを間違えやすいので、リスタート間隔と合わせて検算する）。

### `&nml_run_ini_state` (history.F90)

| パラメータ | 型 | デフォルト | 説明 |
|---|---|---|---|
| l_rst_in | logical | - | `.true.`: リスタートファイルから初期値を読む。`.false.`: 静止状態(u,v,ssh=0)から開始 |

**依存・注意点**:
- `nml_barotropic_run/l_rst_barotropic_in` など個別グループの指定で上書きされる
  （個別指定が優先）。spin-up初回runでは `.false.`、継続runでは `.true.` が典型。

### `&nml_barotropic_model` (surface_grid.F90)

| パラメータ | 型 | 単位 | 説明 |
|---|---|---|---|
| dt_barotropic_sec | real(8) | 秒 | 順圧モードの時間刻み（`dt_sec` より短い） |


詳細: 水平粘性グループ
--------

出典は `README_Namelist.md` と `README_Options.md`（horizontal mixing 節）。
型は README に記載がないため「実数」などと書いている。

関係するオプション（`README_Options.md`）:

| オプション | 内容 | README 上の制約 |
|---|---|---|
| (なし) | ラプラシアン型の水平粘性 | - |
| `BIHARMONIC` | 水平拡散と粘性を倍調和型にする | - |
| `VISBIHARM` | 水平粘性だけ倍調和型にする（`TRCBIHARM` は拡散だけ） | - |
| `SMAGOR` | Smagorinsky 型の粘性 | - |
| `SMAGHD` | 拡散にも Smagorinsky 型を使う | `SMAGOR` と併用 |
| `VIS9P` | 粘性の計算に 9 点を使う（既定は 5 点） | slip側壁、`VISANISO`に必須 |
| `VISANISO` | 非等方粘性 | `VIS9P` と併用 |
| `FSVISC` | 順圧モードに粘性をかける（`&nml_barotropic_visc_horz`） | - |


### `&nml_baroclinic_visc_horz` (clinic_hvis.F90)

| パラメータ | 型 | 単位 | デフォルト | 説明 |
|---|---|---|---|---|
| visc_horz_cm2ps | 実数 | cm²/s | 正値で指定が必須 | ラプラシアン型の水平粘性係数 |
| visc_horz_cm4ps | 実数 | cm⁴/s | 正値で指定が必須 | 倍調和型の水平粘性係数（`BIHARMONIC` か `VISBIHARM` のとき） |
| file_visc_horz_2d | character | - | - | 粘性係数の 2 次元分布を与えるファイル（作成ツールは MXE `prep/MIX/`）。指定すると上の 2 つは無視される |
| slip_factor | 実数 | - | 0.d0 | no-slip: 0.d0、slip: 1.d0（`VIS9P` のときだけ有効） |

**依存・注意点**:
- 単位は cm 系。m²/s から換算するときは 10⁴ 倍、m⁴/s からは 10⁸ 倍する。
- `&nml_grid_size_change_mix_coefs` で `l_grid_size_change_mix_coefs = .true.` にすると、
  格子幅 100 km を基準として、格子サイズに応じて粘性係数が変えられる（`SMAGOR` のときは対象外）。
  格子幅 / 100 km の値が係数に掛けられる。

**係数の目安**（README 由来ではない。海洋モデル一般の目安。中緯度、β ≈ 2×10⁻¹¹ m⁻¹s⁻¹ で計算）:
- 下限その1: Munk 境界層の幅 δ_M = (A/β)^{1/3} が格子 1〜2 点以上になること。δ_M ≳ Δx とすると A ≳ βΔx³。
- 下限その2: 格子レイノルズ数 UΔx/A ≲ 2。渦解像に近い格子では、ラプラシアン型でこれを満たすのは非現実的。
  倍調和型を使う主な理由はこれ。 <!-- TODO: 要出典>
- 上限: 陽解法の安定条件。ラプラシアン型なら A < Δx²/(8Δt)。
- Δx = 10 km の場合の目安:
  - ラプラシアン型: 100〜500 m²/s（`visc_horz_cm2ps = 1.0d6`〜`5.0d6`）
  - 倍調和型: 10⁹〜10¹⁰ m⁴/s（10¹⁷〜10¹⁸ cm⁴/s） <!-- TODO: 要出典>
  - 小さめから始め、西岸境界や格子スケールのノイズを見ながら 3 倍程度ずつ上げる。
- 矩形海の標準値は `visc_horz_cm2ps = 2.5d8`（2.5×10⁴ m²/s）。これは100kmの粗い格子用で、細かい格子にそのまま流用すると大きすぎる。


### `&nml_smagor` (clinic_hvis.F90) — `SMAGOR` のとき

| パラメータ | 型 | 単位 | デフォルト | 説明 |
|---|---|---|---|---|
| smagor_scale | 実数 | 無次元 | README に記載なし | 粘性係数決定用のスケーリング係数 |
| smagor_diff_ratio | 実数 | - | README に記載なし | 粘性係数から拡散係数を決める比（`SMAGHD` のとき有効） |
| l_smagor_nonzero_bg | logical | - | .false. | `.true.` で Smagorinsky 粘性に背景値を足す。背景値は `&nml_baroclinic_visc_horz` で与える |

**依存・注意点**:
- `SMAGOR` と `BIHARMONIC`/`VISBIHARM` は併用できる。(マニュアル Sec.8.3.1)
  - Smagorinsky 粘性により倍調和型の粘性係数が求められる。
  - `l_smagor_nonzero_bg =.true.` とすると `visc_horz_cm4ps` が背景値となる

**係数の目安**
- smagor_scale - Laplacian では 3.0 - 4.0, Bihamonic では 2.0 - 3.0が良いらしいが（Griffies and Hallberg, 2000）、モデルの解像度等に合わせてチューニングをする。(clinic_hvis.F90のコメント)


### `&nml_hvisc_add` (clinic_hvis.F90)

| パラメータ | 型 | 単位 | デフォルト | 説明 |
|---|---|---|---|---|
| l_hvisc_add_harmonic | logical | - | .false. | `.true.` でラプラシアン粘性を追加する |
| file_hvisc_harmonic | character | - | - | 追加するラプラシアン粘性の 2 次元分布 [cm²/s]（T 点） |

**依存・注意点**:
- 重調和型を全域にかけ、西岸や赤道付近など一部だけラプラシアンを足す、といった使い方を想定している。
  ただし、どのオプションとの組み合わせが前提かは README に記載なし（TODO）。


実例（動作実績のあるnamelist本体）
--------

用途別に `sample_ogcm/` 以下へディレクトリを分けて置く（Markdownに埋め込まず、
そのまま `NAMELIST.OGCM` として使えるファイルにしてある）。AIに新しいnamelistを
作らせる際は、まず該当する実例ファイルを読ませて「型」として使うとよい。

* [sample_ogcm/rectangle/NAMELIST.OGCM](sample_ogcm/rectangle/NAMELIST.OGCM) -
  矩形海テストケース（`anl/rectangle/` に対応）。Step 3a の MRICOM-rect と同じ設定で、
  初期値は水温・塩分だけを読む。各パラメータに説明コメント付き。
  ヒストリー出力の `NAMELIST.OGCM.MONITOR` もある。[Step 4](tutorial/04-own-toy.md) で使う。

新しい実例を追加する手順は [sample_ogcm/README.md](sample_ogcm/README.md) を参照。


よくある落とし穴チェックリスト
--------

AIが生成したnamelistをレビューする際、最低限これだけは確認する。

- [ ] `dt_sec` と `dt_barotropic_sec` の比が整数になっているか（CFL条件・時間積分の整合性）
- [ ] `file_dz_cm`/`dz_const_cm`、`file_dxdy_tbox_deg`/`dx_const_deg`+`dy_const_deg` など
      「ファイル指定」と「定数指定」を両方書いていないか（排他）
- [ ] 格子ファイル・地形ファイル・強制データファイルの格子点数（nx, ny, km）が
      コンパイル時設定と一致しているか
- [ ] `nml_run_ini` の日時がリスタートファイルの時刻と一致しているか（継続run時）
- [ ] `nstep_total` は「欲しい期間 ÷ dt_sec」で正しく計算されているか（閏年・月末日数に注意）
- [ ] `&nml_force_data` / `&nml_tracer_data` / `&nml_restart` など繰り返し可能なグループで
      変数の抜け漏れがないか
- [ ] パス指定（`file_*`）が実行ディレクトリからの相対パスとして正しいか
- [ ] 水平粘性係数の種類（`visc_horz_cm2ps` か `visc_horz_cm4ps` か）が `BIHARMONIC`/`VISBIHARM` の有無と合っているか。
      値が格子幅に見合っているか（粗い格子の値の流用に注意）


参照情報
--------

* `~/mricom/docs/README_Namelist.md` — 全namelistグループの一次情報源（`grep -n '^&nml_<name>'` で探す）
* `~/mricom/docs/README_Restart.md` / `README_Monitor.md` — リスタート・出力設定
* [mricom-readme-map.md](mricom-readme-map.md) — 目的別のREADME参照先
* MRICOM-rect の `exp/run/namelist/*.in`・`exp/run/option/*/` — 実際に動くnamelistテンプレートとオプション別の断片
* READMEで確定できない既定値などは、人間がモデル開発者に確認する（AIはソースを読まない）
* `anl/rectangle/` (本リポジトリ) — 矩形海テストケースの解析スクリプト（上記実例の対応先）

<!--
TODO（このファイルの育て方）:
1. （済）対象バージョンを冒頭に明記する
2. 「未」になっているグループから、実際に使うものだけ本体README_Namelist.mdを見て埋めていく
3. 実際に流した実験のnamelistを `sample_ogcm/` 以下に用途別（全球/領域/ALE2層など）で
   ディレクトリを追加していく（`sample_ogcm/README.md` にも一覧を追記する）
4. （済）リポジトリ直下の CLAUDE.md から doc/README.md 経由でこのファイルを案内している
-->
