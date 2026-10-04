MRI.COM チュートリアル
========

MRI.COM に習熟するためのチュートリアルと、実験時に引くリファレンス集。
人間向けの手引きであると同時に、Claude 等の AI に読ませて「正しい文脈で手伝わせる」ことを目的とする。
namelist 作成支援もこの一部として、各ステップからリファレンスを参照する。


情報源のルール（最重要）
--------

* **MRI.COMモデル本体のソースコードはAIに読ませない。** AIが参照してよいのはREADME類のみ。
  * 可: `~/mricom/README_First.md`, `~/mricom/docs/README_*.md`
  * 可: 公開マニュアル [気象研究所技術報告第87号](https://www.mri-jma.go.jp/Publish/Technical/DATA/VOL_87/index.html)（MRI.COM v5.0 対応。食い違うときは `docs/README_*.md` を優先）
  * 不可: `src/`, `samples/` 以下, `tools/`, `ChangeLog*` など README 以外すべて
    （MRICOM-rect・MXE 内の `exp/MRICOM/`, `exp/src*/`, `exp/modsrc/` のコピーも同様）
  * `.claude/settings.json` に Read の deny ルールを設定済み。
    ただしBash経由（`cat`, `grep` など）は防げないので、AIへの依頼時も注意すること。
* MRICOM-rect（矩形海パッケージ）の本体以外の部分（`exp/run/` のスクリプト、`run.conf`、
  namelistテンプレート、`nml_monitor/`）は参照してよい。
* READMEに書かれていないこと（デフォルト値の詳細など）をAIが推測で埋めてはいけない。
  不明点は「不明」と明示させ、人間がモデル開発者・ソースで確認する。


チュートリアル `tutorial/`
--------

順番に進める。各ステップに「目標・前提・手順・完了の確認・落とし穴・AIへの頼み方」を書く。

| ステップ | 内容 |
|---|---|
| [0. MRI.COM とは](tutorial/00-about.md) | 概要、公開マニュアル（技術報告第87号）と README 類、MRI.COM / MXE / rectangle の関係 |
| [1. 取得](tutorial/01-get.md) | MRI.COM・MXE・MRICOM-rect（要申請）と入力データの取得 |
| [2. 実行環境](tutorial/02-environment.md) | コンパイラ・MPI・`macros.make`・MXE の Fortran テスト・Python 環境 |
| [3. 矩形海を動かす](tutorial/03-rectangle.md) | MRICOM-rect をそのまま実行 → 結果を描画 → 設定を1つずつ変える・継続run |
| [4. 矩形海を自作する](tutorial/04-own-toy.md) | MXE の前処理で MRICOM-rect と同じ設定を一から作って再現 → 自分のトイモデルへ |
| [5. 独自モデル](tutorial/05-own-model.md) | 実地形・実データのモデルに必要な要素と参照先（道案内） |

補足: [tutorial/rect_workflow.md](tutorial/rect_workflow.md) — MRICOM-rect の実験手順（`exp/run/` のスクリプトで設定→コンパイル→実行→継続→後処理）。Step 3 の詳細版。


リファレンス
--------

| ファイル | 内容 | いつ読ませるか |
|---|---|---|
| [mricom-readme-map.md](mricom-readme-map.md) | 「何を知りたいか → MRI.COMのどのREADMEの何節を見るか」の対応表 | 常に。AIが一次情報を探す起点 |
| [input-data.md](input-data.md) | 入力データ（格子・地形・強制・レストア）のファイル形式と単位 | 前処理（`prep/`）で入力ファイルを作るとき |
| [namelist-reference.md](namelist-reference.md) | `NAMELIST.OGCM` の主要グループの解説とレビュー用チェックリスト | namelistを作る／レビューするとき |
| [namelist-examples/](namelist-examples/README.md) | 動作実績のあるnamelistの実例 | namelistを作るときの「型」として |


AIへの頼み方（例）
--------

リポジトリのルートで Claude Code を起動すると `CLAUDE.md` 経由でこのファイルが案内される。
明示的に頼む場合の例:

```
doc/README.md と doc/tutorial/rect_workflow.md を読んで、矩形海実験を dt=1800秒・30日間で
回すために run.conf と namelist のどこを変えればよいか教えて。
```

```
doc/namelist-reference.md と doc/namelist-examples/rectangle/NAMELIST.OGCM を型にして、
HFLUX オプションを加えた実験の NAMELIST.OGCM を作って。
不明なパラメータは ~/mricom/docs/README_Namelist.md で確認し、
そこにも書かれていなければ推測せず TODO として残すこと。
```

AIが作ったnamelistや設定は、**投入前に必ず人間がレビューする**。
誤設定はクラッシュより「エラーなく走るが物理的に不正な結果」になりやすい
（単位の取り違え、CFL条件違反、格子数の不整合など）。


ドキュメントの編集方針
--------

* 実験で詰まった点・分かった点は、該当ファイルに1行でも追記する。
  AIの回答精度はここに書かれた経験の量で決まる。節は内容で分ける:
  * 「落とし穴」— 設定時に避けるべきミス。エラーにならずに結果がおかしくなるものを含む
    （例: 継続runでリスタート読み込みフラグを戻し忘れても `EXP succeed.` になる）。
  * 「トラブルシューティング」— エラーメッセージへの対応。「症状（メッセージ）→ 原因 → 対処」の形で書く。
    該当する記述が出てきたら、その時点で節を作る。
* 実際に流した実験のnamelistは `namelist-examples/` に用途別に追加する。
* 新しいファイルを足したら、この目次とリポジトリ直下の `CLAUDE.md` を更新する。
* 未確認の記述には `<!-- TODO: 要確認 -->` を付け、確認できたら外す。
