#!/usr/bin/env python
'''線形トレンドの増加率を月毎にプロットする
'''

import numpy as np
import matplotlib.pyplot as plt

value=np.array([0.00982972, 0.01162976, 0.01281047, 0.0160385,  0.02171918, 0.02783453,
 0.03317427, 0.05438747, 0.02545231, 0.02571126, 0.02418869, 0.0092918 ]) * 10.

fig, ax = plt.subplots()
ax.bar(range(1,13),value)
ax.set_title( '1991-2020 SST linear trend (Japan Sea)' )
ax.set_ylabel('K / 10 years',fontsize='large')
ax.set_xlabel('month',fontsize='large')
ax.set_xticks(range(1,13))
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
plt.grid(axis='y')
plt.savefig('temp.png', bbox_inches='tight')

