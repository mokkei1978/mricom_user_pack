矩形海テストケース
========

`anl/rectangle/` が対象とする矩形海モデル（62×52×10）の namelist。
[Step 4](../../tutorial/04-own-toy.md) で、MXE で作った入力データから MRICOM-rect の標準設定（Step 3a）を再現するのに使う。
MRI.COM 5_4 で動作を確認（2026-10）。各パラメータに説明のコメントを付けてある（説明は MRI.COM の README による）。
新しい namelist を AI に作らせる際の「型」として、このファイルをそのまま読ませるとよい。

* `NAMELIST.OGCM` - Step 3a で MRICOM-rect が使った `NAMELIST.OGCM`（`exp/run/log/`）を次のように変えたもの
  * 初期値として水温・塩分（`rs_t`, `rs_s`）だけを読む（`l_rst_in = .false.` と `&nml_tracer_run` の `l_rst_tracer_in = .true.`）。
    速度・SSH はゼロ、鉛直混合は一様値から始まる。
  * リスタートの入出力先を `../restart-main/` から `../restart/` に変えた。
  * 説明のコメントを加え、グループを内容ごとに並べ替えた（値は同じ）。
* `NAMELIST.OGCM.MONITOR` - ヒストリー出力。水温・塩分・流速（東西・南北）・SSH・鉛直積分した流量（東西・南北）の日平均だけ（`interval_step = -2`）を `../hst_day/` に出す。
  Step 3a（`log/NAMELIST.OGCM.MONITOR`）の同じ 7 つの出力とデータはビット一致する（`.ctl` の時間軸は違う）。
* `configure.in` - モデル設定（オプション・格子数・MPI 分割数）。Step 3a の `log/configure.in` からモデル設定だけを抜き出したもの。
  ビルド設定（[../configure.in-gfortran-openmpi-noomp](../configure.in-gfortran-openmpi-noomp) など）を末尾に加えて使う（Step 4c）。
