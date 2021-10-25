
from osgeo import gdal
from spectral.io import envi
import numpy as np
import rasterio as rio
import netCDF4 as nc
import os



def gdal_line_by_line_read(input_file):
    ds = gdal.Open(input_file, gdal.GA_ReadOnly)
    dat = np.zeros((ds.RasterYSize, ds.RasterXSize, ds.RasterCount))

    for _l in range(ds.RasterYSize):
        dat[_l,...] = np.squeeze(ds.ReadAsArray(0, _l, ds.RasterXSize, 1)).transpose()

    return


def gdal_full_read(input_file):
    ds = gdal.Open(input_file, gdal.GA_ReadOnly)
    dat = ds.ReadAsArray()

    return


def envi_full_read(input_file):
    ds = envi.open(input_file + '.hdr', gdal.GA_ReadOnly)
    dat = ds.open_memmap(interleave='bip').copy()

    return


def envi_full_read_return(input_file):
    ds = envi.open(input_file + '.hdr', gdal.GA_ReadOnly)
    dat = ds.open_memmap(interleave='bip').copy()

    return dat

def rio_full_read(input_file):
    ds = rio.open(input_file)
    dat = ds.read()

    return

def netcdf_full_read(input_file):
    ds = nc.Dataset(input_file)
    dat = np.array(ds[os.path.basename(input_file)])

    return

