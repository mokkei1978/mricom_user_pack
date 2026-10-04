Step 3: 矩形海モデルを動かす（MRICOM-rect をそのまま使う）
========

**目標**: 取得した MRICOM-rect を変更せずに動かし、結果を見て、
設定を少しずつ変えたときの応答を体験する。

**前提**: [Step 2](02-environment.md) の環境確認が済んでいる。

手順の詳細は [../workflow.md](../workflow.md)（`exp/run/` の各スクリプト）を参照。


3a. そのまま回す
--------

手順は統合テスト `exp/test-system/test_exp.sh` の中身と同じ（コメント付きで読みやすいので一読するとよい）。

```bash
# (最初に 1 回) リポジトリ直下で Setup.sh を実行し setting/macros.make を作る
cd ~/rect/exp
sh clean.sh                  # 前回の作業ファイルを掃除
sh make_newexp.sh tut3       # 実験名 tut3。linkdir/result/tut3/ に出力先を作りリンクを張る
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
D=../../link/data/rectangle/result/tut3/hst_day-main
python contour_ssh_um_grads.py  $D 1901-01-10 tut3   # (1) SSH + 鉛直積分速度（hs_sfc_um/vm）→ temp.png
python contour_ssh_vel_grads.py $D 1901-01-10 tut3   # (2) SSH + 第 1 層（10 m）の速度（hs_u/v）→ temp.png
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


3c. 設定を変えてみる
--------

1 回に 1 つだけ変え、3b と同じ図で比較する。

| 変える場所 | 例 | 再コンパイル |
|---|---|---|
| `run/run.conf` | 積分期間 `period_day`、時間刻み `dt_sec`、出力間隔 | 不要 |
| `run/namelist/NAMELIST-*.in` | 粘性・拡散係数、風応力 | 不要 |
| `run/change_option.sh MODE` | オプション追加（例: hflux） | 必要 |
| `config_files/configure.in` | 格子数、MPI 分割 | 必要（入力データも作り直し → Step 4） |

namelist を編集するときは [../namelist-reference.md](../namelist-reference.md) と
[../namelist-examples/rectangle/](../namelist-examples/rectangle/README.md) を参照する。

最後に継続 run（リスタートからの再開）を 1 回行う（[../workflow.md](../workflow.md)「継続run」）。

**完了の確認**:
* [ ] パラメータ変更前後の違いを図で説明できる
* [ ] 継続 run がつながる


よくあるトラブル
--------

[../workflow.md](../workflow.md) の「落とし穴」を参照。新しく見つけたらそちらへ追記する。

* `exp/test.sh`（全オプションの統合テスト）は各テスト後に `exp/` で `git checkout .` を実行する。
  `exp/` 以下の未コミットの編集（`run.conf`、namelist など）が消えるので、作業中のコピーでは使わない。
* `setup.sh` は `config_files/configure.in*` を書き換える（`docker` は追記）。
  実験後に元に戻すなら `git checkout -- config_files`。


AIへの頼み方（例）
--------

```
doc/tutorial/03-rectangle.md と doc/workflow.md を読んで、矩形海実験を dt=1800秒・30日間で
回すために run.conf と namelist のどこを変えればよいか教えて。
```
