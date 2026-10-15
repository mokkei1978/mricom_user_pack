MRICOM-rect の実験手順
========

MRICOM-rect（矩形海パッケージ、MXEと同様の構成）の `exp/` で実験を行う場合の手順（チュートリアル Step 3 用）。
MXE で自作する Step 4 以降の流れは扱わない。
スクリプトは `exp/run/` にあり、統合テスト `exp/test-system/test_exp.sh` が
標準手順の実例になっている（迷ったらこのスクリプトを読む）。

モデル本体の一般的な説明は `~/mricom/README_First.md` の Sec.3（ビルド）・Sec.4（入力データ）・Sec.5（実行）を参照。


全体の流れ
--------

```
 [1] 実験ディレクトリ作成   exp/make_newexp.sh EXPNAME
          ↓
 [2] マシン環境設定         run/setup.sh MACHINE        → config_files/configure.in, run/run.sh を書き換え
          ↓
 [3] オプション追加(任意)   run/change_option.sh MODE   → configure.in, namelist/*.in, run.conf を書き換え
          ↓
 [4] コンパイル             run/compile.sh              → exp/src/ogcm
          ↓
 [5] 実行設定               run/run.conf を編集（期間・時間刻み・出力間隔・初期値）
          ↓
 [6] 初期値リンク           run/link_restart.sh         → exp/restart-main/rs* へのリンク
 [7] 前処理                 run/run_pre.sh              → run/NAMELIST.OGCM, NAMELIST.OGCM.MONITOR, ogcm
          ↓
 [8] 実行                   run/run.sh                  → 最後に run_post.sh が成否を表示
          ↓
 [9] 後処理                 run/mv_log.sh               → ログ・設定一式を run/log/ へ
          ↓
[10] 解析                   本リポジトリの anl/         → hst_*-main/ の出力を描画
```

`setup.sh` と `change_option.sh` は **git管理下のファイルを直接書き換える**。
実験後に元に戻すには `git checkout .`（`exp/` で）を使う。
複数の変更を重ねるときは「マシン設定 → オプション」の順で実行する。


各ステップの詳細
--------

### [1] 実験ディレクトリ作成 (`exp/make_newexp.sh`)

`linkdir/result/EXPNAME/` 以下に出力先を作り、`exp/` からシンボリックリンクを張る。

| リンク | 中身 |
|---|---|
| `exp/restart-main/` | リスタート（初期値の入力・最終状態の出力） |
| `exp/hst_day-main/`, `exp/hst_hour-main/` | ヒストリー出力（日・時間間隔） |
| `exp/run/log/` | ログ置き場 |

ネスティング時は `-sub`, `-bay` も同様に作られる。

### [2]–[3] コンパイル設定 (`config_files/configure.in`)

コンパイル時に決まる設定。**namelistでは変えられない**ので、変えたら再コンパイルが必要。

| 変数 | 意味 |
|---|---|
| `OPTIONS` | モデルオプション（例: `"SPHERICAL QUICKADVEC PARALLEL MPI2"`）。一覧は `README_Options.md` |
| `IMUT`, `JMUT`, `KM` | 格子点数（東西・南北・鉛直） |
| `NPARTX`, `NPARTY` | MPI分割数（`PARALLEL` 時）。実行時プロセス数 = NPARTX×NPARTY |
| `NSFMRGN` | のりしろ格子数（`PARALLEL` 時、≥2。SSH水平拡散が非ゼロなら偶数） |
| `NUMTRC_A`, `NUMTRC_P` | 活性トレーサ数（既定2: 水温・塩分）・パッシブトレーサ数 |
| `MACHINE` or `F90`/`FFLAGS`/... | コンパイラ環境 |

詳細は `README_First.md` Sec.3.1。

`change_option.sh MODE` は `run/option/MODE/setup.sh` を実行し、
`OPTIONS` へのオプション追加と、対応するnamelist断片（例: `option/hflux/hflux.nml`）の
`namelist/NAMELIST-common.in` への追記を行う。引数なしで実行すると利用可能なMODE一覧が出る。
**新しいオプションを試すときは、まず対応する `option/MODE/` があるか確認し、その中身を型にする**のが確実。

### [4] コンパイル (`run/compile.sh`)

`exp/src/` で `./configure && make` を行う。`-r` を付けると `make clean`/`configure` を省いて再make。
失敗したら `MPI2` オプションを外すと通ることがある（`configure.in` のコメントより）。

### [5] 実行設定 (`run/run.conf`)

`run_pre.sh` がこの値を使ってnamelistテンプレートの `@...@` を置換する。

| 変数 | 意味 | namelist への反映 |
|---|---|---|
| `period_day` | 積分日数。**空にするとデバッグ用に12ステップ** | `nml_run_period/nstep_total` = 3600/dt_sec × 24 × period_day |
| `dt_sec` | 基本時間刻み [秒] | `nml_time_step/dt_sec` |
| `dt_barotropic_sec` | 順圧モード時間刻み [秒] | `nml_barotropic_model/dt_barotropic_sec` |
| `initial_main` | 初期値リスタートのディレクトリ（`linkdir/data/` からの相対） | `link_restart.sh` が使う |
| `hst_hour`, `snp_hour` | ヒストリー・スナップショット出力間隔 [時間] | `NAMELIST.OGCM.MONITOR` |
| `monitor_day_main`, `monitor_hour_main` | 出力項目（`run/nml_monitor/hs_*.nml` の `*` 部分を空白区切り） | 同上 |
| `command_exe` | 実行形態（parallel/single/nest_*…）。**手で変えず change_option.sh に任せる** | `run.sh`, `compile.sh` が使う |

リスタート出力間隔は `nstep_total` と同じ（run終了時に1回）に設定される。

namelistの `@...@` 以外の部分（格子・地形・強制・粘性など）を変えたいときは
`run/namelist/NAMELIST-main.in`（モデル固有部分）と `NAMELIST-common.in`（共通部分）を直接編集する。
各グループの意味は [namelist-reference.md](../namelist-reference.md) と `README_Namelist.md`。

### [6]–[7] 初期値リンクと前処理

* `link_restart.sh`: `linkdir/data/${initial_main}/rs*` を `restart-main/` にリンクする。
  ディレクトリが無いとエラー終了。
* `run_pre.sh`: `NAMELIST-main.in` + `NAMELIST-common.in` を連結・置換して `NAMELIST.OGCM` を、
  `nml_monitor/add_NAMELIST.sh` で `NAMELIST.OGCM.MONITOR` を作り、`../src/ogcm` をコピーする。
  `configure.in` に `NETCDF` があると出力ファイル名の接頭辞が `nc_`、なければ `hs_` になる。

### [8] 実行 (`run/run.sh`)

`command_exe` に応じて `mpirun -np 4 ./ogcm` などを実行し、最後に `run_post.sh` が成否を判定する:

* **成功**: `restart-main/rs_ssh.*` が非空で存在し、`rs_ssh-fail*` が無い → `EXP succeed.`
* **失敗**: 上記以外 → `EXP fail.`（`rs_ssh-fail*` は異常終了時に出力されるものと思われる <!-- TODO: 要確認 -->）

標準出力は `nml_stdout` の設定により `OGCM-<file_base_stdout>-stdout.0000` などのファイルに出る。
体積保存の確認例: `grep "zos (#snap" OGCM-19010101-stdout.0000` の値がほぼゼロならよい。

### [9] 後処理 (`run/mv_log.sh`)

`configure.in`、`run.conf`、`run.sh`、`NAMELIST.*`、標準出力などを `run/log/` へ移す。
MRI.COMのバージョン（ChangeLog先頭行）も `log/conf.txt` に記録される。
**実験の再現に必要な情報はすべて `log/` に残る**ので、実験結果と一緒に保存しておく。

### [10] 解析

出力は `exp/hst_day-main/` などに入る（実体は `linkdir/result/EXPNAME/`）。
本リポジトリでは `link/data` → `/data01/sakamoto` を通してアクセスし、
`lib/mricom.py` の `open_history()`（netCDF）/ `open_grads()`（GrADS ctl）で xarray として読む。
描画スクリプトは `anl/<対象>/` にある（`anl/README.md`）。
出力変数の名前と意味は `README_Monitor.md` の "Available outputs"。


継続run（リスタートからの再開）
--------

長期積分は「run」を繰り返してつなぐ。`nml_exp_start`（実験全体の開始）は固定し、
各runの開始時刻 `nml_run_ini` と初期値リスタートを前runの終了時点に合わせる。

1. 前runの `restart-main/` に出力されたリスタート（`rs_*.YYYYMMDDhhmmss` 形式）を確認する
2. `NAMELIST-common.in` の `&nml_run_ini` を前runの終了時刻に書き換える
3. `&nml_run_ini_state/l_rst_in = .true.` を確認する
4. 前runのリスタートが `restart-main/` から読める状態にする（`initial_main` の切り替えまたはリンク）。
   読まれるのは `rs_*.` + `nml_run_ini` の日時のファイル
5. 初回に `.false.` にしてある `l_rst_LFAM3_in`, `l_rst_vmix_in`, `l_rst_barotropic_dflx_in` を `.true.` にする
   （忘れても走るが、通しrunと一致しない）

MRICOM-rect のスクリプトには継続runの自動化が無い。手で行う手順（新しい実験名で前runのリスタートにリンクを張る、
`l_rst_LFAM3_in`/`l_rst_vmix_in`/`l_rst_barotropic_dflx_in` を `.true.` にする）と、
通しrunとのビット一致の確認は [03-rectangle.md](03-rectangle.md) の 3c を参照（2026-10-04 確認）。

リスタートの入出力方式（`read_method`/`write_method`、ノード別ファイルなど）と
必須変数の一覧は `README_Restart.md` を参照。
「X/Y diffusion flux for ssh」のリスタートが無い場合は
`nml_barotropic_run/l_rst_barotropic_dflx_in = .false.` にする（`README_Restart.md` より。
MRICOM-rect のテンプレートはこの設定になっている）。
