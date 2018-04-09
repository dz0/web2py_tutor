# -*- coding: utf-8 -*-
# http://www.web2py.com/init/default/examples
from plugin_introspect import tutor, menu

def index(): return menu()

@tutor

def hello3():
    return dict(message=T("Hello World"))


def hello5():
    return HTML(BODY(H1(T('Hello World'),_style="color: red;"))).xml() # .xml to serialize

def hello6():
    response.flash=T("Hello World in a flash!")
    return dict(message=T("Hello World"))

def status():
    return dict(toobar=response.toolbar())

def raisehttp():
    raise HTTP(400,"internal error")
    
def raiseexception():
    1/0
    return 'oops'

def makejson():
        return response.json(['foo', {'bar': ('baz', None, 1.0, 2)}])


def redirectme():
    redirect(URL('hello3'))
    
def rss_aggregator():
    import datetime
    import gluon.contrib.rss2 as rss2
    import gluon.contrib.feedparser as feedparser
    d = feedparser.parse("http://rss.slashdot.org/Slashdot/slashdot/to")

    rss = rss2.RSS2(title=d.channel.title,
    link = d.channel.link,
    description = d.channel.description,
    lastBuildDate = datetime.datetime.now(),
    items = [
       rss2.RSSItem(
         title = entry.title,
         link = entry.link,
         description = entry.description,
         # guid = rss2.Guid('unkown'),
         pubDate = datetime.datetime.now()) for entry in d.entries]
       )
    response.headers['Content-Type']='application/rss+xml'
    return rss2.dumps(rss)


def ajaxwiki():
    form=FORM(TEXTAREA(_id='text',_name='text'),
              INPUT(_type='button',_value='markmin',
              _onclick="ajax('ajaxwiki_onclick',['text'],'html')"))
    return dict(form=form,html=DIV(_id='html'))

def ajaxwiki_onclick():
    return MARKMIN(request.vars.text).xml()



def counter():
    session.counter = (sesstion.counter or 0) + 1
    return dict(counter=session.counter)

def beautify():
    dict(message=BEAUTIFY(dict(a=1,b=[2,3,dict(hello='world')])))
    
    
def form():
    form=FORM(TABLE(TR("Your name:",INPUT(_type="text",_name="name",requires=IS_NOT_EMPTY())),
                    TR("Your email:",INPUT(_type="text",_name="email",requires=IS_EMAIL())),
                    TR("Admin",INPUT(_type="checkbox",_name="admin")),
                    TR("Sure?",SELECT('yes','no',_name="sure",requires=IS_IN_SET(['yes','no']))),
                    TR("Profile",TEXTAREA(_name="profile",value="write something here")),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.accepts(request,session):
        response.flash="form accepted"
    elif form.errors:
        response.flash="form is invalid"
    else:
        response.flash="please fill the form"
    return dict(form=form,vars=form.vars)
