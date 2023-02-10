from girbot import client
from .radarr import RadarrAPI
from .sonarr import SonarrAPI
import re
import os

RADARR_SERVER = os.getenv( 'RADARR_SERVER' )
if not RADARR_SERVER:
    raise Exception( "Please specify RADARR_SERVER env variable" )
RADARR_API_KEY = os.getenv( 'RADARR_API_KEY' )
if not RADARR_API_KEY:
    raise Exception( "Please specify RADARR_API_KEY env variable" )
ROOT_FOLDER_PATH = os.getenv( 'ROOT_FOLDER_PATH' )
if not ROOT_FOLDER_PATH:
    raise Exception( "Please specify ROOT_FOLDER_PATH env variable" )
SONARR_SERVER = os.getenv( 'SONARR_SERVER' )
if not SONARR_SERVER:
    raise Exception( "Please specify SONARR_SERVER env variable" )
SONARR_API_KEY = os.getenv( 'SONARR_API_KEY' )
if not SONARR_API_KEY:
    raise Exception( "Please specify SONARR_API_KEY env variable" )

@client.command( "movie" )
async def movie(ctx, movie):
    imdb_ids = re.compile("tt\d{7,8}").findall( movie )
    if not imdb_ids:
        await ctx.send("IMDB id not found")
    else:
        imdb_id = imdb_ids[0]
        r = RadarrAPI( RADARR_SERVER, RADARR_API_KEY )
        movie = r.lookup_by_imdb_id( imdb_id )
        if not movie:
            await ctx.send("No movie found for ID: %s" % imdb_id)
        else:
            response = r.add_movie( movie )
            try:
                if "already been added" in response:
                    await ctx.send( "Movie '%s' is _probably_ already on the plex" % movie['title'])
                elif not response:
                    await ctx.send( "There was a problem adding movie '%s'" % movie['title'] )
                else:
                    await ctx.send( "Movie '%s' successfully added" % movie['title'] )
            except:
                await ctx.send( "There was a problem adding movie '%s'" % movie['title'])

@client.command( "tv" )
async def tv(ctx, tvdb_series_id):
    try:
        s = SonarrAPI( SONARR_SERVER, SONARR_API_KEY )
        series = s.lookup_by_tvdb_id( tvdb_series_id )
        if not series:
            await ctx.send( "No series found for ID: %s" % tvdb_series_id )
        else:
            response = s.add_series( series )
            if "already been added" in response:
                await ctx.send( "Tv show '%s' is _probably_ already on the plex" % series['title'])
            elif not response:
                await ctx.send( "There was a problem adding series %s" % series['title'] )
            else:
                await ctx.send( "Series '%s' successfully added" % series['title'] )
    except:
        await ctx.send("There was a probelm adding series %s" % series['title'])
