# -*- coding: utf-8 -*-
# try something like
import inspect
import re

def exposed_functions( bla=None):
    from gluon.admin import apath
    from gluon.compileapp import find_exposed_functions
    app = request.application
    c = request.controller
    fpath = apath('%s/controllers/%s.py' % (app, c), r=request)
    data = open(fpath).read()
    
    items = find_exposed_functions(data)
    if 'get_active_code' in items:    items.remove( 'get_active_code' )
    return items
    
def index( ): 
    items = exposed_functions( )
    return UL( [item!=request.function and A(item, _href=URL(item)) or item    for item in items] )
    
def show_code( f ):
    def result():
        return CAT(
                    f(), 
                    SEMIHIDDEN_CONTENT("Kodas:", get_active_code(f) ) if '_task' not in f.__name__ else   ""
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
    
def show_menu_and_code( f ): return show_code_and_menu( f ) # alias

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

    
    

@show_menu_and_code
def HTML_helpers1():
    return CAT( "labas ", B("pasauli")  ) # CAT - nuo žodžio "ConCATenate" - tiesiog sujungia elementus 
    
@show_menu_and_code
def HTML_helpers2():
    return DIV( 
                SPAN("labas", _style="color:blue"),  # kai daugiau info, sveika ją išvardinti per eilutes
                B("pasauli") 
            )

@show_menu_and_code 
def HTML_helpers2_task1():
    return DIV( SPAN( "labas " , _style="color:blue"), 
                B("Pasauli"), 
                SPAN("!", _style="color:red") 
              )

@show_menu_and_code
def HTML_helpers2_nested():
    return SPAN( CAT( EM("labas"), " pasauli"), _style="color:blue")

@show_menu_and_code
def HTML_helpers2_task2():
    return DIV( 
                SPAN( CAT("labas ", B("Pasauli")) , _style="color:blue"), 
                SPAN("!", _style="color:red") 
           )

@show_menu_and_code
def HTML_helpers3_UL():
    return UL( "labas", "rytas", IMG(_height="20", _src="https://upload.wikimedia.org/wikipedia/en/8/80/Wikipedia-logo-v2.svg") )

@show_menu_and_code
def HTML_helpers3_task():
    return UL( 
        "labas", 
        B("rytas"), 
        SPAN("pasauli", IMG(_height="20", _src="https://upload.wikimedia.org/wikipedia/en/8/80/Wikipedia-logo-v2.svg")) 
     )

@show_menu_and_code
def HTML_helpers4_UL_list():
    daug = ['viens', 'du', 'trys']
    return UL(  daug  )


@show_menu_and_code
def HTML_helpers5_TABLE():
    daug = ['viens', 'du', 3]
    return CAT(
            TABLE(  daug, daug, daug, daug ), 
            STYLE( "table td { border:1px solid silver }" )  # bendrai stilių geriau aprašyt kokiam CSS
            )
            
@show_menu_and_code 
def HTML_helpers_BEAUTIFY_dict():
    zodynas = {'viens':1, 'du':2, 'trys':3 }
    return BEAUTIFY( zodynas )  # žodynui  paryškina raktines reikšmes

@show_menu_and_code 
def HTML_helpers_BEAUTIFY_dict_nested():
    zodynas = { 
                'LT': {'viens':1, 'du':2 }, 
                'EN': {'one': 1, 'two': 2 }
              }
    return BEAUTIFY( zodynas )  # sąrašo elementus į atskiras eilutes

            
@show_menu_and_code 
def HTML_helpers_BEAUTIFY_mixed():
    zodynas = {'viens':1, 'du':2, 'trys': [3, 6, 9]}
    return BEAUTIFY( zodynas )  # sąrašo elementus į atskiras eilutes



@show_menu_and_code
def HTML_helpers5_TABLE():
    daug = ['viens', 'du', 'trys']
    return CAT(
            TABLE(  daug, daug, daug, daug ), 
            STYLE( """
                  table {border-collapse:collapse;} 
                  table td { border:1px solid silver }""" )  # bendrai stilių geriau aprašyt kokiam CSS faile
            )


@show_menu_and_code
def HTML_helpers5_TABLE_matrix():
    maisto_islaidos = [ # matrica
                        ['pusryčiai', 'pietūs', 'vakarienė'],
                        [2,  5, 6],  
                        [0, 10, 5],  
                        [2,  5, 6], 
                        [0,  5, 3], 
                        [9,  0, 6]  
                      ]
            
    return CAT(
            TABLE( maisto_islaidos  ), 
            STYLE( """
                  table {border-collapse:collapse;} 
                  table td { border:1px solid silver }""" )  # bendrai stilių geriau aprašyt kokiam CSS faile
            )



@show_menu_and_code
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
