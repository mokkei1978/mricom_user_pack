#!/usr/bin/env python

confs = [ { 'name':'HIMSST',
            'file':'../../link/data/netCDF/HIMSST/2024/nc_sst.2*',
            'kind':'mricom-history',
            'undef':999.,},
          { 'name':'MGDSSTnorm',
            'file':'../../link/data/netCDF/MGDSST/norm/nc_sst.2004*',
            'kind':'mricom-history',}, ]
