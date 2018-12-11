import urllib
from BeautifulSoup import BeautifulSoup   
import re

import sys
import re
import xapian
from MoinMoin.search.Xapian.indexing import MoinSearchConnection 
from MoinMoin import wikiutil

#from galoes.lib import crossquery


from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'galoes',
            'grammarlist':  [ 
		    ['fin', 'Finnish', 'John Doe', 'sebastian.nordhoff at gmail.com'], 
		    ['sci', 'Sri Lanka Malay', 'John Doe', 'sebastian.nordhoff at gmail.com'], 
		    ['sjd', 'Kildin Saami', 'John Doe', 'sebastian.nordhoff at gmail.com'],
		    ['sje', 'Pite Saami', 'John Doe', 'sebastian.nordhoff at gmail.com'],
		    ['sjt', 'Ter Saami', 'John Doe', 'sebastian.nordhoff at gmail.com'],
		    ['sme', 'North Saami', 'John Doe', 'sebastian.nordhoff at gmail.com'],
		    ['swe', 'Swedish', 'John Doe', 'sebastian.nordhoff at gmail.com'],
		    ['udu', 'Uduk', 'John Doe', 'sebastian.nordhoff at gmail.com'], 
		   ],
	'walslist': [('A01','Consonant Inventories'),
	('A02','Vowel Quality Inventories')
	],	
	'ldslist' : [("1.","Syntax"),
	("1.1.","General questions")
	]
	,	
	'occultlist' : [("1.","semasiological"),
	("2.","onomasiological")
	]
}

@view_config(route_name='grammarsearch', renderer='templates/result.pt')
def grammarsearch(request): 
    lgs = request.params.getall('lgs[]')
    print lgs
    querystring = request.params.get('freesearch','no_querystring_provided')
    d = {}
    totalmatches = 0
    for lg in lgs:
	d[lg] = crossquery(querystring, lg)
	for r in d[lg]: 
	    totalmatches += len(r['matches'])
		
	
    
    return {'project': 'galoes',
            'searchstring': querystring,
            'pages' : d,
            'totalmatches': totalmatches
    }
    
def crossquery(querystring, lg): 
    url = 'http://www.galoes.org/grammars/%s/%s'
    width = 20 
    
    d = '/var/wiki' 
    results = [] 
    qp = xapian.QueryParser() 
    database = xapian.Database('/var/wiki/xapian/%s/index'%lg) 
    qp.set_database(database)
    msc = MoinSearchConnection(database)
    qresults = msc.get_all_documents(query=qp.parse_query(querystring))
    
    for r in qresults:
	wikiname = r.data['title'][0]
	wikinamefs = wikiutil.quoteWikinameFS(wikiname)
	try:	
	    refv = '%s/%s/pages/%s/current'%(d,lg,wikinamefs) 
	    revnr = open(refv).read().strip()
	    contentf = '%s/%s/pages/%s/revisions/%s'%(d,lg,wikinamefs,revnr) 
	    content = open(contentf).read().decode('utf8')
	except IOError:
	    print "File not Found", wikinamefs
	    continue
	
	matches = re.findall(u'%s%s%s' % ('.'+'{,%i}'%width,querystring.lower(),'.'+'{,%i}'%width),content.lower())
	print matches
	results.append({'link':url%(lg,wikinamefs),
			'totalmatches':len(matches),
			'matches':matches,
			'name':wikiname,
			    })
    return results