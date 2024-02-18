from utils import get_clinician_status, parse_geojson, clinician_outside_zone, send_email

NUM_EMPLOYEES = 7

#TODO: Implement Time interval

for i in range(1, NUM_EMPLOYEES+1):
    geo_info = get_clinician_status(i)
    #TODO: Implement response validation
    location, zone = parse_geojson(geo_info)
    if clinician_outside_zone(location, zone):
        print(f"ALERT! Clinician {i} is outside of their zone!") 
        send_email("WARNING: Clinician has exited specified zone", f"Clinician {i} is outside of their zone!") 
    else:
        print(f"Clinician {i} is safely in their zone!") 