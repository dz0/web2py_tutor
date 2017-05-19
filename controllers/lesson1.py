# -*- coding: utf-8 -*-
# try something like
import inspect
import re

def index(): 
    from gluon.admin import apath
    from gluon.compileapp import find_exposed_functions
    app = request.application
    c = request.controller
    fpath = apath('%s/controllers/%s.py' % (app, c), r=request)
    data = open(fpath).read()
    
    items = find_exposed_functions(data)
    items.remove( 'get_active_code' )
    items.remove( 'index' )
    
    return UL( [item!=request.function and A(item, _href=URL(item)) or item    for item in items] )


def get_active_code():
#     return BEAUTIFY( inspect.currentframe().f_code.co_varnames )
    def SEMIHIDDEN_CONTENT(name, content):
        js_toggle = """
        d=this.nextElementSibling.style.display; this.nextElementSibling.style.display = d=='block'? 'none': 'block';
        """
        return CAT( 
            BR(),
            SPAN( name, _onclick=js_toggle, _style="cursor:hand"),
            SPAN( content, _style="display:none" )
        )
    name = inspect.currentframe().f_back.f_code.co_name
    if request.function == name:
        lines, start_line = inspect.getsourcelines( globals()[request.function] ) 
        code = inspect.getsource( globals()[request.function] ) 
        
        # remove some function calls from code
        code = re.sub(r",\s*?get_active_code\(\s*?\)", "", code) 
        code = re.sub(r",\s*?index\(\s*?\)", "", code) 
        
        return    DIV(
             
            SEMIHIDDEN_CONTENT(
                "Kodas:", 
                CODE(code, language="python", link='/examples/global/vars/', counter=start_line)
            ),            
            SEMIHIDDEN_CONTENT("Meniu:", index() )
        )
    


def HTML_helpers1():
    return PRE( "labas ", B("pasauli"), get_active_code()  )
    
def HTML_helpers2():
    return PRE( SPAN("labas ", _style="color:blue"), B("pasauli"),  get_active_code() )

def GET_vars():
    
    duomenys = request.vars  # request reiškia kreipimąsi į serverį. O "vars" -- atseit "variables" (pažodžiui būtų "kintamieji", bet realiai -- tiesiog duomenys su vardais) .
    
    link1 = URL( vars={'a':5, 'b':"labas" } ) 
    link2 = URL( vars={ 'z':[1, 3, 5] } ) 
    
    return CAT( 
        XML("GET parametrai paduodami per nuorodą. Išbandykite nuorodas ir žiūrėkite, kaip keičiasi adreso laukelis ir gauti kintamieji <br/> <br/>"),
        DIV( "Gauti duomenys:", BEAUTIFY( duomenys ) if duomenys else "nieko"),

        UL(
            A(link1, _href=link1 ) , 
            A(link2, _href=link2 ),
            A(URL(), _href=URL() ) 
        ), 
        get_active_code() 
        )

