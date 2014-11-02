#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
Collects samples from bing
"""
import settings
import requests
import json
import os

def getUrls( word, key, skip=0, urls=[] ):
    
    print "Samples:", len(urls)
    prefix = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Image'
    params = {
            'Query': "'%s'" % word , 
            'Adult': "'Off'", 
            '$format': 'json', 
            }
    
    if skip:
        params.update( { '$skip': str( skip ) } )

    results = requests.get( prefix, auth=( key, key ), params=params)
    results = results.json()
    for result in results['d']['results']:
        typ = result[ 'ContentType' ]
        if typ== 'image/jpg' or typ == 'image/jpeg':
            urls.append( result['MediaUrl'] )

    if results['d'].has_key( '__next' ):
        return getUrls( word, key, skip=skip+50, urls=urls)
    else:
        return urls

def saveImages( urls, dir ):
    counter = 0
    for url in urls:
        try:
            counter = counter + 1
            print "writing [%d/%d]: %s" % (counter, len(urls), url)
            fname = os.path.join( dir, os.path.basename( url ) )
            if not os.path.exists(fname):
                img = requests.get(url, timeout=5).content
                f = open(fname , 'wb' )
                f.write( img )
                f.close()
        except Exception, e:
            print "failed to get "
            print url
            print e.message
            pass
        except requests.exceptions.ReadTimeout:
            print "timeout"

if __name__ == '__main__':
    word = settings.word
    key = settings.key
    dir = os.path.join( 'static', 'img' )

    urls = getUrls( word, key )
    saveImages( urls, dir )
