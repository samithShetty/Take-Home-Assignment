import requests
import geojson

BASE_URL = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test"

def get_clinician_status(clinician_id: int) -> geojson.GeoJSON:
    endpoint = f"{BASE_URL}/clinicianstatus/{clinician_id}"
    response = requests.get(endpoint)
    info = geojson.loads(response.text)
    return info

def get_clinician_location(geo_info: geojson.GeoJSON) -> list[float]:
    # GeoJSON does not guarantee any order, so we should check all features
    # The feature for clinician location will be the only 'Point'
    for feature in geo_info['features']:
        if feature['geometry']['type'] == 'Point':
            return feature['geometry']['coordinates']

def get_bounding_zones(geo_info: geojson.GeoJSON) -> list[list[float]]:
    # There will sometimes be multiple separate zones in the GeoJSON
    # Each will be their own 'Polygon' feature, so we should return the list of all of them
    polygons = []
    for feature in geo_info['features']:
        if feature['geometry']['type'] == 'Polygon':
            polygons.append(feature['geometry']['coordinates'])
    return polygons

def is_clinician_outside_zone(geo_info: geojson.GeoJSON) -> bool:
    location = get_clinician_location(geo_info)
    bounding_zones = get_bounding_zones(geo_info)
    for zone in bounding_zones:
        if is_outside_zone(location, zone):
            return True
    return False

def is_outside_zone(point, zone) -> bool:
    #TODO: Implement Point-in-Polygon Collision
    return False