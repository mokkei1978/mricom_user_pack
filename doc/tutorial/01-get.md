Step 1: MRI.COM・MXE・MRICOM-rect の取得
========

**目標**: 以降のステップで使うパッケージとデータを手元にそろえる。

**前提**: [Step 0](00-about.md) で MRI.COM / MXE / MRICOM-rect の関係を把握している。


何を取得するか
--------

対象バージョンは **MRI.COM 5.4**。

| もの | 使うステップ | 入手先 |
|---|---|---|
| MRICOM-rect（矩形海パッケージ、MRI.COM 同梱） | 3 | https://github.com/mri-ocean/MRICOM-rect （要申請） |
| 矩形海の入力データ | 3 | `git clone https://github.com/mokkei1978/rectangle_data.git`（MRICOM-rect の `README.md`） |
| MXE | 4, 5 | https://github.com/mri-ocean/MXE （要申請） |
| MRI.COM 本体 | 4, 5 | https://github.com/mri-ocean/MRICOM （要申請） |
| 本リポジトリ | 3〜5（解析） | <!-- TODO: 要確認 --> |
| （任意）mxe-docker | 2 | https://github.com/mokkei1978/mxe-docker （Docker で環境を作る場合） |

Step 3 までは MRICOM-rect と入力データだけで進められる。


### 利用申請

MRICOM, MXE, MRICOM-rect の各リポジトリは非公開で、利用には次の 2 つが必要:

1. 気象研究所への書類申請
2. GitHub への登録

<!-- TODO: 要確認。申請書類の入手先・提出先（MRI.COM web page の該当ページ）、所要日数 -->

申請が通るまでの間は [Step 0](00-about.md) の公開マニュアルを読み進めておくとよい。


### バージョンをそろえる

<!-- TODO: 要確認。5.4 に対応するタグ・ブランチ名と、MRICOM-rect 同梱の MRI.COM（開発版）との関係。
     Step 4 で MRICOM-rect の結果を再現するには、MRI.COM・MXE・MRICOM-rect の版の組み合わせをそろえる必要がある -->


ディレクトリ配置の例
--------

<!-- TODO: 推奨配置を決める。clone 先のディレクトリ名は任意
     （作者環境: MRICOM → ~/mricom, MRICOM-rect → ~/myrect, ~/rectangle_data, ~/mxe-docker） -->


完了の確認
--------

* [ ] MRICOM-rect の `README.md` が読める（申請が通り clone できた）
* [ ] 入力データディレクトリに `dz_cm.d`, `topo.d`, `rs_t.*`, `rs_s.*` などがある


よくあるトラブル
--------

<!-- 経験したら追記 -->
