Step 2: 実行環境の構築と確認
========

**目標**: Fortran コンパイラ・MPI・ライブラリが MRI.COM / MXE の要求どおりに動くことを確かめる。

**前提**: [Step 1](01-get.md) で MRICOM-rect を取得済み。


確認するもの
--------

| 項目 | 確認方法 | 参照 |
|---|---|---|
| Fortran コンパイラ | `gfortran --version` | `README_First.md` Sec.3.1（`F90`, `FFLAGS`） |
| MPI | `mpif90 --version`, `mpirun --version` | 同上（`INCLUDES`） |
| netCDF（任意） | `nf-config --version`（netCDF-Fortran） | `setting/README-MXE.md`（`MXE_NETCDF`） |
| MXE ツール用ビルド設定 | `Setup.sh` → `setting/macros.make` が作られる | `setting/README-MXE.md`, `setting/machine/` |
| MXE ライブラリ | `lib/` で `make` | `README-MXE.md` |
| Fortran の動作テスト | `fortran/` の各テスト（eos, mpiio, nml, openmp など） | `fortran/README-MXE.md` |
| Python 解析環境 | 下記「Python 解析環境」のライブラリが import できる | 本リポジトリ |

<!-- TODO: fortran/ のどのテストを、どの順で、何が出れば合格とするかを決める -->


Python 解析環境
--------

本リポジトリの `lib/mricom.py` と `anl/` のスクリプト用。venv や conda で 1 つ環境を作っておく。

| ライブラリ | 用途 | 動作実績 |
|---|---|---|
| numpy | 配列計算 | 2.3.5 |
| xarray | データを Dataset として扱う（`lib/mricom.py`） | 2025.12.0 |
| dask | `xr.open_mfdataset()`（`open_history()`）に必要 | 2025.11.0 |
| netCDF4 | netCDF 形式ヒストリーの読み込み（xarray のバックエンド） | 1.7.2 |
| xgrads | GrADS 形式（`.ctl`）の読み込み（`open_grads()`） | 0.2.7 |
| matplotlib | 描画 | 3.10.7 |
| cartopy | 地図投影・海岸線（`anl/` のほぼ全スクリプト） | 0.25.0 |
| docopt | スクリプトの引数解析（`anl/` のほぼ全スクリプト） | 0.6.2 |
| pandas | 時系列処理（`anl/japan_sea`, `transport` など一部） | 2.3.3 |
| cmocean | 海洋用カラーマップ（`anl/japan_sea` など一部） | 4.0.3 |

動作実績は Python 3.13.5。作り方の例（venv の場合）:

```bash
python3 -m venv ~/venv
source ~/venv/bin/activate
pip install numpy xarray dask netCDF4 xgrads matplotlib cartopy docopt pandas cmocean
```

確認:

```bash
source ~/venv/bin/activate
python -c "import numpy, xarray, dask, netCDF4, xgrads, matplotlib, cartopy, docopt, pandas, cmocean; print('ok')"
```

* cartopy は初回の描画で Natural Earth の海岸線データをダウンロードする（ネットワークが必要）。


Docker を使う場合
--------

ローカル環境の構築で詰まったら、テストマシンと同じ Docker + Debian + gfortran (MPI) 環境を使える。
MRICOM-rect の `docker/README.md`、mxe-docker の README を参照。


完了の確認
--------

* [ ] `setting/macros.make` が作られ、`lib/` の make が通る
* [ ] `fortran/` のテストが通る
* [ ] Python 解析環境の import 確認が `ok` になる
* [ ] MPI で 4 プロセス程度の並列実行ができる（[Step 3a](03-rectangle.md) の `run.sh` が `mpirun -np 4` で回れば OK）

動作実績（2026-10-04, Debian 13）: gfortran 14.2.0、Open MPI 5.0.7、netCDF-Fortran 4.5.4 で Step 3a が通った。Python は上表のライブラリを入れた venv で Step 3b が描けた。


よくあるトラブル
--------

<!-- 経験したら追記 -->
