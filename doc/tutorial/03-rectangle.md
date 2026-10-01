Step 3: 矩形海モデルを動かす（MRICOM-rect をそのまま使う）
========

**目標**: 取得した MRICOM-rect を変更せずに動かし、結果を見て、
設定を少しずつ変えたときの応答を体験する。

**前提**: [Step 2](02-environment.md) の環境確認が済んでいる。

手順の詳細は [../workflow.md](../workflow.md)（`exp/run/` の各スクリプト）を参照。


3a. そのまま回す
--------

1. `Setup.sh` でマシン環境を設定
2. `exp/make_newexp.sh` で実験ディレクトリを作る
3. `run/setup.sh MACHINE` → `run/compile.sh`
4. `run/run.conf` を確認（最初は既定のまま）
5. `run/link_restart.sh` → `run/run_pre.sh` → `run/run.sh`
6. `EXP succeed.` を確認し、`run/mv_log.sh`

**完了の確認**:
* [ ] `EXP succeed.` が出る
* [ ] 標準出力で体積保存（`zos (#snap`）がほぼゼロ
* [ ] <!-- TODO: 要確認。exp/test-system/md5sum.txt の参照値とリスタートが一致するか確かめる手順 -->


3b. 結果を見る
--------

* 出力（`hst_*-main/`）を本リポジトリの `lib/mricom.py`（`open_history()` / `open_grads()`）で読み、
  `anl/` のスクリプトで描画する。
* 出力変数の意味は `README_Monitor.md` の "Available outputs"。

<!-- TODO: 矩形海の標準結果として何を描くか（SSH、表層流速、水温断面など）と対応する anl/ スクリプト -->

**完了の確認**:
* [ ] SSH の水平分布図が描ける（西岸強化した循環が見える） <!-- TODO: 要確認 -->


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


AIへの頼み方（例）
--------

```
doc/tutorial/03-rectangle.md と doc/workflow.md を読んで、矩形海実験を dt=1800秒・30日間で
回すために run.conf と namelist のどこを変えればよいか教えて。
```
