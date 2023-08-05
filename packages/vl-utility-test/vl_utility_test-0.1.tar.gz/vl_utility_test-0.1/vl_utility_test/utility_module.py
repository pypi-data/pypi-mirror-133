import os
import sys
import rasterio
import numpy as np
from osgeo import gdal
import glob
import time

def create_rgb(raster_path, rgb_output_path):
	data = rasterio.open(raster_path).read()
	vh_data = data[0,:,:]
	vv_data = data[1,:,:]
	
	#Coeficients
	c1 = 0.001
	c2 = 0.01
	c3 = 0.02
	c4 = 0.03
	c5 = 0.045
	c6 = 0.05
	c7 = 0.9
	c8 = 0.25
	
	#Red Band
	temp_vv_data = vv_data.copy()
	temp_vv_data[temp_vv_data < 0.001] = 0.001
	red_band = c4 + np.log ((c1 - np.log (c6 / (c3 + 50 * temp_vv_data))))
	red_band[temp_vv_data == 1] = 0
	red_band = red_band.reshape((1,data.shape[1],data.shape[2]))

	#Green Band
	green_band = c6 + np.exp (c8 * (np.log (c2 + 2 * vv_data) + np.log (c3 + 5 * vh_data)))
	green_band[vv_data == 1] = 0
	green_band = green_band.reshape((1,data.shape[1],data.shape[2]))

	#Blue Band
	blue_band = 0.5 + np.log((c8 / (c5 + 5 * vv_data)))
	blue_band[vv_data == 1] = 0
	blue_band = blue_band.reshape((1,data.shape[1],data.shape[2]))

	rgb_data  = np.concatenate((red_band, green_band, blue_band), axis = 0)
	
	with rasterio.open(raster_path) as dataset:
		meta_data = dataset.meta
	new_dataset = rasterio.open(
		rgb_output_path,
		'w',
		driver='GTiff',
		height=rgb_data.shape[1],
		width=rgb_data.shape[2],
		count=rgb_data.shape[0],
		dtype=rgb_data.dtype,
		crs=meta_data['crs'],
		transform=meta_data['transform'],
	)
	new_dataset.write(rgb_data)
	new_dataset.close()


def createTiles(in_path, out_path, output_filename, tile_size_x, tile_size_y):
	file = in_path
	ds = gdal.Open(file)
	if(ds != None):
		band = ds.GetRasterBand(1)
		xsize = band.XSize
		ysize = band.YSize

		#tile_size_x = xsize//3
		#tile_size_y = ysize//3
	
		for i in range(0, xsize, tile_size_x):
			for j in range(0, ysize, tile_size_y):
				try:
					#print('*****************************************',out_path)
					#print(str(output_filename) + str(i) + "_" + str(j) + ".tif")
					com_string = "gdal_translate --config GDAL_CACHEMAX 512 -a_nodata 0 -co NUM_THREADS=ALL_CPUS -of GTiff -co BIGTIFF=YES -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + file +" " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
				

					#print(com_string)
					os.system(com_string)
					#transform()		
					tile = gdal.Open(str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif")
					arr = np.array(tile.ReadAsArray())
						
					if(np.count_nonzero(arr) == 0):
						print("Removing Empty File...")
						os.system("rm "+str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif")
						continue

							# command_string = "gdal_translate -of PNG " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif" + " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".png"
							# os.system(command_string)
							# os.system("rm "+str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif")
				except Exception as e:
					print('Gdal error', e)
	#end = time.time()
	#print("Time taken: " + total_time(end - start))
	
	
def generate_ndwi(nir_file,swir_file, output_name):
    swir_link = gdal.Open(swir_file)
    nir_link = gdal.Open(nir_file)
    driver = gdal.GetDriverByName('GTiff')
    swir = swir_link.ReadAsArray().astype(np.float)
    nir = nir_link.ReadAsArray().astype(np.float)
    ndwi_img = ((nir - swir)/(nir + swir))

    # save the raster file
    x_pixels = ndwi_img.shape[1]
    y_pixels = ndwi_img.shape[0]

    ndwi_data = driver.Create(output_name, x_pixels, y_pixels, 1, gdal.GDT_Float32)
    ndwi_data.GetRasterBand(1).WriteArray(ndwi_img)
    geotrans = swir_link.GetGeoTransform()
    proj = swir_link.GetProjection()
    ndwi_data.SetGeoTransform(geotrans)
    ndwi_data.SetProjection(proj)
    ndwi_data.GetRasterBand(1).SetNoDataValue(swir_link.GetRasterBand(1).GetNoDataValue())
    ndwi_data.FlushCache()
    ndwi_data=None
    
    
def merge_layers(input_path, output_path):
	files = os.listdir(input_path)
	df = []
	for filee in files:
		temp = rasterio.open(input_path+filee)
		df.append(temp)

	dest, output_transform = rasterio.merge.merge(df)

	with rasterio.open(input_path+files[0]) as src:
		out_meta = src.meta.copy()    
	out_meta.update({"driver": "GTiff","height": dest.shape[1],"width": dest.shape[2],"compress": "DEFLATE","transform": output_transform})
	with rasterio.open(output_path, "w", **out_meta) as dest1:
		dest1.write(dest)
		

def Compression(raster_path, output_path, nbits):
	if nbits != 'null':
		command = "gdal_translate -of GTiff -co compress=DEFLATE -co BIGTIFF=YES -co NBITS="+str(nbits)+" "+raster_path+" "+output_path
		os.system(command)
	elif nbits == 'null':
		command = "gdal_translate -of GTiff -ot Byte -co TILED=YES -co COMPRESS=JPEG -co PHOTOMETRIC=YCBCR "+raster_path+ " " +output_path
		os.system(command)
	os.system("sudo chmod +777 "+output_path)
	
	
def reproject(raster_path, output_path, projection):
	command = "gdalwarp -t_srs "+projection+" "+raster_path+" " +output_path
	print('Command',command)
	os.system(command)
	

from shapely.geometry import shape, mapping
from shapely.geometry import Polygon
import shapefile
import fiona
from scipy.ndimage import gaussian_filter1d
import numpy as np
from shapely.geometry.multipolygon import MultiPolygon
import os, sys
import rasterio
import geopandas as gpd

def Vectorize(raster_path, output_dir, mitank_id, date, source, projection, sigma):
	command = "gdal_contour -a pixelvalue -i 1 -off 0.1 "+raster_path+" "+output_dir+"temp_"+mitank_id+".shp"
	os.system(command)
	
	shp_schema = {
		'geometry': 'MultiPolygon',
		'properties': {'mitank_id': 'str', 'date': 'str', 'depth': 'int', 'source': 'str'}
	}

	raster_data = rasterio.open(raster_path).read()
	unique_values = np.array(np.unique(raster_data))
	unique_values = unique_values[unique_values>=0]

	new_shp = output_dir+mitank_id+".shp"
	old_shp = shapefile.Reader(output_dir+"temp_"+mitank_id+".shp")
	shapes = old_shp.shapeRecords()

	with fiona.open(new_shp, 'w', 'ESRI Shapefile', shp_schema, projection) as shp:
		for pixel_value in unique_values:
			polygons = []
			for i in range(len(shapes)):
				shp_obj = shapes[i]
				if int(shp_obj.record[1]) == pixel_value:
					coords = np.array(shp_obj.shape.points)
					coords[:,0] = gaussian_filter1d(coords[:,0], sigma)
					coords[:,1] = gaussian_filter1d(coords[:,1], sigma)
					geom = Polygon(coords)
					polygons.append(shape(geom))
			if len(polygons) != 0:
				multipolygon = MultiPolygon(polygons)
				shp.write({
					'geometry': mapping(multipolygon),
					'properties': {'mitank_id': str(mitank_id), 'date': str(date), 'depth': int(pixel_value), 'source': str(source)}
				})
	os.system("rm -r "+output_dir+"temp_"+mitank_id+"*")
	
	
def stack_RGB(red_input_path, green_input_path, blue_input_path, output_path):
	input_files = red_input_path + ' ' + green_input_path + ' ' + blue_input_path
	command = 'gdal_merge.py -of GTiff -ot Byte -seperate -co compress=DEFLATE -o '+output_path+' '+input_files
	print('Command', command)
	os.system(command)
	
	

