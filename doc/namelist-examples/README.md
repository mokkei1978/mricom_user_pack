Namelist実例集
========

動作実績のあるNamelist（`NAMELIST.OGCM`）の実例を、用途別にディレクトリを分けて置く。
`../namelist-reference.md` から参照される。


内容
--------

* [rectangle](rectangle/README.md) - 矩形海テストケース（最小構成）


ディレクトリの増やし方
--------

用途ごとに1ディレクトリ（例: `global/`, `ale2layer/`, `forajpn/`）を作り、
実際に流した設定を元にした `NAMELIST.OGCM` と、簡単な説明の `README.md` を置く。
追加したら `namelist-reference.md` の実例一覧にもリンクを足す。
