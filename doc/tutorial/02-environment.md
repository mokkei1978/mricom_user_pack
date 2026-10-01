Step 2: 実行環境の構築と確認
========

**目標**: Fortran コンパイラ・MPI・ライブラリが MRI.COM / MXE の要求どおりに動くことを確かめる。

**前提**: [Step 1](01-get.md) で MRICOM-rect を取得済み。


確認するもの
--------

| 項目 | 確認方法 | 参照 |
|---|---|---|
| Fortran コンパイラ | <!-- TODO --> | `README_First.md` Sec.3.1（`F90`, `FFLAGS`） |
| MPI | <!-- TODO --> | 同上（`INCLUDES`） |
| netCDF（任意） | <!-- TODO --> | `setting/README-MXE.md`（`MXE_NETCDF`） |
| MXE ツール用ビルド設定 | `Setup.sh` → `setting/macros.make` が作られる | `setting/README-MXE.md`, `setting/machine/` |
| MXE ライブラリ | `lib/` で `make` | `README-MXE.md` |
| Fortran の動作テスト | `fortran/` の各テスト（eos, mpiio, nml, openmp など） | `fortran/README-MXE.md` |
| Python 解析環境 | xarray 等の import、本リポジトリの `lib/mricom.py` | 本リポジトリ |

<!-- TODO: fortran/ のどのテストを、どの順で、何が出れば合格とするかを決める -->


Docker を使う場合
--------

ローカル環境の構築で詰まったら、テストマシンと同じ Docker + Debian + gfortran (MPI) 環境を使える。
MRICOM-rect の `docker/README.md`、mxe-docker の README を参照。


完了の確認
--------

* [ ] `setting/macros.make` が作られ、`lib/` の make が通る
* [ ] `fortran/` のテストが通る
* [ ] MPI で 4 プロセス程度の並列実行ができる <!-- TODO: 確認方法 -->


よくあるトラブル
--------

<!-- 経験したら追記 -->
