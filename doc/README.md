MRI.COM 実験ドキュメント集（AI支援用）
========

MRI.COMを使った実験を、Claude等のAIアシスタントの助けを借りて進めるためのドキュメント集。
人間向けの手引きであると同時に、AIに読ませて「正しい文脈で手伝わせる」ことを目的とする。


情報源のルール（最重要）
--------

* **MRI.COMモデル本体のソースコードはAIに読ませない。** AIが参照してよいのはREADME類のみ。
  * 可: `~/mricom/README_First.md`, `~/mricom/docs/README_*.md`
  * 不可: `src/`, `samples/` 以下, `tools/`, `ChangeLog*` など README 以外すべて
    （`~/myrect/exp/MRICOM/`, `~/myrect/exp/src*/`, `~/myrect/exp/modsrc/` のコピーも同様）
  * `.claude/settings.json` に Read の deny ルールを設定済み。
    ただしBash経由（`cat`, `grep` など）は防げないので、AIへの依頼時も注意すること。
* rectangleパッケージ（`~/myrect`）の本体以外の部分（`exp/run/` のスクリプト、`run.conf`、
  namelistテンプレート、`nml_monitor/`）は参照してよい。
* READMEに書かれていないこと（デフォルト値の詳細など）をAIが推測で埋めてはいけない。
  不明点は「不明」と明示させ、人間がモデル開発者・ソースで確認する。


目次
--------

| ファイル | 内容 | いつ読ませるか |
|---|---|---|
| [workflow.md](workflow.md) | 実験の全体手順（myrect の `exp/run/` を基準に、設定→コンパイル→実行→継続→後処理） | 新しい実験を立ち上げるとき、実行で詰まったとき |
| [mricom-readme-map.md](mricom-readme-map.md) | 「何を知りたいか → MRI.COMのどのREADMEの何節を見るか」の対応表 | 常に。AIが一次情報を探す起点 |
| [input-data.md](input-data.md) | 入力データ（格子・地形・強制・レストア）のファイル形式と単位 | 前処理（`prep/`）で入力ファイルを作るとき |
| [namelist-reference.md](namelist-reference.md) | `NAMELIST.OGCM` の主要グループの解説とレビュー用チェックリスト | namelistを作る／レビューするとき |
| [namelist-examples/](namelist-examples/README.md) | 動作実績のあるnamelistの実例 | namelistを作るときの「型」として |


AIへの頼み方（例）
--------

リポジトリのルートで Claude Code を起動すると `CLAUDE.md` 経由でこのファイルが案内される。
明示的に頼む場合の例:

```
doc/README.md と doc/workflow.md を読んで、矩形海実験を dt=1800秒・30日間で
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


ドキュメントの育て方
--------

* 実験で詰まった点・分かった点は、該当ファイルの「落とし穴」節に1行でも追記する。
  AIの回答精度はここに書かれた経験の量で決まる。
* 実際に流した実験のnamelistは `namelist-examples/` に用途別に追加する。
* 新しいファイルを足したら、この目次とリポジトリ直下の `CLAUDE.md` を更新する。
* 未確認の記述には `<!-- TODO: 要確認 -->` を付け、確認できたら外す。
