Step 4: MXE で矩形海モデルを自作する
========

**目標**: MXE の前処理ツールを使い、Step 3 の MRICOM-rect と同じ設定を自分で一から作って再現する。
再現できたら、格子・地形・強制を変えた自分のトイモデルに発展させる。

**前提**: [Step 3](03-rectangle.md) を終え、MRICOM-rect の結果（入力ファイル・出力）が手元にある。
MXE を取得し（[Step 1](01-get.md)）、`lib/` をコンパイル済み（[Step 2](02-environment.md)）。


4a. rectangle と同じ入力データを作る
--------

MXE の `prep/rectangle/README.md` の手順に従う。

| 生成物 | ツール | 確認 |
|---|---|---|
| 鉛直層厚 `dz_cm.d` | `prep/DZ/`（`make_dz.sh`） | rectangle_data の同名ファイルと `cmp` |
| グリッド設定 `NAMELIST.MXE` | `prep/rectangle/`（`NAMELIST.MXE-main`、`sample/NAMELIST.MXE`） | |
| 地形 `topo.d` | `prep/rectangle/make_topo.sh` | `cmp` |
| 風応力 `wind.d` | `prep/rectangle/make_wind.sh` | `cmp` |
| 初期値 `rs_t.*`, `rs_s.*` | `prep/rectangle/make_restart.sh` | `cmp` |
| `configure.in`, `NAMELIST.OGCM` | `prep/rectangle/sample/` を型に作成 | MRICOM-rect の `run/log/` に残したものと差分 |

入力ファイルの形式・単位は [../input-data.md](../input-data.md)。

<!-- TODO: 要確認。rectangle_data のどのディレクトリ（main.NN）が rectangle の標準設定に対応するか -->


4b. MXE の exp/ で実験を立ち上げて再現を確かめる
--------

1. MXE の `exp/` で実験ディレクトリを作り、4a の `configure.in` と入力データを使う
2. `NAMELIST.OGCM` は [../namelist-reference.md](../namelist-reference.md) を見ながら自分で書く
   （AI に下書きさせてもよい。下の頼み方の例）
3. Step 3 と同じ期間を回し、結果を比べる

**完了の確認**:
* [ ] 4a の入力ファイルが rectangle_data と一致する（一致しない場合は差の理由を説明できる）
* [ ] リスタート出力が Step 3 と一致する（`md5sum`）<!-- TODO: 要確認。MRICOM-rect 同梱は v5.5、MXE で使う MRI.COM は 5.4 なので、ビット一致を期待できるか。
     できない場合は何を比べて「再現できた」とするか（コンパイラ・MPI分割をそろえる条件も） -->


4c. 自分のトイモデルにする
--------

1 つずつ変えて、そのたびに 4b の手順で動作を確かめる。

1. 格子数・領域（`configure.in` の `IMUT`/`JMUT`/`KM` と `NAMELIST.MXE`、入力データを一緒に変える）
2. 地形（海嶺、陸棚、湾など。`prep/rectangle/` の `kida-ridge`, `shelf`, `bay` などが例）
3. 強制（風応力の形、熱フラックス `make_hflux.sh`）
4. 鉛直座標・層数（例: ALE 2層 `2layer-slope`。本リポジトリに描画ツールあり）

<!-- TODO: 推奨する例題（二重ジャイヤ、周期水路など）と、それぞれ見るべき結果 -->


落とし穴
--------

* 格子数（`configure.in`）と入力データ・`NAMELIST.MXE`・`NAMELIST.OGCM` のサイズが食い違う
  （[03-rectangle.md](03-rectangle.md)「落とし穴」）

<!-- 経験したら追記 -->


AIへの頼み方（例）
--------

```
doc/namelist-reference.md と doc/namelist-examples/rectangle/NAMELIST.OGCM を型にして、
格子を東西 2 倍にした矩形海実験の configure.in と NAMELIST.OGCM の変更点を挙げて。
不明なパラメータは ~/mricom/docs/README_Namelist.md で確認し、
そこにも書かれていなければ推測せず TODO として残すこと。
```
