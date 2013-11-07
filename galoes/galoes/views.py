import urllib
from BeautifulSoup import BeautifulSoup   
import re


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

@view_config(route_name='result', renderer='templates/result.pt')
def result(request): 
    host = "http://www.galoes.org/grammars"
    context = 180
    
    questionnaireused = request.params.get('questionnaireused',u'')
    
    searchstring = 'Kasus'
    lgs =  ['fin','swe', 'sci']
    pages = {}
    for lg in lgs:
	lgresults = []
	urlstring = "%s/%s?action=fullsearch&context=%i&value=%s&fullsearch=Text" % (host,lg,context,searchstring)  
	getpage = urllib.urlopen(urlstring)
	soup = BeautifulSoup(getpage)
	dts = soup.findAll('dt')
	dds = soup.findAll('dd')  
	matcharr = soup.findAll("span", "info") 
	totalmatches = sum([int(str(x.next).replace(' . . . ','').replace(' matches','').replace(' match','')) for x in matcharr]) 
	results = []
	
	for term, definition in zip(dts,dds):
	    linkportion = re.compile('\%28.*\%29">(.*?)</a>').search(unicode(term)).group(1)  
	    link = "%s/%s/%s" % (host,lg,linkportion)
	    try:
		term = term.decode('utf8')
	    except TypeError:
		term = repr(term)
	    try:
		definition = definition.decode('utf8')
	    except TypeError:
		definition = repr(definition)
	    #weakstrongarr = h.destrongify(definition)
	    #weakstrongarr = [h.dewikify(h.striptags(x)) for x in weakstrongarr]  
	    results.append({'term':repr(term),'definition':repr(definition),'link':link}) 
	dico = {'code':lg, 'name':lg,'results':results, 'totalmatches':totalmatches} 
	pages[lg] = dico
    
    
    return {'project': 'galoes',
            'searchstring': searchstring,
            'pages' : pages
    }