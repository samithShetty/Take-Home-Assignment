# Poll API on regular interval
for sprinterID in sprinterIDs:
    sprinter_info = get_sprinter_info(sprinterID)

    # Parse response -> Check if sprinter is in Zone
    if not sprinter_info or is_outside_zone(sprinter_info.location, sprinter_info.zone):

# If no response or sprinter outside -> send email
        send_warning_email(sprinter_info)
