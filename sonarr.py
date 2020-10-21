import requests
import json
from urllib.parse import urljoin
from pprint import pprint

class SonarrAPI():
    SERIES_LOOKUP_ENDPOINT_TVDB = "/api/series/lookup"
    SERIES_ENDPOINT = "/api/series"

    def __init__( self, server, api_key ):
        self.server = server
        self.rq_session = requests.Session()
        self.rq_session.headers.update({'X-Api-Key':api_key})

    def lookup_by_tvdb_id( self, tvdb_id ):
        full_endpoint_url = urljoin( self.server,
                SonarrAPI.SERIES_LOOKUP_ENDPOINT_TVDB )
        response = self.rq_session.get( full_endpoint_url,
                params = {'term':'tvdb:%s' % tvdb_id} )
        if response.text:
            return json.loads( response.text )[0]
        else: return None

    def add_series( self, lookup_output, qualityProfileId=3,
            rootFolderPath="/media", monitored=True, download=True):
        full_endpoint_url = urljoin( self.server, SonarrAPI.SERIES_ENDPOINT )
        lookup_output['rootFolderPath'] = rootFolderPath
        lookup_output['profileId'] = qualityProfileId
        lookup_output['monitored'] = monitored
        lookup_output['seasonFolder'] = True
        lookup_output['addOptions'] = {'searchForMissingEpisodes':download}
        response = self.rq_session.post(full_endpoint_url, json = lookup_output )
        response.raise_for_status()
        if response.text:
            return json.loads( response.text )
        else:
            return None
