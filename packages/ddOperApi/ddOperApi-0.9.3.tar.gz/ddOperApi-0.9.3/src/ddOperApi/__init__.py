"""Module to connect to the dd-api-oper

This module contains the following classes:

 * ddOperApi: Main class to connect to the dd api oper interface
 * ddOperResult: Super class for results
   - ddOperLocation: Result class for locations
   - ddOperQuantitie: Result class for quantities
   - ddOperValues: Result class for values
 * ddOperApiHttpError: Exception class for http errors

See:
    https://digitaledeltaorg.github.io/dd-oper.v201.html
"""

import logging
import requests
import numpy as np
from datetime import datetime, timedelta
from dateutil.parser import parse

""" Version info changed by git hook """
__version__ = '0.9.3'

class ddOperApi:
    """
    Class that connects to the digitale delta api with a client certificate.

    Methods for retrieving:
     - The list of locations
     - The list of quantitiess
     - The quantities of a location
     - Values for a given process, location and quantity
    """

    RWS_DD_API = "https://ddapi.rws.nl/dd-oper/2.0"

    def __init__(self, certfile=None, certkey=None, url=RWS_DD_API, checkssl=True):
        """ddOperApi(certfile, certKey, url="https://ddapi.rws.nl/dd-oper/2.0", checkssl=True)

certfile:           x509 pki overheidscertificaat
certKey:            Unencrypted private key
url(optional):      dd Api url (default https://ddapi.rws.nl/dd-oper/2.0)
checkssl(optional): Check ssl keychain (default true)

Details for the certificate files see:
    https://requests.readthedocs.io/en/master/user/advanced/#client-side-certificates

"""
        self.certfile = certfile
        self.certkey  = certkey
        self.url      = url
        self.checkssl = checkssl
        logging.debug("ddOperApi.__init__(%s)" % url)

    def get(self, url):
        """get(url)

Get the json data from the dd-api with pyton request.

Note: Internal use!
"""
        logging.debug("ddOperApi.get(%s)" % url)
        try:
            req = requests.get(url, cert=(self.certfile, self.certkey), verify=self.checkssl)
        except Exception as e:
            logging.exception("ddOperApi.get error: %s" % e)
            raise(e)
        if (req.status_code != 200):
            raise ddOperApiHttpError(req.status_code)
        return(req.json())

    def locations(self):
        """locations()

Request the list of locations and return a ddOperLocation object.
"""
        return(ddOperLocation(self.get(self.url + "/locations")["results"]))

    def quantities(self):
        """quantities()

Request the list of quantities and return a ddOperQuntitie object.
"""
        return(ddOperQuantitie(self.get(self.url + "/quantities")["results"]))

    def locationQuantities(self, location):
        """locationQuantities(location)

location: A dd-api location (e.g. hoekvanholland)

Request the list of quantities from a location and return
a ddOperQuntitie object.
"""
        return(ddOperQuantitie(self.get(self.url + "/locations/%s/quantities" % location)["results"]))

    def values(self, location, quantitie, process="measurement",
                     starttime=None, endtime=None,
                     intervalLength="10min", aspectset="minimum"):
        """values(location, quantitie, process="measurement",
    starttime=None, endtime=None, intervalLength="10min", aspectset="minimum")

location:                 A dd-api location (e.g. hoekvanholland)
quantitie:                A dd-api quantitie (e.g. waterlevel)
process(optional):        Default measurement (forecast, astronomical, advise)
starttime(optional):      Start of the time serie (Default 24 hours ago)
endtime(optional):        End of the time serie (Default now)
intervalLength(optional): Interval between measurements (default 10 min)
aspectset(optional):      Default minimum (normal, maximum)

"""
        if not endtime:
            endtime = datetime.utcnow()
        if not starttime:
            starttime = endtime - timedelta(days=1)
        if type(starttime) == datetime:
            starttime = starttime.isoformat() + "Z"
        if type(endtime) == datetime:
            endtime = endtime.isoformat() + "Z"
        logging.debug("ddOperApi.values(%s, %s, %s, %s, %s, %s, %s)" % (
                        location, quantitie, process, starttime, endtime,
                        intervalLength, aspectset))
        return(ddOperValues(self.get((
                            "%s"
                            "/locations/%s/quantities/%s"
                            "/timeseries?&startTime=%s&endTime=%s"
                            "&process=%s&intervalLength=%s&aspectSet=%s"
                        ) %
                        (
                            self.url,
                            location, quantitie,
                            starttime, endtime,
                            process,
                            intervalLength, aspectset
                        ))))

class ddOperResult(object):
    """
Class ddOperResult:

Base class for ddOperResults.
"""

    def __init__(self, data):
        """ddOperResult(data)"""
        self.data = data

class ddOperLocation(ddOperResult):
    """
Class ddOperLocation:

ddOper Result class for locations.
"""

    def __init__(self, data):
        super().__init__(data)
        self.createIndex()

    def createIndex(self):
        """createIndex()

Note: Internal function
"""
        self.__index = {}
        i = 0
        for loc in self.data:
            self.__index[loc["properties"]["locationName"]] = i
            i+=1

    def locationNames(self):
        """locationNames()

Returns a list of ddapi location names
"""
        return(self.__index.keys())
         
    def locationDetail(self, locationName):
        """locationDetail(locationName):

Returns the detais of a location from the list
"""
        return(self.data[self.__index[locationName]])

    def displayNameGlobal(self, locationName):
        """displayNameGlobal(locationName)

Returns the global display name of a location
"""
        return(self.locationDetail(locationName)["properties"]["displayNameGlobal"])

    def coordinate(self, locationName):
        """coordinate(locationName)

Returns the coordinates of a location
"""
        return(self.locationDetail(locationName)["geometry"]["coordinates"])

class ddOperQuantitie(ddOperResult):
    """
Class ddOperQuantitie:

ddOper Result class for Quantities.
"""

    def quantities(self):
        """quantities()

Returns a list of quantities
"""
        return(self.data)

class ddOperValues(ddOperResult):
    """
Class ddOperValues:

ddOper Result class for values.
"""

    def provider(self):
        """provider()

Returns the provider metadata.
"""
        return(self.data["provider"])

    def result(self, index=0):
        """result(index=0)

Returns the results part of the response.
"""
        return(self.data["results"][index])

    def __iter__(self):
        self.values()

    def aspectSet(self):
        """aspectSet()

Returns the metadata of the aspectSet.

Note: Return a empty dict if there is no aspectset (matroos)
"""
        observationType = self.result().get("observationType", {})
        aspectSet       = observationType.get("aspectSet", {})
        aspects         = aspectSet.get("aspects", {})
        return(aspects)

    def location(self):
        """location()

Returns the location metadata
"""
        return(self.result()["location"])

    def source(self):
        """source()

Returns the source metadata
"""
        return(self.result()["source"])

    def values(self, index=0, quality=False, additionalInfo=False):
        """values(index=0, quality=False, additionalInfo=False)

Returns the values as a ittorator of tupples.

 (datetime, value, (quality, addiotinalInfo))
 (datetime, value, ...)

Note:
  Is this the correct return data format??
  This may change!
"""
        for e in self.result()["events"]:
            dt = parse(e["timeStamp"])
            if "value" in e:
                p  = e
            elif "aspects" in e:
                p  = e["aspects"][index]["points"][0]
            else:
                raise()
            v  = p.get("value", None)
            q  = p.get("quality", None)
            a  = p.get("additionalInfo", None)
            if (quality & additionalInfo):
                yield (dt, v, q, a)
            elif quality:
                yield (dt, v, q)
            elif additionalInfo:
                # Why would you use this?
                yield (dt, v, a)
            else:
                yield (dt, v)

    def np(self, index=0, quality=False, additionalInfo=False):
        """np(index=0, quality=False, additionalInfo=False)

Returns the values as a numpy array

 (datetime, value, (quality, additionalInfo))
 (datetime, value, ...)

Note:
  Is this the correct return data format??
  This may change!
"""
#        c = 2
#        if quality:
#            c+=1
#        if additionalInfo:
#            c+=1
#        l = len(self.result()["events"])
#        res = np.empty((c, l))
#        i = 0
        res = []
        for elem in self.values(index, quality, additionalInfo):
            res.append(elem)
        return(np.array(res).T)

    def sip(self, index=0):
        """sip(index)

Returns the result set as string in the sip format!
"""
        r   = "!"
        sep = " "
        for e in self.result()["events"]:
            if "aspects" in e:
                e = e["aspects"][index]["points"][0]
            v   = e["value"]
            q   = e["quality"]
            r  += "%s%i/%i" % (sep, v, q)
            sep = ";"
        return(r)
        
class ddOperApiHttpError(Exception):
    """
Class ddOperApiHttpError

Exception class to use on http errors.
"""
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return("Code: %s" % self.code)

class ddOperApiJsonError(Exception):
    """
Class ddOperApiJsonError

Exception class to use on json errors.
"""
    def __init__(self, json):
        self.json = json

    def __str__(self):
        return("Parse error in: %s" % self.json)

if __name__ == "__main__":
    pass
