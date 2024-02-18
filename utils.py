import requests
import smtplib
from geojson import GeoJSON, loads
from shapely import from_geojson
from shapely.geometry import  Point, GeometryCollection
import smtplib
from email.mime.text import MIMEText
from config import API_BASE_URL, SMTP_EMAIL, SMTP_PASSWORD

def get_clinician_status(clinician_id: int) -> GeoJSON:
    endpoint = f"{API_BASE_URL}/clinicianstatus/{clinician_id}"
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

def send_email(subject: str, body: str, to_email: str = SMTP_EMAIL, from_email: str = SMTP_EMAIL):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587 
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)

        email = MIMEText(body)
        email['From'] = from_email
        email['To'] = to_email
        email['Subject'] = subject
        server.sendmail(from_email, to_email, email.as_string())
