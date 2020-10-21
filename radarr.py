import requests
import json
from urllib.parse import urljoin

class RadarrAPI():
    MOVIE_LOOKUP_ENDPOINT_IMDB = "/api/movie/lookup/imdb"
    MOVIE_ENDPOINT = "/api/movie"
    def __init__( self, server, api_key ):
        self.server = server
        self.rq_session = requests.Session()
        self.rq_session.headers.update({'X-Api-Key':api_key})

    def get_movies( self ):
        full_endpoint_url = urljoin( self.server, RadarrAPI.MOVIE_ENDPOINT )
        response = self.rq_session.get( full_endpoint_url )
        print( response.text )


    def lookup_by_imdb_id( self, imdb_id ):
        """
        https://github.com/Radarr/Radarr/wiki/API:Movie-Lookup
        """
        full_endpoint_url = urljoin( self.server,
                RadarrAPI.MOVIE_LOOKUP_ENDPOINT_IMDB )
        response = self.rq_session.get(full_endpoint_url,
                params = {'imdbId':imdb_id})
        if response.text:
            return json.loads( response.text )
        else:
            return None

    def add_movie( self, lookup_output, qualityProfileId=3,
            rootFolderPath="/media", monitored=True, download=True ):
        full_endpoint_url = urljoin( self.server, RadarrAPI.MOVIE_ENDPOINT )
        lookup_output['qualityProfileId'] = qualityProfileId
        lookup_output['rootFolderPath'] = rootFolderPath
        lookup_output['monitored'] = True
        lookup_output['addOptions'] = {'searchForMovie':download}
        response = self.rq_session.post(full_endpoint_url, json = lookup_output )
        response.raise_for_status()
        if response.text:
            return json.loads( response.text )
        else:
            return None
