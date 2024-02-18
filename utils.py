import requests
from geojson import GeoJSON, loads
from shapely import from_geojson
from shapely.geometry import  Point, GeometryCollection

BASE_URL = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test"

def get_clinician_status(clinician_id: int) -> GeoJSON:
    endpoint = f"{BASE_URL}/clinicianstatus/{clinician_id}"
    response = requests.get(endpoint)
    info = loads(response.text)
    return info

def parse_geojson(geo_info: GeoJSON) -> tuple[Point, GeometryCollection]:
    """
    Convert GeoJSON into usable Shapely Geometry to perform bounds checks
    """
    zones = []
    location = None
    features = geo_info['features']
    for feature in features:
        shape = from_geojson(str(feature))
        if shape.geom_type == 'Point':
            location = shape
        else:
            zones.append(shape)
    return location, GeometryCollection(zones)

def clinician_outside_zone(location: Point, bounding_zone: GeometryCollection) -> bool:
    return not location.intersects(bounding_zone)


# UNUSED: My own custom implementation of point-in-polygon collision, using the Ray-Casting Algorithm
# Replaced by the shapely library's intersects() method
def is_outside_polygon(point: list[float], polygon: list[list[float]]) -> bool:
    """
    Cast horizontal ray (to simplify math) from point and check intersection with all lines of the polygon.
    If intersection count is even -> point is outside, if odd -> point is inside 
    """
    x,y = point
    is_outside = False
    vert1_x, vert1_y = polygon[0]
    for vertex in polygon[1:]:
        vert2_x, vert2_y = vertex
        if vert1_y == vert2_y:
            if y == vert1_y and min(vert1_x,vert2_x) <= x <= max(vert1_x, vert2_x):
                is_outside = not is_outside
        else:        
            x_intersection = vert1_x + (vert2_x - vert1_x) * (y-vert1_y) / (vert2_y-vert1_y)
            if min(vert1_x,vert2_x) <= x_intersection <= max(vert1_x, vert2_x) and x_intersection <= x:
                is_outside = not is_outside
        vert1_x, vert1_y = vert2_x, vert2_y  
    return is_outside