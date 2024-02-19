# Take-Home-Assignment
This service polls clinician locations on a regular interval and sends alert emails when clinicians are either outside of their expected scheduled zone or when their location is unavaialable.   
It runs on Python 3.12, primarily using the GeoJSON, Shapely, and SMTP libraries.

If you want to run to actually run the service locally, you just need to provide the config variables (explained at the bottom of this README) and run the `main.py` file.

Below I've provided some explanations for some some of my design and implementation decisions of this system. 

## Split into  `main.py` and `utils.py` files

For sake of simplicity, I have a single `main.py` which runs is what runs and polls the statuses on a set interval, and this calls functions inside the the `utils.py` file, which contains all utility functions for the various tasks this system requires. I think this helps readability greatly and is the right balance of abstraction and simplicity for a system of this size, however if there was more functionality to add to the system, I would consider further dividing the utilities into separate modules within a utilities package (i.e. utils.requests, utils.email_services, utils.geometry, etc.) rather than stuffing all of the unrelated utilities into a single file.

## Use of GeoJSON library

I discovered that there is a GeoJSON library for Python that provides native Python objects that conform to the GeoJSON standard which the API uses. While I found that working with these objects didn’t particularly simplify the code any more than directly handling the JSON as it’s provided, using the library does ensure that the JSON is being properly received and read in the correct format, thus I considered it worth adding and using. 

## Email Method

This system utilizes the built-in Python library from SMTP (Simple Mail Transfer Protocol). Since we only needed to send simple emails to a single inbox, using a more complex services would’ve only added cost and complexity to the code where a single utility function to wrap the functionality provides everything we need.

## Point-in-Polygon Collision

I opted to use the open-source Shapely library to handle point-in-polygon collisions rather than relying on my own-implementation (which can be seen below). While my implementation mostly worked, I found the Shapely library to be more robust in handling edge-cases and also greatly simplified the code overall, as it integrates well with the pre-existing use of the GeoJSON standard. Nonetheless, if using the shapely library were not possible for our service for some reason, the next best option would be to expand upon the above implementation and use it as an internal utility.

```python
# UNUSED: My own custom implementation of point-in-polygon collision, using the Ray-Casting Algorithm
# Replaced by the more robust shapely.intersects() method
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
```


## Key Config File

I've opted to place sensitive keys such as the SMTP email login/password as well and configuration specific resources such as the API endpoint, Polling Rate, and output Email Inbox in a local `config.py` file that is not included in the repo itself. This file simply defines these environment variables so that they can then be imported and accessed from other files without revealing their values, mimicking how this service would run internally using some sort of environment variable or token manager setup.