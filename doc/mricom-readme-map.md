MRI.COM README 対応表
========

「何を知りたいか」から「MRI.COMのどのREADMEのどこを見るか」を引くための表。
AIはまずここで参照先を決め、該当READMEの該当節だけを読むこと（READMEは合計8000行超あり、全部読む必要はない）。

* README の場所: `~/mricom/README_First.md`, `~/mricom/docs/README_*.md`
  （myrect 内のコピー `~/myrect/exp/MRICOM/docs/` は myrect 同梱版。実験に使うバージョンの方を見る）
* **README 以外（`src/` など）は参照禁止**（[README.md](README.md) の「情報源のルール」）。
* 行番号はバージョンで変わるので、節名や `grep -n '^&nml_xxx' README_Namelist.md` のような検索キーで探す。


目的別の参照先
--------

### 実験の設定・ビルド

| 知りたいこと | 参照先 | 検索キー・節 |
|---|---|---|
| `configure.in` に書く項目（IMUT, KM, NPARTX…） | `README_First.md` | Sec.3.1 "Configuration of the model" |
| あるオプション（`HFLUX`, `ICE` など）の意味・依存関係 | `README_Options.md` | 冒頭のアルファベット順一覧 → オプション名で検索 |
| オプションに伴って必要になるnamelist | `README_Options.md` の各項目 + `README_Namelist.md` "Optional namelists" | `#### <OPTION> chosen` |
| 削除されたオプション・機能（古い設定の移行） | `README_DeletedFeatures.md` | |
| ソースのディレクトリ構成（どのパッケージが何を担当するか） | `README_First.md` Sec.2.2 / `README_Tree.md` | ※ディレクトリ名の把握まで。ソース本体は読まない |

### Namelist

| 知りたいこと | 参照先 | 検索キー・節 |
|---|---|---|
| 全namelistグループの一覧 | `README_Namelist.md` | 冒頭 "Contents" |
| 必須グループ（格子・時間・初期状態・混合係数など） | `README_Namelist.md` | "Required namelists" 節 |
| オプション依存のグループ | `README_Namelist.md` | "Optional namelists" 節の `#### <OPTION> chosen` |
| 個々のグループの変数・単位・既定値 | `README_Namelist.md` | `grep -n '^&nml_<name>'`（Contents と本文の2か所にヒットする。本文側を読む） |
| 本リポジトリでの要約・実例・レビュー観点 | [namelist-reference.md](namelist-reference.md), [namelist-examples/](namelist-examples/README.md) | |

### 入力データ

| 知りたいこと | 参照先 | 検索キー・節 |
|---|---|---|
| 層厚・水平格子・地形・スケールファクタのファイル形式 | `README_First.md` | Sec.4.1–4.3 |
| トレーサのナッジング（レストア）用データ | `README_First.md` Sec.4.4 + `README_Namelist.md` `&nml_tracer_data` | |
| 海面強制（風・放射・気温・降水・河川・海氷密接度）の要素名 | `README_First.md` | Sec.4.5（`name = 'U-wind'` など） |
| 強制データの時間間隔・内挿方法の指定 | `README_Namelist.md` | `&nml_force_data` |
| 海面フラックス・大気要素の扱い（単位・符号） | `README_Surfflux.md` | |
| 背景鉛直拡散の鉛直分布ファイル | `README_First.md` | Sec.4.6 |
| 本リポジトリでの要約 | [input-data.md](input-data.md) | |

### 出力・リスタート

| 知りたいこと | 参照先 | 検索キー・節 |
|---|---|---|
| ヒストリー出力の指定（`NAMELIST.OGCM.MONITOR` の `&nml_history`） | `README_Monitor.md` | "New style" → "Namelist specification" |
| 出力できる変数名の一覧 | `README_Monitor.md` | "Available outputs"（カテゴリ別に `####` 見出し） |
| NetCDF / MPI-IO 出力の設定 | `README_Monitor.md` | "Common settings" 以下 |
| リスタートの指定（`&nml_restart`）と入出力方式 | `README_Restart.md` | "Namelist specification" |
| リスタートに必須の変数 / オプション別に追加で必要な変数 | `README_Restart.md` | "Required variables", "Optional variables", `### <OPTION> chosen` |
| 初期状態の選択（静止状態から or リスタートから） | `README_Restart.md` | "Standard namelists" の `&nml_run_ini_state` |

### その他

| 知りたいこと | 参照先 |
|---|---|
| 粒子追跡（`PARTICLE`） | `README_Particle.md` |
| 開発者向けの内部ルーチン（出力間隔の上書きなど） | `README_Advanced.md` |


READMEに答えが無いとき
--------

1. このドキュメント集（特に各ファイルの「落とし穴」）と `namelist-examples/` を確認する。
2. myrect の `exp/run/option/<MODE>/`（オプション別の設定例）や `exp/run/namelist/*.in` を確認する。
3. それでも無ければ、AIは推測で埋めずに「READMEに記載なし」と報告する。
   人間がモデル開発者に確認し、分かったことをこのドキュメント集に追記する。
