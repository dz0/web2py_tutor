# -*- coding: utf-8 -*-
# try something like
import inspect
import re

def index( html=True ): 
    from gluon.admin import apath
    from gluon.compileapp import find_exposed_functions
    app = request.application
    c = request.controller
    fpath = apath('%s/controllers/%s.py' % (app, c), r=request)
    data = open(fpath).read()
    
    items = find_exposed_functions(data)
    if 'get_active_code' in items:    items.remove( 'get_active_code' )
    # items.remove( 'index' )
    if html:
        return UL( [item!=request.function and A(item, _href=URL(item)) or item    for item in items] )
    else:
        return items

def show_code( f ):
    def result():
        return CAT(
                    f(), 
                    SEMIHIDDEN_CONTENT("Kodas:", get_active_code(f) )
                )
        
    return result

def show_menu( f ):
    def result():
        return CAT(  
                    f(), 
                    SEMIHIDDEN_CONTENT("Meniu:", index() ), 
               )
    return result

def show_code_and_menu( f ):
    return show_menu(   show_code(  f  )  )

def SEMIHIDDEN_CONTENT(name, content):
    js_toggle = """
    d=this.nextElementSibling.style.display; this.nextElementSibling.style.display = d=='block'? 'none': 'block';
    """
    return CAT( 
        BR(),
        SPAN( name, _onclick=js_toggle, _style="cursor:hand"),
        SPAN( content, _style="display:none" )
    )

def get_active_code(f=None):  
    """Gets code of either the request.function (it it is the callee) or the provided function"""
    
    if f is None:
        name = inspect.currentframe().f_back.f_code.co_name
        if request.function == name:  # if the callee is active function
            f = globals()[request.function]
        else:
            return ""# we don't have info about function
    

    lines, start_line = inspect.getsourcelines( f ) 
    # code = inspect.getsource( f ) 
    code = ''.join( lines )
    
    # remove some function calls from code
    code = re.sub(r",\s*?get_active_code\(\s*?\)", "", code) 
    code = re.sub(r",\s*?index\(\s*?\)", "", code) 
    code = re.sub(r"^@show_.+?$", "", code, flags=re.MULTILINE) 
    # code = re.sub(r"@show_menu", "", code) 
    # code = re.sub(r"@show_code", "", code) 
    
    return  CODE(code, language="python", link='/examples/global/vars/', counter=start_line)

    
    



@show_code_and_menu
def HTML_helpers1():
    return P( "labas ", B("pasauli")  )
    
@show_code_and_menu

def HTML_helpers2():
    return DIV( SPAN("labas ", _style="color:blue"), B("pasauli") )

@show_code_and_menu
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
            )
        )


# for fname in index(html=False):
    # print fname
    # fun = globals()[fname]
    # print fun
    # fun = show_code( fun )
    # fun = show_menu( fun )
