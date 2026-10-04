Step 3: 矩形海モデルを動かす（MRICOM-rect をそのまま使う）
========

**目標**: 取得した MRICOM-rect を変更せずに動かし、結果を見て、
設定を少しずつ変えたときの応答を体験する。

**前提**: [Step 2](02-environment.md) の環境確認が済んでいる。

手順の詳細は [rect_workflow.md](rect_workflow.md)（`exp/run/` の各スクリプト）を参照。


3a. そのまま回す
--------

手順は統合テスト `exp/test-system/test_exp.sh` の中身と同じ（コメント付きで読みやすいので一読するとよい）。

```bash
# (最初に 1 回) リポジトリ直下で Setup.sh を実行し setting/macros.make を作る
cd ~/rect/exp
sh clean.sh                  # 前回の作業ファイルを掃除
sh make_newexp.sh test3a     # 実験名 test3a。linkdir/result/test3a/ に出力先を作りリンクを張る
cd run
sh setup.sh docker           # 一般の Linux + gfortran + Open MPI ならこれ（下記）
sh compile.sh                # ../src/ogcm ができる
# run.conf を確認（最初は既定のまま: 10 日、dt=3600 秒、初期値 main.23）
sh link_restart.sh
sh run_pre.sh
sh run.sh                    # 最後に "EXP succeed."
sh mv_log.sh                 # 標準出力などを log/ へ
```

* マシン設定名は `run/machine/` 以下から選ぶ。`docker` は `MACHINE=linux86-gfortran`、
  `FFLAGS="-mcmodel=large -fconvert=big-endian -O3 -fopenmp"` を `configure.in` に追記し、
  `mpirun -np 4`（OpenMP 2 スレッド）で実行する。Docker 外の普通の Linux でもそのまま使える。
  `gfortran` は気象研内サーバ用（`MACHINE=mri-ogsv009-gfortran`）。
* 実験名を毎回変えれば過去の結果を上書きしない。
* 実績（2026-10-04, 4 コア, gfortran 14.2.0, Open MPI 5.0.7）: `compile.sh` 約 30 秒、10 日積分（240 step）約 10 秒。

**完了の確認**:

* [ ] `EXP succeed.` が出る
* [ ] 標準出力で体積保存がほぼゼロ:
  `grep "zos (#snap" log/OGCM-19010101-stdout.0000 | tail -3` → `1e-15 [cm]` 程度
* [ ] 同じ設定で 2 回実行し、リスタートがビット一致する（md5sumを用いたハッシュ値チェック）:
  ```bash
  cd ~/rect/exp
  find restart-main/ -type f -name 'rs_*' | sort | xargs md5sum > md5_run1.txt
  # run/ で link_restart.sh → run_pre.sh → run.sh をもう一度
  md5sum -c md5_run1.txt
  ```
  (`exp/test-system/`にある`md5sum.txt` は気象研究所内の開発に用いられる。ユーザーは使わない。)


3b. 結果を見る
--------

* 出力（`hst_*-main/`）を本リポジトリの `lib/mricom.py`（`open_history()` / `open_grads()`）で読み、
  `anl/` のスクリプトで描画する。
* 出力変数の意味は `README_Monitor.md` の "Available outputs"を参照。
* 標準設定のヒストリーは GrADS 形式（`hs_*.ctl` + `hs_*.1901`）。日平均が `hst_day-main/` に出る
  （例: `hs_ssh` = `zos` [cm]、`hs_t` = `thetao`、`hs_u`/`hs_v` = `uo`/`vo`、`hs_sfc_um`/`hs_sfc_vm` = 鉛直積分速度 `um`/`vm` [cm^2/s]、`hs_wind` = `tauuo`/`tauvo`。
  格子は 62×52、10 層）。

最終10日目の SSH と速度ベクトルを描画する。まず鉛直積分した速度、次に第 1 層の速度を見る。

```bash
source ~/venv/bin/activate      # xarray, xgrads, cartopy, docopt を入れた Python 環境
cd ~/mricom_user_pack/anl/rectangle
D=../../link/data/rectangle/result/test3a/hst_day-main
python contour_ssh_um_grads.py  $D 1901-01-10 test3a   # (1) SSH + 鉛直積分速度（hs_sfc_um/vm）→ temp.png
python contour_ssh_vel_grads.py $D 1901-01-10 test3a   # (2) SSH + 第 1 層（10 m）の速度（hs_u/v）→ temp.png
```

出力はどちらも `temp.png`（上書きされる）なので、1 枚ずつ見る。

1. **鉛直積分速度**: 南の亜熱帯循環（SSH 正、最大 +4 cm 程度、時計回り）と
   北の亜寒帯循環（負、最小 −6 cm 程度、反時計回り）の二重ジャイア。
   どちらも西岸に強化され、流れは SSH の等値線に沿う（地衡流）。
2. **第 1 層の速度**: ジャイヤではなく、東西に一様な南北流の帯が目立つ
   （10°N 付近で北向き約 16 cm/s、35°N 付近で南向き約 6 cm/s）。
   風応力は東西成分のみ（南で東風、中緯度で西風）なので、これは風に直交する表層エクマン流で、
   大きさも τ/(ρ f h) の見積もり（10.5°N、20 m 厚の層で約 15 cm/s）と合う。
   第 1 層の矢印が SSH と合わないのは誤りではない。

* `open_grads()` は GrADS の UNDEF（-9.99E+33、陸格子）を NaN にして返す。
* `anl/rectangle/` の他のスクリプト（`contour_ssh.py` など）は netCDF 出力（`nc_*`）を前提にしている。
  標準設定の出力をそのまま読むには `*_grads.py` を使うか、同じように `open_grads()` に書き換える。

**完了の確認**:
* [ ] SSH と鉛直積分速度の図で、西岸強化した二重ジャイアが見える
* [ ] 第 1 層の速度がエクマン流でジャイアと向きが違う理由を説明できる


3c. 継続実験（リスタートからの再開）
--------

長期積分は run を繰り返してつなぐ。3a の `test3a`（1/1〜1/10）の続きとして 1/11〜1/20 を回し、
最初から 20 日間通して回した場合とビット一致することを確かめる。

継続 run は **新しい実験名** (test3cとする)で行い、前 run のリスタートにリンクを張る。
同じ実験名のまま回すと、ヒストリー（年ごとのファイル `hs_*.1901`）と
`run/mv_log.sh` で移すログ（ファイル名が `OGCM-19010101-stdout.*` のまま）が前 run の分を上書きする。

```bash
cd ~/rect/exp
sh clean.sh
sh make_newexp.sh test3c
ln -s ~/rect/linkdir/result/test3a/restart-main/rs_*.19010111000000 restart-main/
```

namelist テンプレートを 4 か所変える（`link_restart.sh` は使わない）:

| ファイル | 設定 | 初回 (3a) | 継続 |
|---|---|---|---|
| `NAMELIST-common.in` | `&nml_run_ini` の `day` | `1` | `11`（前 run の終了時刻） |
| `NAMELIST-common.in` | `&nml_run_ini_state/l_rst_LFAM3_in` | `.false.` | `.true.` |
| `NAMELIST-common.in` | `&nml_vmix_run/l_rst_vmix_in` | `.false.` | `.true.` |
| `NAMELIST-main.in` | `&nml_barotropic_run/l_rst_barotropic_dflx_in` | `.false.` | `.true.` |

* `&nml_exp_start`（実験全体の開始日 1901/1/1）は変えない。`run.conf` の `period_day=10` もそのまま。
* 読み込むリスタートは `rs_*.` + `nml_run_ini` の日時（ここでは `rs_t.19010111000000` など）。
  標準出力の `Open  ../restart-main/rs_t.19010111000000` で確かめられる。
* 初回の値が `.false.` なのは、初期値 `main.23` に前ステップ値（LFAM3）・鉛直混合係数・SSH 拡散フラックスの
  リスタートが無いため（意味は `README_Restart.md` "Standard namelists"）。3a の run はこれらを出力しているので、
  継続では `.true.` にして読む。
* 強制は定常（`interval = -999`）なので `&nml_force_data` の `ifstart` は変えなくてよい。
* test3aとディレクトリを変えずに実験して
  ヒストリー出力を上書きしないためには、`run_pre.sh`で生成される
  NAMELIST.OGCM.MONITORの `suffix`を`'day'`とするか削除する(デフォルトは'day')。
* 標準ログ出力を上書きしないためには、`file_base_stdout` を`'19010121'`とする

```bash
cd run
sh run_pre.sh
sh run.sh                    # EXP succeed.
sh mv_log.sh
cd ..
git checkout -- run/namelist # テンプレートを初回の設定に戻す
```

**比較用に 20 日間通して回す**: テンプレートは初回のまま、`run.conf` を `period_day=20` にして
実験名 `test3a-20d` で 3a と同じ手順を踏む。終わったら両者の 1/21 0:00 のリスタートを比べる:

```bash
cd ~/rect/linkdir/result
for f in test3a-20d/restart-main/rs_*.19010121000000; do
  cmp -s $f test3c/restart-main/$(basename $f) && echo "same $f" || echo "DIFF $f"
done
```

* `nml_run_ini` だけ変え、3 つのフラグを `.false.` のままにした継続 run → `EXP succeed.` になるが
  結果は一致しない。
  **エラーにならないので、フラグの戻し忘れに気づきにくい**。

**完了の確認**:
* [ ] 継続 run `test3c` が前 run のリスタート（`*.19010111000000`）を読んで `EXP succeed.` になる
* [ ] 通し run `test3a-20d` と 1/21 のリスタートがビット一致する


3d. 設定を変えてみる
--------

1 回に 1 つだけ変え、3b と同じ図で比較する。

| 変える場所 | 例 | 再コンパイル |
|---|---|---|
| `run/run.conf` | 積分期間 `period_day`、時間刻み `dt_sec`、出力間隔 | 不要 |
| `run/namelist/NAMELIST-*.in` | 粘性・拡散係数、風応力 | 不要 |
| `run/change_option.sh MODE` | オプション追加（例: hflux） | 必要 |
| `config_files/configure.in` | 格子数、MPI 分割 | 必要（入力データも作り直し → Step 4） |

`run.conf`や`NAMELIST-*.in`を変えた場合は、`run_pre.sh`の再実行が必要。
namelist を編集するときは [../namelist-reference.md](../namelist-reference.md) と
[../namelist-examples/rectangle/](../namelist-examples/rectangle/README.md) を参照する。

**完了の確認**:
* [ ] パラメータ変更前後の違いを図で説明できる


落とし穴
--------

* `setup.sh` は `config_files/configure.in*` を書き換える。
  実験後に元に戻すなら `git checkout -- config_files`。
* `setup.sh`/`change_option.sh` を何度も実行すると、`OPTIONS` やnamelist断片が**重複して追記**される。
  やり直すときは `git checkout .` で戻してから実行し直す。
* 格子点数（`IMUT`/`JMUT`/`KM`）はコンパイル時設定。地形・層厚・強制データのサイズと一致させる。
  層厚ファイルの `km` と `KM` が食い違うとエラー。
* MPI分割数 `NPARTX×NPARTY` と `run.sh` の `mpirun -np` を一致させる。
* `period_day` を空にするとデバッグ用の12ステップ積分になる（出力間隔も1ステップ単位になる）。
* 単位系は基本的に **cgs**（cm, g, s）。ただし海氷・海面フラックスなど一部の表層過程は **MKS**
  （`README_First.md` Sec.2.2）。パラメータ名の接尾辞（`_cm`, `_cm2ps`, `_sec`, `_deg`）で単位を確認する。
* `exp/test.sh`（全オプションの統合テスト）は気象研究所での開発用。使わない。


AIへの頼み方（例）
--------

```
doc/tutorial/03-rectangle.md と doc/tutorial/rect_workflow.md を読んで、矩形海実験を dt=1800秒・30日間で
回すために run.conf と namelist のどこを変えればよいか教えて。
```
