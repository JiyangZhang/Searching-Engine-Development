from bottle import route, run, request, FormsDict, error, redirect, app, Bottle
import collections, sqlite3, httplib2
from math import ceil, floor
from oauth2client.client import OAuth2WebServerFlow, flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
import collections
import string
import getdata as gd


#variable definitions
baseURL = ""
#new
mapURL = "https://www.google.com/maps/search/"
map_flag = 0
image_flag = 0
scope = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
redirect_uri = baseURL + '/redirect'
code = ""
checkLogout = 0
topdic = collections.OrderedDict()
userinfo = '<p> your email address :'  #user's information string
user_email = {}
# add words into dic
def countdic(stringin):
    stringin = "".join(l for l in stringin if l not in string.punctuation)
    stringin = stringin + ' '
    stringin = stringin.lower()
    dic = collections.OrderedDict()
    flag = 0
    for i in range(len(stringin)):
        if stringin[i] == ' ':
            st = stringin[flag:i]
            if st in dic:
                dic[st] = dic[st]+1
            else:
                dic[st] = 1
            if st in topdic:
                topdic[st] = topdic[st]+1
            else:
                topdic[st]=1
            flag = i+1
    return dic

#frontend script
frontend = []
frontend.append('''<!DOCTYPE html>
<html>
        <head>
        <meta name=""viewport"" content=""width=device-width, initial-scale=1, maximum-scale=1"">
                <style>
li{
        display:inline;
}
body {
        background-image: url("https://static.pexels.com/photos/36764/marguerite-daisy-beautiful-beauty.jpg");
}
a{
        font-size:20px;
}
a:link {
        color: #FFF5EE;
        background-color: transparent;
        text-decoration: none;
}
a:visited {
        color: white;
        background-color: transparent;
        text-decoration: underline;
}

a:hover{
        color: #FFF8DC;
        background-color: transparent;
        text-decoration: none;
}

.active {
color: #FFF8DC;
background-color: transparent;
text-decoration : none;
}

div.relative {
        position: relative;
        left: 60px;
}

                </style>

        </head>
<body>
<div class = "relative">
<li>
<a class = "active" href = "''' + baseURL +"/all" + '''">All &nbsp</a>
</li>
<li>
<a href = "'''+ baseURL + "/map" + '''">Maps &nbsp</a>
</li>
<li>  
<a href = "'''+ baseURL + "/image" + '''">Images &nbsp</a>
</li>
</div>
''' )  

frontend.append('''<!DOCTYPE html>
<html>
        <head>
        <meta name=""viewport"" content=""width=device-width, initial-scale=1, maximum-scale=1"">
                <style>
li{
        display:inline;
}
body {
        background-image: url("https://static.pexels.com/photos/36764/marguerite-daisy-beautiful-beauty.jpg");
}
a{
        font-size:20px;
}
a:link {
        color: #FFF5EE;
        background-color: transparent;
        text-decoration: none;
}
a:visited {
        color: white;
        background-color: transparent;
        text-decoration: underline;
}

a:hover{
        color: #FFF8DC;
        background-color: transparent;
        text-decoration: none;
}

.active {
        color: #FFF8DC;
        background-color: transparent;
        text-decoration : none;
}

div.relative {
        position: relative;
        left: 60px;
}

                </style>

        </head>
<body>
<div class = "relative">
<li>
<a  href = "''' + baseURL +"/all" + '''">All &nbsp</a>
</li>
<li>
<a class = "active" href = "'''+ baseURL + "/map" + '''">Maps &nbsp</a>
</li>
<li>  
<a href = "'''+ baseURL + "/image" + '''">Images &nbsp</a>
</li>
</div>

''' )
frontend.append('''<!DOCTYPE html>
<html>
        <head>
        <meta name=""viewport"" content=""width=device-width, initial-scale=1, maximum-scale=1"">
                <style>
li{
        display:inline;
}
body {
        background-image: url("https://static.pexels.com/photos/36764/marguerite-daisy-beautiful-beauty.jpg");
}
a{
        font-size:20px;
}
a:link {
        color: #FFF5EE;
        background-color: transparent;
        text-decoration: none;
}
a:visited {
        color: white;
        background-color: transparent;
        text-decoration: underline;
}

a:hover{
        color: #FFF8DC;
        background-color: transparent;
        text-decoration: none;
}

.active {
        color: #FFF8DC;
        background-color: transparent;
        text-decoration : none;
}

div.relative {
        position: relative;
        left: 60px;
}

                </style>

        </head>
<body>
<div class = "relative">
<li>
<a  href = "''' + baseURL +"/all" + '''">All &nbsp</a>
</li>
<li>
<a href = "'''+ baseURL + "/map" + '''">Maps &nbsp</a>
</li>
<li>  
<a class = "active" href = "'''+ baseURL + "/image" + '''">Images &nbsp</a>
</li>
</div>

''' )

html = frontend[0]
#Search form
searchHTML_mid = '''
	<div align ="middle">
		<form action ="/search" method="get" autocomplete="on" spellcheck="true">
			 <input name="userinput" type="text"/>
			<input value = "Search" type="submit" />
		</form>
	</div>
'''
searchHTML = '''
        <div>
                <form action ="/search" method="get">
                         <input name="userinput" type="text"/>
                        <input value = "Search" type="submit" />
                </form>
        </div>
        '''

#greetings
greeting = '''
<img id="d2" src="https://gss0.baidu.com/-fo3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/9825bc315c6034a8e0dd5e1dc01349540923766b.jpg" width=50/>
<img src="https://gss0.baidu.com/9vo3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/aa64034f78f0f736b693aa9d0155b319ebc41338.jpg" width=150>
'''
greeting_anime = '''
<div align ="middle">
<img id="d2" src="https://gss0.baidu.com/-fo3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/9825bc315c6034a8e0dd5e1dc01349540923766b.jpg" width="150" align="middle"/>
<script type="text/javascript">
var i=1;
function f(){
   i++;
   if(i>4) i=1;
   if(i==1){
   document.getElementById('d2').src="https://gss0.baidu.com/-fo3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/9825bc315c6034a8e0dd5e1dc01349540923766b.jpg";
   }
   if(i==2){
   document.getElementById('d2').src="https://gss0.baidu.com/-Po3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/b2de9c82d158ccbfa7df53a612d8bc3eb03541cf.jpg";
   }
   if(i==3){
   document.getElementById('d2').src="https://gss0.baidu.com/-Po3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/79f0f736afc37931115660b5e0c4b74543a9116b.jpg";
   }
   if(i==4){
   document.getElementById('d2').src="https://gss0.baidu.com/9vo3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/4b90f603738da977104d60b7bb51f8198718e3c8.jpg";
   }  
}
window.setInterval(f, 500);
</script></div>

<div align ="middle">
	<img src="https://gss0.baidu.com/9vo3dSag_xI4khGko9WTAnF6hhy/zhidao/pic/item/aa64034f78f0f736b693aa9d0155b319ebc41338.jpg" width=300>
</div><br></br>
'''

#login button
loginButton = '''<FORM METHOD="LINK" ACTION="''' + baseURL + '''/login" ALIGN = "right">
<INPUT TYPE="submit" VALUE="Login">
</FORM></body></html>'''
#logout button
logoutButton = '''<FORM METHOD="LINK" ACTION="''' + baseURL + '''/logout" ALIGN = "right">
<INPUT TYPE="submit" VALUE="Logout">
</FORM></body></html>'''
#back button
backButton = '''<FORM METHOD="LINK" ACTION="''' + baseURL + '''/back" ALIGN = "right">
<INPUT TYPE="submit" VALUE="Back">
</FORM></body></html>'''



page_ID = 0

#cache
cache_opts = {
        'cache.type': 'file',
        'cache.data_dir': '/tmp/cache/data',
        'cache.lock_dir': '/tmp/cache/lock'
}

#cache = CacheManager(**parse_cache_config_options(cache_opts))

session_opts = {
        'session.type': 'file',
        'session.cookie_expires': 300,
        'session.data_dir': './data',
        'session.auto': True,
}
bottleApp = app()
App = SessionMiddleware(bottleApp, session_opts)


#error 404
@error(404)
def error404(error):
        return '''This page or file does not exist. <br><br> Please visit <a href="''' + baseURL + '''"> Home </a> for a new search.'''

@route('/','GET')
def start():
        global baseURL
        baseURL = '{}'.format(request.url)
        if map_flag == 1:
                html = frontend[1]
        elif image_flag ==1:
                html = frontend[2]
        else:
                html = frontend[0]
        session = request.environ.get('beaker.session')
        if session == None:
                redirect('/home_anonymous')
        else:
                redirect('/user_home')





@route('/login')
def login():
        flow = flow_from_clientsecrets("client_secrets.json", scope = scope, redirect_uri = redirect_uri, prompt = 'select_account')
        uri = flow.step1_get_authorize_url()
        redirect(str(uri))

@route('/logout')
def logout():
        session = request.environ.get('beaker.session')
        if 'credentials' in session:
                del session['credentials']
        redirect("/home_anonymous")

@route('/back')
def back():
        redirect(baseURL)

# different searching modes
@route('/map')
def map():
        global map_flag
        global image_flag
        map_flag = 1
        image_flag = 0
        redirect(baseURL)

@route('/all')
def all():
        global map_flag
        global image_flag
        map_flag = 0
        image_flag = 0
        redirect(baseURL)

@route('/image')
def all():
        global map_flag
        global image_flag
        image_flag = 1
        map_flag = 0
        redirect(baseURL)
 
@route('/home_anonymous')
def anonymous():
        return html + loginButton + backButton + "<br><br>" + greeting_anime + searchHTML_mid

@route('/user_home')
def user_home():
        session = request.environ.get('beaker.session')
        email = "no user logged in"
        if 'email' in session:
                email = session['email']

        command_top_home = '<div align="middle"><table id="history"><tr><th>Top 20</th><th>words list</th></tr></div>'
        i = 0
        if len(topdic) != 0:
                for key in topdic.keys():
                        if key == ' ':
                                topdic.pop(key)
                        if i>=20:
                                break
                        else:
                                command_top_home = command_top_home+'<tr><td>'+str(key)+'</td><td>'+str(topdic[key])+'</td></tr>'
                                i = i+1
        command_top_home = command_top_home + '</table>'
        return html + logoutButton + backButton + "<br><br>" + greeting_anime + searchHTML_mid + command_top_home +userinfo + email + '</p>'


#search page - includes an html form with one text box for search input
@route('/redirect')
def search():
        code = request.query.get("code", "")
        if(code == ""):
                redirect('/')

        flow = OAuth2WebServerFlow(client_id='108597482889-qcfp3i7n6iuec7srt00spf8ln96qad6h.apps.googleusercontent.com', client_secret = 'JznB0QNm9C9p1n9wtFHjvyQg', scope = scope, redirect_uri = redirect_uri)
        credentials = flow.step2_exchange(code)
        session = request.environ.get('beaker.session')
        session['credentials'] =credentials
        token = credentials.id_token['sub']
        session['access_token'] = token

        session.save()

        #retrieve user data with the access token
        http = httplib2.Http()
        http = credentials.authorize(http)

        #get user email
        users_service = build('oauth2', 'v2', http=http)
        user_document = users_service.userinfo().get().execute()
        user_email[0]= user_document['email']
        session['email']= user_email[0]
        #get username
        #users_service = build('plus', 'v1', http=http)
        #profile = users_service.people().get(userId='me').execute()
        #user_name = profile['displayName']
        #user_image = profile['image']['url']

        sorted(topdic.items(), key=lambda e:e[1], reverse=True)
        command_top = '<div align="middle"><table id="history"><tr><th>Top 20</th><th>words list</th></tr></div>'
        i = 0
        if len(topdic) != 0:
                for key in topdic.keys():
                        if key == ' ':
                                topdic.pop(key)
                        if i>=20:
                                break
                        else:
                                command_top = command_top+'<tr><td>'+str(key)+'</td><td>'+str(topdic[key])+'</td></tr>'
                                i = i+1
        command_top = command_top + '</table>'
        return html + backButton + logoutButton  + "<br><br>" + greeting_anime + searchHTML_mid + command_top +userinfo + user_email[0] + '</p>'


@route('/search', method='GET')
def do_search():

        userinput = request.query.userinput
        search_dic = countdic(userinput)

        #split user search into words and count the occurance of each word using collections.Counter
        #words = userinput.split(" ")
        #wordcounter = collections.Counter(words)

        #Create a new string printWordCounter which holds the text for an HTML table include all the words and the number of times they occur in the search
        command = """<table border = "0"><tr><th align = "left">Word</th><th>Count</th></tr>"""
        for i in search_dic:
            command = command + '<tr><td>' + str(i) + '</td><td>' + str(search_dic[i]) + '</td></tr>'
        command = command + '</table>'
        if map_flag == 1:
            req = userinput.replace(' ','+')
            url = mapURL + req
            redirect(url)
        else:
            redirect('/search/'+ str(page_ID) +'/'+ userinput)

@route('/search/<pageid>/<userinput>')
def searchpages(pageid, userinput):
        #get results from  table
        words = userinput.split(" ")
        searchWord = (words[0])
        url = []
        if image_flag == 0:
                url = gd.word_to_urls(searchWord)
        elif image_flag ==1:
                url = gd.word_to_img(searchWord)
	
	if url == "wrong":
		session = request.environ.get('beaker.session')
            if session == None:
                return html + loginButton + backButton + greeting + searchHTML + "<br><br><font color='white'>"  + userinput + " not found.</font>"
            else:
                return html + logoutButton + backButton + greeting + searchHTML + "<br><br><font color='white'>"  + userinput + " not found.</font>"
		
           
        
        page = []
        temp_page=[]
        #The SELECT DISTINCT statement is used to return only distinct values

        #put urls into page, 5 urls are in one index
        if len(url)<=5:
                for item in url:
                        item = '<tr><td><font size=5><a href="' + item + '" target="_blank">'+ item + "</a><font></td></tr>"
                        temp_page.insert(len(temp_page), item)
                        page[0]=[temp_page]
        else:
                counter =0
                page_num =  0
                for item in url:
                        item = '<tr><td><font size=5><a href="' + item + '" target="_blank">'+ item + "</a><font></td></tr>"
                        temp_page.insert(len(temp_page), item)
                        counter +=1
                        if counter==5:
                                page.insert(len(page),temp_page)
                                page_num +=1
                                counter = 0
                                temp_page = []
                if counter != 0:
                        page.insert(len(page),temp_page)




        if len(page) ==0:
            session = request.environ.get('beaker.session')
            if session == None:
                return html + loginButton + backButton + greeting + searchHTML + "<br><br><font color='white'>"  + userinput + " not found.</font>"
            else:
                return html + logoutButton + backButton + greeting + searchHTML + "<br><br><font color='white'>"  + userinput + " not found.</font>"


        pageList = "ALL RESULTS SHOWN:<br>"+"""<table border = "0"><tr>"""
        for pagenum in range(0, len(page)):
                pageList += '<th><font size=5><a href= "' + baseURL + '/search/' + str(pagenum) + '/' + userinput + '">' + str(pagenum+1) + "<a><font></th>"

        pageList += "</tr>"

        if len(page) != 0:
            Result = """<table border = "0"><tr><th align = "left"><font size=5>Search Results<font></th></tr>"""
            urlHTML = " ".join(page[int(pageid)])
            session = request.environ.get('beaker.session')
            if 'credentials' not in session:
                return html + loginButton + backButton + greeting + "<br><br>" + searchHTML + "<br><br>" +  "<br><br><font size=5>%s %s</table></font<br><br>%s"  %(Result, urlHTML, pageList)
            else:
                return html + logoutButton + backButton + greeting + "<br><br>" + searchHTML + "<br><br>" +  "<br><br><font size=5>%s %s</table></font<br><br>%s"  %(Result, urlHTML, pageList)
        else:
                redirect('/err')

run(host='0.0.0.0',port='80',debug=True)


