import sys
import re
import xapian
from MoinMoin.search.Xapian.indexing import MoinSearchConnection 
import glob

def crossquery(querystring, lgs): 
    url = 'http://www.galoes.org/grammars/%s/%s'
    width = 0
    #querystring = sys.argv[1]
    d = '/var/wiki'
    #lgs = glob.glob('/var/wiki/*')
    results = []
    for lg in lgs:  
	qp = xapian.QueryParser()
	try:
	    database = xapian.Database('/var/wiki/xapian/%s/index'%lg)
	except:
	    #print "no index found for ", lg
	    continue
	qp.set_database(database)
	msc = MoinSearchConnection(database)
	qresults = msc.get_all_documents(query=qp.parse_query(querystring))
	for r in qresults:
	    wikiname = r.data['title'][0]
	    wikinamefs = wikiname.replace(' ','(20)').replace(',','(2c)')
	    try:
		    revnr = open('%s/%s/pasges/%s/current'%(d,lg,wikinamefs)).read().strip()
		    content = open('%s/%s/pages/%s/revisions/%s'%(d,lg,wikinamefs,revnr)).read()
	    except IOError:
		print "File not Found", wikinamefs
		continue
	    matches = re.findall('%s%s%s' % (width*'.',querystring.lower(),width*'.'),content.lower())
	    results.append({'link':url%(lg,wikinamefs),
			    'matchcount':len(matches),
			    'matches':matches,
				})
    return result
