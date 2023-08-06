from typing import Union

from localtileserver.client import TileClient
from localtileserver.tileserver import get_data_path, get_pine_gulch_url, get_sf_bay_url


def get_blue_marble(port: Union[int, str] = "default", debug: bool = False):
    path = get_data_path("frmt_wms_bluemarble_s3_tms.xml")
    return TileClient(path, port=port, debug=debug)


def get_virtual_earth(port: Union[int, str] = "default", debug: bool = False):
    path = get_data_path("frmt_wms_virtualearth.xml")
    return TileClient(path, port=port, debug=debug)


def get_arcgis(port: Union[int, str] = "default", debug: bool = False):
    path = get_data_path("frmt_wms_arcgis_mapserver_tms.xml")
    return TileClient(path, port=port, debug=debug)


def get_elevation(port: Union[int, str] = "default", debug: bool = False):
    path = get_data_path("aws_elevation_tiles_prod.xml")
    return TileClient(path, port=port, debug=debug)


def get_bahamas(port: Union[int, str] = "default", debug: bool = False):
    path = get_data_path("bahamas_rgb.tif")
    return TileClient(path, port=port, debug=debug)


def get_pine_gulch(port: Union[int, str] = "default", debug: bool = False):
    path = get_pine_gulch_url()
    return TileClient(path, port=port, debug=debug)


def get_landsat(port: Union[int, str] = "default", debug: bool = False):
    path = get_data_path("landsat.tif")
    return TileClient(path, port=port, debug=debug)


def get_san_francisco(port: Union[int, str] = "default", debug: bool = False):
    path = get_sf_bay_url()
    return TileClient(path, port=port, debug=debug)
