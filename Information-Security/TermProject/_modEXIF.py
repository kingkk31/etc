from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

#extract GPS information
def ExtractGPSDictionary(fileName):

    #get exif information
    try:
        pilImage = Image.open(fileName)
        exifData = pilImage._getexif()
    
    except Exception:
        return None, None

    imageTimeStamp = "NA"
    cameraModel = "NA"
    cameraMake = "NA"
    gpsData = False
    
    gpsDictionary = {}
    
    if exifData:
            
        for tag, theValue in exifData.items():

            #get value of tag
            tagValue = TAGS.get(tag, tag)
                
            if tagValue == 'DateTimeOriginal':
                imageTimeStamp = exifData.get(tag)
                
            if tagValue == "Make":
                cameraMake = exifData.get(tag)
                
            if tagValue == 'Model':
                cameraModel = exifData.get(tag)

            #GPS information
            if tagValue == "GPSInfo":
                
                gpsData = True;

                #get GPS value of GPS tag
                for curTag in theValue:
                    gpsTag = GPSTAGS.get(curTag, curTag)
                    #add dictionary of GPS information
                    gpsDictionary[gpsTag] = theValue[curTag]

                #other information list
                basicExifData = [imageTimeStamp, cameraMake, cameraModel]    

                #return results
                return gpsDictionary, basicExifData
            
        if gpsData == False:
            return None, None
    else:
        return None, None
    

#extract latitude, longtitude
def ExtractLatLon(gps):

    if (gps.has_key("GPSLatitude") and gps.has_key("GPSLongitude") and gps.has_key("GPSLatitudeRef") and gps.has_key("GPSLatitudeRef")):

        #get latitude, longtitude
        latitude     = gps["GPSLatitude"]
        latitudeRef  = gps["GPSLatitudeRef"]
        longitude    = gps["GPSLongitude"]
        longitudeRef = gps["GPSLongitudeRef"]

        #convert to degrees
        lat = ConvertToDegrees(latitude)
        lon = ConvertToDegrees(longitude)
                
        if latitudeRef == "S":
            lat = 0 - lat

        if longitudeRef == "W":
            lon = 0- lon

        #set result dictionary
        gpsCoor = {"Lat": lat, "LatRef":latitudeRef, "Lon": lon, "LonRef": longitudeRef}

        #return result
        return gpsCoor
    
    else:
        return None
    

#conver to degrees
def ConvertToDegrees(gpsCoordinate):

    #degrees
    d0 = gpsCoordinate[0][0]
    d1 = gpsCoordinate[0][1]
    try:
        degrees = float(d0) / float(d1)
    except:
        degrees = 0.0

    #minutes
    m0 = gpsCoordinate[1][0]
    m1 = gpsCoordinate[1][1]
    try:
        minutes = float(m0) / float(m1)
    except:
        minutes=0.0

    #seconds
    s0 = gpsCoordinate[2][0]
    s1 = gpsCoordinate[2][1]
    try:
        seconds = float(s0) / float(s1)
    except:
        seconds = 0.0

    #result degrees
    floatCoordinate = float (degrees + (minutes / 60.0) + (seconds / 3600.0))

    #return result
    return floatCoordinate

