#!/usr/bin/env python

confs = [ { 'name':'JPNv2',
            'file':'../../link/data/JPN20-assim/hst_mon-jpn/nc_t/20*/nc_t.20*',
            'kind':'mricom-history',},
          { 'name':'MGDSST',
            'file':'../../link/data/netCDF/MGDSST/*/nc_sst.*',
            'kind':'mricom-history',},
          { 'name':'MOVEJPN',
            'file':'../../link/data/netCDF/JPN/month/nc_t.202*',
            'kind':'mricom-history',},
          { 'name':'JPNclim',
            'file':'../../link/data/netCDF/JPN/clim_month/nc_t.2008*',
            'kind':'mricom-history',
            'undef':9.999e20,}]
