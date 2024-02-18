import utils

NUM_EMPLOYEES = 6

#TODO: Implement Time interval

for i in range(1, NUM_EMPLOYEES+1):
    geo_info = utils.get_clinician_status(i)
    if utils.is_clinician_outside_zone(geo_info):
        # TODO: Implement Email Sending
        print("Alert! Clinician {i} is outside of their zone!") 