


import argparse
import time
from reads import gdal_line_by_line_read, gdal_full_read, envi_full_read, rio_full_read, envi_full_read_return, netcdf_full_read
from writes import write_geotiff, write_cog, write_netcdf
import logging
import numpy as np
import os

def timefunc(function, name, function_args):
    st = time.perf_counter()
    function(*function_args)
    et = time.perf_counter()

    print(f'{name} completed in: {np.round(et - st,2)} s')




def main():

    parser = argparse.ArgumentParser(description='Compare read/write speads in different formats')
    parser.add_argument('input_file', type=str)
    parser.add_argument('scratch_dir', type=str)
    args = parser.parse_args()

    print('\n\nENVI Reads and Writes\n\n')
    timefunc(gdal_line_by_line_read, 'GDAL Line by Line Read', {args.input_file})
    timefunc(gdal_full_read, 'GDAL Full Read', {args.input_file})
    timefunc(envi_full_read, 'ENVI Full Read', {args.input_file})
    timefunc(rio_full_read, (args.input_file), 'RasterIO Full Read')

    #dat = envi_full_read_return(args.input_file)
    #print('\n\nGeotiff Reads and Writes\n\n')
    #timefunc(write_geotiff, 'Geotiff Write - Basic', (dat, os.path.join(args.scratch_dir, 'geotiff_basic.tif'), []))
    #timefunc(gdal_line_by_line_read, 'GDAL Line by Line Read', {os.path.join(args.scratch_dir, 'geotiff_basic.tif')})
    #timefunc(gdal_full_read, 'GDAL Full Read', {os.path.join(args.scratch_dir, 'geotiff_basic.tif')})
    #print('\n')
    #timefunc(write_geotiff, 'Geotiff Write - Tiled', (dat, os.path.join(args.scratch_dir, 'geotiff_t.tif'), ['TILED=YES']))
    #timefunc(gdal_line_by_line_read, 'GDAL Line by Line Read', {os.path.join(args.scratch_dir, 'geotiff_t.tif')})
    #timefunc(gdal_full_read, 'GDAL Full Read', {os.path.join(args.scratch_dir, 'geotiff_t.tif')})
    #print('\n')
    #timefunc(write_geotiff, 'Geotiff Write - Tiled, LZW', (dat, os.path.join(args.scratch_dir, 'geotiff_tc.tif'), ['TILED=YES', 'COMPRESS=LZW']))
    #timefunc(gdal_line_by_line_read, 'GDAL Line by Line Read', {os.path.join(args.scratch_dir, 'geotiff_tc.tif')})
    #timefunc(gdal_full_read, 'GDAL Full Read', {os.path.join(args.scratch_dir, 'geotiff_tc.tif')})

    #print('\n\nCOG Reads and Writes\n\n')
    #timefunc(write_cog, 'COG Write - Tiled, LZW', (dat, os.path.join(args.scratch_dir, 'geotiff_cog.tif'), ['TILED=YES', 'COMPRESS=LZW']))
    #timefunc(gdal_line_by_line_read, 'GDAL Line by Line Read', {os.path.join(args.scratch_dir, 'geotiff_cog.tifcog')})
    #timefunc(gdal_full_read, 'GDAL Full Read', {os.path.join(args.scratch_dir, 'geotiff_cog.tifcog')})

    dat = envi_full_read_return(args.input_file)
    print('\n\nNETCDF Reads and Writes\n\n')
    #timefunc(write_netcdf, 'NETCDF Write - Uncompressed', (dat, os.path.join(args.scratch_dir, 'netcdf.cf'), 0, None))
    #timefunc(netcdf_full_read, 'NETCDF Full Read', {os.path.join(args.scratch_dir, 'netcdf.cf')})

    for complevel in range(0,9):
        fname = os.path.join(args.scratch_dir, f'netcdf_c{complevel}.cf')
        timefunc(write_netcdf, 'NETCDF Write - Compressed', (dat, fname, complevel, None))
        timefunc(netcdf_full_read, 'NETCDF Full Read', {fname})



if __name__ == '__main__':
    main()