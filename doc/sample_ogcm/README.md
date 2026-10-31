MRI.COM 設定例
========

MRI.COM の実験に使う設定ファイル（`configure.in`, `NAMELIST.OGCM` など）の例。
`../namelist-reference.md` や `../tutorial/` から参照される。


configure.in
--------

`configure.in` の一部分。組み合わせて使う（`cat` でつなげる。[Step 4c](../tutorial/04-own-toy.md)）。

* ビルド設定（コンパイラ・MPI）。`configure.in` の末尾に加える（[Step 2](../tutorial/02-environment.md)）
  * [configure.in-gfortran-openmpi-noomp](configure.in-gfortran-openmpi-noomp) - gfortran + Open MPI
  * [configure.in-gfortran-openmpi](configure.in-gfortran-openmpi) - gfortran + Open MPI + OpenMP
* モデル設定（オプション・格子数・MPI 分割数）。各実例のディレクトリに置く
  * [rectangle/configure.in](rectangle/configure.in) - 矩形海（MRICOM-rect の標準設定と同じ）


namelist 実例
--------

動作実績のある namelist（`NAMELIST.OGCM` など）の実例を、用途別にディレクトリを分けて置く。

* [rectangle](rectangle/README.md) - 矩形海テストケース（MRICOM-rect の標準設定と同じ。説明コメント付き。Step 4 で使う）


ディレクトリの増やし方
--------

用途ごとに1ディレクトリ（例: `global/`, `ale2layer/`, `forajpn/`）を作り、
実際に流した設定を元にした `NAMELIST.OGCM`（必要なら `NAMELIST.OGCM.MONITOR`, モデル設定の `configure.in`）と、
簡単な説明の `README.md` を置く。
追加したら `namelist-reference.md` の実例一覧にもリンクを足す。
