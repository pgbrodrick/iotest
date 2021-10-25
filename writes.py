from osgeo import gdal
from spectral.io import envi
import numpy as np
import rasterio as rio
import netCDF4 as nc
import os


def write_geotiff(dat, output_file, options):
    driver = gdal.GetDriverByName("GTiff")
    outDataset = driver.Create(output_file, dat.shape[1], dat.shape[0], dat.shape[2], gdal.GDT_Float32, options=options)
    for _b in range(dat.shape[2]):
        outDataset.GetRasterBand(_b+1).WriteArray(dat[...,_b])
    dat = None
    return outDataset


def write_cog(dat, output_file, options):
    outDataset = write_geotiff(dat, output_file, options)
    outDataset.BuildOverviews("NEAREST", [2,4,8,16,32,64,128,256])

    driver = gdal.GetDriverByName("GTiff")
    output_options = options + ['COPY_SRC_OVERVIEWS=YES']
    ds2 = driver.CreateCopy(output_file + 'cog', outDataset, options=output_options)
    del outDataset, ds2
    return

def write_netcdf(dat, output_file, complevel, chunkshape):
    outDataset = nc.Dataset(output_file, 'w', clobber=True, format='NETCDF4')
    dim_names = ['y','x','z']
    for _d, dn in enumerate(dim_names):
        outDataset.createDimension(dn, dat.shape[_d])

    var = outDataset.createVariable(os.path.basename(output_file), 'f4', dimensions=dim_names, zlib=complevel > 0,
                              complevel=complevel, chunksizes=chunkshape, fill_value=-9999)
    var[...] = dat
    outDataset.sync()