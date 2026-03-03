#!/usr/bin/env python

confs = [ { 'name':'JRA3q',
            'file':'../../link/data/jra3q/month/2023/nc_phy2m.2023*',
            'kind':'mricom-history',},
          { 'name':'JRA3q',
            'file':'../../link/data/jra3q/month/*/nc_phy2m.*',
            'kind':'mricom-history',},
          { 'name':'JRA3q_clim',
            'file':'../../link/data/jra3q/month/clim.nc',
            'kind':'mricom-history',},
          { 'name':'JRA3q_day',
            'file':'../../link/data/jra3q/day/202*/nc_phy2m.2*',
            'kind':'mricom-history',},]
