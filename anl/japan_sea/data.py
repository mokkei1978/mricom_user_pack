#!/usr/bin/env python

confs = [ { 'name':'HIMSST',
            'file':'../../link/data/netCDF/HIMSST/20??/nc_sst.2*',
#            'file':'../../link/data/netCDF/HIMSST/202?/nc_sst.2*',
            'kind':'mricom-history',
            'undef':999.,},
          { 'name':'MGDSSTnorm',
            'file':'../../link/data/netCDF/MGDSST/norm/nc_sst.2004*',
            'kind':'mricom-history',},
          { 'name':'JPNv2',
            'file':'../../link/data/JPN20-assim/hst_day-jpn/nc_t/2019/nc_t.2019*',
            'kind':'mricom-history',},]
