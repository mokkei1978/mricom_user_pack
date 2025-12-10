日本海の解析
========

HIMSST, MGDSST気候値, MOVE-JPN に対応。

* anim_sst.py                      - アニメーション用にSST分布を連番で描く
* contour_heat_content.py          - 表層の貯熱量分布を描く
* contour_heatflux.py              - 海面熱フラックス分布を描く
* contour_heatflux_anom.py         - 海面熱フラックス偏差分布を描く
* contour_s.py                     - ある深さの塩分水平分布を描く
* contour_ssh.py                   - SSH分布を描く
* contour_sst.py                   - SST分布を描く
* contour_t_section.py             - 水温鉛直断面分布を描く
* contour_t_vel.py                 - 水温分布と流速ベクトルを重ねて描く
* contour_t_yt.py                  - 水温の緯度・時間ホフメラー図を描く
* contour_t_zt.py                  - 水温の深度・時間ホフメラー図を描く
* make_jra3q_ave.py                - JRA-3Qデータの領域平均を計算する
* make_jra3q_clim.py               - JRA-3Qの平年値ファイルを作る
* make_jra3q_seagrid.py            - 日本海のJRA-3Q 陸海グリッドファイルを作る
* make_sst_ave.py, plot_sst_ave.py - SST水平平均値の時系列を計算する, 描く
* make_strait_transport_netcdf.py  - MXEで計算した海峡通過流量を1つのnetCDFファイルにまとめる
* make_t_3d_ave.py                 - 全層で水温水平平均値の時系列を計算する
* map_brank.py                     - 白地図を描く
* plot_bathymetry.py               - モデルの水深図を描く(地図投影)
* plot_heatflux_ave.py             - 海面熱フラックス領域平均値の時系列を描く
* plot_strait_transport.py         - 海峡通過流量の時系列を描く
* vec_uv.py                        - 流速分布を描く
