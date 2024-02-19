import requests
from requests.exceptions import RequestException 
import smtplib
from typing import Union
from geojson import GeoJSON, loads
from shapely import from_geojson
from shapely.geometry import  Point, GeometryCollection
import smtplib
from email.mime.text import MIMEText
from config import API_BASE_URL, SMTP_EMAIL, SMTP_PASSWORD, EMAIL_INBOX

def get_clinician_status(clinician_id: int) -> Union[GeoJSON, RequestException]:
    '''
    Fetches Clinician's status from API and converts to GeoJSON (throws error if data is unavailable) 
    '''
    endpoint = f"{API_BASE_URL}/clinicianstatus/{clinician_id}"
    response = requests.get(endpoint)
    info = loads(response.text)
    if 'features' not in info.keys():
        raise requests.exceptions.RequestException
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
    """
    Determine if clinician is inside their specified zone (inclusive of boundary)
    """
    return not location.intersects(bounding_zone)

def send_email(subject: str, body: str, to_email: str = EMAIL_INBOX, from_email: str = SMTP_EMAIL):
    """
    Use built-in SMTP to send an email 
    """
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

def poll_clinician_statuses(num_employees = 6):
    """
    Poll and carry out necessary actions for all clinicians based on their current location/status
    """
    for i in range(1, num_employees+1):
        try:
            geo_info = get_clinician_status(i)
            location, zone = parse_geojson(geo_info)
            if clinician_outside_zone(location, zone):
                print(f"ALERT! Clinician {i} is outside of their zone!")
                email_body_lines = [
                    f"Clinician {i} is outside of their expected scheduled zone!",
                    "For an interactive view of their current location, visit http://geojson.io and paste the following text into the JSON tab:",
                    str(geo_info)
                ]
                send_email(f"ALERT: Clinician {i} is outside of expected scheduled zone", "\n\n".join(email_body_lines)) 
            else:
                print(f"Clinician {i} is safely in their zone!") 
        except RequestException:
            print(f"ALERT! Location Data for Clinician {i} currently unavailable")
            email_body_lines = [
                f"Location Data for Clinician {i} is currently unavailable",
                f"Please check status at {API_BASE_URL}/clinicianstatus/{i}"
            ]
            send_email(f"ALERT: Location is currently unknown for Clinician {i}", "\n\n".join(email_body_lines)) 
