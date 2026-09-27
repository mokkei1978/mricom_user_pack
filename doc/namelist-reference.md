MRI.COM Namelist リファレンス（雛形）
========

MRI.COMの実行に必要なNamelist（`NAMELIST.OGCM`）作成をAIに手伝ってもらうための参照ドキュメント。
人間が読むためだけでなく、Claude等のAIアシスタントに読ませて
「妥当なnamelistを提案させる／レビューさせる」ことを主目的とする。

対象バージョン: MRI.COM 開発版（`~/mricom`, 2026年5月時点）の `docs/README_Namelist.md` に基づく。

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
| `nml_baroclinic_visc_horz` | 傾圧粘性（水平） | 未 |
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


実例（動作実績のあるnamelist本体）
--------

用途別に `namelist-examples/` 以下へディレクトリを分けて置く（Markdownに埋め込まず、
そのまま `NAMELIST.OGCM` として使えるファイルにしてある）。AIに新しいnamelistを
作らせる際は、まず該当する実例ファイルを読ませて「型」として使うとよい。

* [namelist-examples/rectangle/NAMELIST.OGCM](namelist-examples/rectangle/NAMELIST.OGCM) -
  矩形海テストケース（`anl/rectangle/` に対応）の最小構成。一部の付随ファイル・
  繰り返しグループは省略。

新しい実例を追加する手順は [namelist-examples/README.md](namelist-examples/README.md) を参照。


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


参照情報
--------

* `~/mricom/docs/README_Namelist.md` — 全namelistグループの一次情報源（`grep -n '^&nml_<name>'` で探す）
* `~/mricom/docs/README_Restart.md` / `README_Monitor.md` — リスタート・出力設定
* [mricom-readme-map.md](mricom-readme-map.md) — 目的別のREADME参照先
* myrect の `exp/run/namelist/*.in`・`exp/run/option/*/` — 実際に動くnamelistテンプレートとオプション別の断片
* READMEで確定できない既定値などは、人間がモデル開発者に確認する（AIはソースを読まない）
* `anl/rectangle/` (本リポジトリ) — 矩形海テストケースの解析スクリプト（上記実例の対応先）

<!--
TODO（このファイルの育て方）:
1. （済）対象バージョンを冒頭に明記する
2. 「未」になっているグループから、実際に使うものだけ本体README_Namelist.mdを見て埋めていく
3. 実際に流した実験のnamelistを `namelist-examples/` 以下に用途別（全球/領域/ALE2層など）で
   ディレクトリを追加していく（`namelist-examples/README.md` にも一覧を追記する）
4. （済）リポジトリ直下の CLAUDE.md から doc/README.md 経由でこのファイルを案内している
-->
