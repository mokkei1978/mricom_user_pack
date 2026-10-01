Step 5: 独自のモデルを作る
========

**目標**: 実地形・実データを使った領域モデルや全球モデルを、必要な要素を自分で選んで組み立てる。

**前提**: [Step 4](04-own-toy.md) で MXE を使って入力データ・設定を一から作れるようになっている。

このステップは一本道の手順ではなく、必要な要素と参照先の道案内とする。


必要な要素と参照先
--------

| 要素 | MXE のツール | MRI.COM の README / マニュアル |
|---|---|---|
| 格子（一般直交座標、tripolar など） | `prep/global-tripolar/`, `prep/regional/`, `prep/closed_basin/` | `README_First.md` Sec.4.1、技術報告第87号 |
| 現実地形 | `prep/TOPO/` | `README_First.md` Sec.4.2 |
| 初期値・レストア（気候値） | `prep/TRACER/`, `prep/restore/`, `prep/refdata/` | `README_First.md` Sec.4.4 |
| 海面強制（バルク式、大気データ） | `prep/FORCE/` | `README_Surfflux.md` |
| 河川 | `prep/rivermouth/`, `prep/river/` | `README_First.md` Sec.4.5.5 |
| 潮汐 | `prep/TIDE/` | `README_Options.md`, `README_Namelist.md` |
| 粘性・拡散係数 | `prep/MIX/` | `README_Namelist.md` |
| ネスティング | `prep/nest/`, `prep/offnestsub/` | `README_Options.md`, `README_Namelist.md`（開境界条件は README に記載なし） |
| モニター出力 | `prep/MONITOR/` | `README_Monitor.md` |

目的別の README 参照先は [../mricom-readme-map.md](../mricom-readme-map.md) も参照。


本リポジトリの実例
--------

<!-- TODO: 実例を追加していく -->
* 全球の年平均風応力の強制ファイル作成（`prep/`, refs #29）
* FORA-JPN 北太平洋モデル結果の SSH 描画（`anl/`, refs #30）


AI の支援範囲
--------

* AI は README 類と公開マニュアルに基づいて、設定・namelist・入力データ作成を手伝う。
* **モデル本体のソースを改造する作業（`modsrc/`）は AI の支援範囲外。** 人間がソースとモデル開発者に確認して行う。
