日本海の解析
========

HIMSST, MGDSST気候値, MOVE-JPN に対応。

* contour_s.py                     - ある深さの塩分水平分布を描く
* contour_ssh.py                   - SSH分布を描く
* contour_t_section.py             - 水温鉛直断面分布を描く
* contour_t_vel.py                 - 水温分布と流速ベクトルを重ねて描く
* contour_t_vel_section.py         - 水温と流速の鉛直断面分布を重ねて描く
* contour_t_yt.py                  - 水温の緯度・時間ホフメラー図を描く
* contour_t_zt.py                  - 水温の深度・時間ホフメラー図を描く
* contour_v_section.py             - 流速鉛直断面分布を描く
* make_t_3d_ave.py                 - 全層で水温水平平均値の時系列を計算する
* map_brank.py                     - 白地図を描く
* plot_bathymetry.py               - モデルの水深図を描く(地図投影)
* vec_uv.py                        - 流速分布を描く


海面水温解析
--------

* anim_sst.py                      - アニメーション用にSST分布を連番で描く
* contour_sst.py                   - SST分布を描く
* make_sst_ave.py, plot_sst_ave.py - SST水平平均値の時系列を計算する, 描く
* make_sst_trend.py                - MGDSSTの各格子各月の線形トレンドを求める
* plot_sst_trend.py                - ある格子、ある月のSST線形トレンドを描画する


貯熱量と海面熱フラックス
--------

* contour_heat_content.py          - 表層の貯熱量分布を描く
* contour_heatflux.py              - 海面熱フラックス分布を描く
* contour_heatflux_anom.py         - 海面熱フラックス偏差分布を描く
* make_heatflux_month.py           - 海面熱フラックス領域平均値の日別値から月別値の値を計算する
* make_jra3q_ave.py                - JRA-3Qデータの領域平均を計算する
* make_jra3q_clim.py               - JRA-3Qの平年値ファイルを作る
* make_jra3q_seagrid.py            - 日本海のJRA-3Q 陸海グリッドファイルを作る
* plot_heat_budget.py              - 貯熱量の熱収支の時系列を描く
* plot_heatflux_ave.py             - 海面熱フラックス領域平均値の時系列を描く


海洋熱波
--------

* make_heatwave_thres_ave.py       - 海洋熱波しきい値水平平均値の時系列を計算する
* make_heatwave_trend_ave.py       - 海洋熱波しきい値用に、SST水平平均値のトレンド時系列を計算する
* judge_heatwave_ave.py            - SST水平平均値から海洋熱波が起こっているかを判定する
* plot_heatwave_days.py            - 海洋熱波発生日/年の時系列を描く
* plot_heatwave_multiyear.py       - SST水平平均値と海洋熱波発生の時系列を描く
