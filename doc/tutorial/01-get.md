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
| 矩形海の入力データ（rectangle_data） | 3 | `git clone https://github.com/mokkei1978/rectangle_data.git`（公開。MRICOM-rect の `README.md` に記載） |
| MXE | 4, 5 | https://github.com/mri-ocean/MXE （要申請） |
| MRI.COM 本体 | 4, 5 | https://github.com/mri-ocean/MRICOM （要申請） |
| 本リポジトリ（mricom_user_pack） | 3〜5（解析） | `git clone https://github.com/mokkei1978/mricom_user_pack.git`（公開） |
| （任意）mxe-docker | 2 | https://github.com/mokkei1978/mxe-docker （Docker で環境を作る場合） |

Step 3 までは MRICOM-rect と入力データだけで進められる。


### 利用申請

MRICOM, MXE, MRICOM-rect の各リポジトリは非公開で、利用には次の 2 つが必要:

1. 気象研究所への書類申請
2. GitHub への登録

申請書類は [MRI.COM web page](https://mri-ocean.github.io/mricom/) から入手でき、送付先のメールアドレスも同ページに記載されている。
了承までには数日かかる。

申請が通るまでの間は [Step 0](00-about.md) の公開マニュアルを読み進めておくとよい。


### バージョンをそろえる

* MRI.COM 5.4 はリポジトリ MRICOM のブランチ `5_4`。clone 後に `git checkout 5_4` する。
* MRICOM-rect に同梱の MRI.COM は最新の開発版（v5.5）。5.4 と少し異なるが、ほぼ同じ。

Step 3（MRICOM-rect）は同梱の v5.5、Step 4 以降（MXE）は手元の 5.4 で動かすことになる。
Step 4 で Step 3 の結果と比べるときは、この版の違いを念頭に置く。


ディレクトリ配置の例
--------

配置は自由に決めてよい。ただし次を推奨する。

* **ソースコードのリポジトリ**（MRICOM, MXE, MRICOM-rect, mricom_user_pack）は home の下に置く（直下でなくてよい）。
* **入力データ**（rectangle_data など）は外部ディスクに置く。

配置の例（本チュートリアルではソースをこの名前で書く。自分の配置に読み替えること）:

```
~/mricom                        MRICOM（ブランチ 5_4）
~/mxe                           MXE
~/rect                          MRICOM-rect
~/mricom_user_pack              本リポジトリ（mricom_user_pack）
~/mxe-docker                    mxe-docker（任意）
<外部ディスク>/rectangle_data   矩形海の入力データ
```


完了の確認
--------

* [ ] MRICOM-rect の `README.md` が読める（申請が通り clone できた）
* [ ] 入力データディレクトリに `dz_cm.d`, `topo.d`, `rs_t.*`, `rs_s.*` などがある


落とし穴
--------

<!-- 経験したら追記 -->
