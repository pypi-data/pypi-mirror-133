import math
import random
import geopy.distance

from .geometry import *
from .timeWindows import *

# Description =================================================================
# STATUS: Currently under rewriting for smaller type of clouds.
# This script is to simulate the movement of clouds
# Note:
#     This script should be independent from other projects, and should be reused
# Assumption:
# 1. The rain and snow happens only when there are clouds above
# 2. Wind speed is not related to the speed of clouds
# 3. Spinning of clouds are not modeled

# Reference ===================================================================
# Taylor's Hypothesis ---------------------------------------------------------
# A series of changes in time at a fixed place is due to the passage of an unchanging 
# spatial pattern over that locale. That is, when observing a cloud or thunderstorm 
# passing overhead, the clouds of the thunderstorm floating by are effectively 
# "unchanging spatial patterns" (big blocks of cloud). Put another way, the lateral 
# change in the cloud conditions across regions of the meteorological event (e.g., 
# cloud-sky-cloud-sky-cloud) can be directly connected locally with a variation in 
# irradiance measurement over time (e.g., a periodic measure of dark-bright-dark-bright-dark).
# Ref: https://www.e-education.psu.edu/eme810/node/583

# Key parameters --------------------------------------------------------------
# Speed of meteorological phenomena: 17 m/s
# Four type of meteorological phenomena and their scale:
# - Cumulus: 2-5 km, 10-100 minutes
# - Cumulonimbus: 10-200 km, 1-5 hours
# - Cumulonimbus cluster: 50-1000 km, 3-36 hours
# - Synoptic: 1000-400000 km, 2-15+ days
# We only consider: 1) Cumulus, 2) Cumulonimbus, and 3) Cumulus + Cumulonimbus (?) situations, the other two are too large

# Constants ===================================================================
# Parameters for clouds
CLOUD_SPD_ABS_RANGE = [15, 19] # 17 m/s
CLOUD_SPD_DEG_RANGE = [50, 70] # [deg, deg]
CLOUD_ORI_DEG_RANGE = [-45, 45] # [deg, deg]

CLOUD_CUMULUS_SIZE = [2000, 5000] # 2-5 km
CLOUD_CUMULONIMBUS_SIZE = [10000, 200000] # 10-200 km

CLOUD_CUMULUS_DURATION = [10 * 60, 100 * 60] # 10 - 100 mins
CLOUD_CUMULONIMBUS_DURATION = [60 * 60, 5 * 60 * 60] # 1-5 hours

def rndRainCloud(
    centroidLatLon: "The lat/lon that the cloud is generated and starts raining/snowing" = None,
    appearTime: "Time when this weather phenomena appears" = 0,
    movingVecPolar: "Moving vector in polar coordinate" = None,
    cloudMode:  "1) String, 'Cumulus', or\
                 2) String, 'Cumulonimbus" = 'Cumulus'
    ) -> "Randomly generate a polygon, that represents a rain cloud. Nodes covered by the rain cloud will be raining/snowing":
    # Size of cloud ===========================================================
    widthInMeter = None
    lengthInMeter = None
    if (cloudMode == 'Cumulus'):
        widthInMeter = random.randrange(CLOUD_CUMULUS_SIZE[0], CLOUD_CUMULUS_SIZE[1])
        lengthInMeter = random.randrange(CLOUD_CUMULUS_SIZE[0], CLOUD_CUMULUS_SIZE[1])
        existDur = random.randrange(CLOUD_CUMULUS_DURATION[0], CLOUD_CUMULUS_DURATION[1])
    elif (cloudMode == 'Cumulonimbus'):
        widthInMeter = random.randrange(CLOUD_CUMULONIMBUS_SIZE[0], CLOUD_CUMULONIMBUS_SIZE[1])
        lengthInMeter = random.randrange(CLOUD_CUMULONIMBUS_SIZE[0], CLOUD_CUMULONIMBUS_SIZE[1])
        existDur = random.randrange(CLOUD_CUMULONIMBUS_DURATION[0], CLOUD_CUMULONIMBUS_DURATION[1])

    # Orientation =============================================================
    oriDeg = random.randrange(CLOUD_ORI_DEG_RANGE[0], CLOUD_ORI_DEG_RANGE[1])

    # Cloud generation ========================================================
    initPolyLatLon = rectInWidthLengthOrientationLatLon(
        centroidLatLon = centroidLatLon,
        widthInMeter = widthInMeter,
        lengthInMeter = lengthInMeter,
        oriDeg = oriDeg)
    
    return {
        'appearTime': appearTime,
        'initPolyLatLon': initPolyLatLon,
        'movingVecPolar': movingVecPolar,
        'existDur': existDur
    }

def getCloudCurrentPosition(
    cloud:      "A cloud dictionary" = None,
    timestamp:  "Time stamp" = None
    ) -> "Given a cloud dictionary and needed time stamps, returns the current position of cloud polygon":

    # Time elapsed ============================================================
    elapsed = timestamp - cloud['appearTime']
    if (elapsed > cloud['existDur'] + CONST_EPSILON or elapsed < 0):
        return None

    # Calculate current location ==============================================
    currentPoly = []
    dist = elapsed * cloud['movingVecPolar'][0]
    for pt in cloud['initPolyLatLon']:
        currentPoly.append(pointInDistLatLon(
            pt = pt, 
            direction = cloud['movingVecPolar'][1],
            distMeters = dist))

    return currentPoly

def getLocCoverBySingleCloudTW(
    cloud:      "A cloud dictionary" = None,
    loc:        "A location, in [lat, lon]" = None
    ) -> "Given a cloud and a location, returns the time window that the location is covered by cloud":
    coverTW = []
    tws = twMovingPtInsidePolyLatLon(
        ptLatLon = loc,
        polyLatLon = cloud['initPolyLatLon'],
        vecPolarPt = (0, 0),
        vecPolarPoly = cloud['movingVecPolar'])
    if (len(tws) > 0):
        for tw in tws:
            if (tw[0] < cloud['existDur']):
                coverTW.append([cloud['appearTime'] + tw[0], cloud['appearTime'] + min(cloud['existDur'], tw[1])])
    return coverTW

def getSegCoverByCloudsTW(
    clouds:     "A list of cloud dictionaries" = None,
    loc1:       "Lat/lon of the first location, in [lat, lon]" = None,
    loc2:       "Lat/lon of the first location, in [lat, lon]" = None
    ) -> "Given a list of clouds and two locations, returns the time windows that anywhere between two locations is covered by cloud":

    # Initialize ==============================================================
    coverTWs = []

    # For each cloud, it should generate at most one cover time window ========
    for cloud in clouds:
        tw = twMovingSegIntersectPolyLatLon(
            segLatLon = [loc1, loc2],
            polyLatLon = cloud['initPolyLatLon'],
            vecPolarSeg = [0, 0],
            vecPolarPoly = cloud['movingVecPolar'])
        if (tw != None):
            if (tw[0] < cloud['existDur']):
                coverTWs.append([cloud['appearTime'] + tw[0], cloud['appearTime'] + min(cloud['existDur'], tw[1])])

    # Merge time windows of clouds ============================================
    coverTWs = mergeTimeWindows(coverTWs)

    return coverTWs
