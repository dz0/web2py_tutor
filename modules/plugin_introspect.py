# -*- coding: utf-8 -*-


from gluon import current
from gluon.html import URL, UL, A, B, CAT, PRE, CODE, BR, SPAN
from gluon.admin import apath
from gluon.compileapp import find_exposed_functions

import inspect
import re
import os

def lessons_menu():
    
    request = current.request
    
    app = request.application
    c = request.controller
    dirpath = apath('%s/controllers' % app, r=request)    
    
    controllers  = [ c[:-len('.py')]   for c in os.listdir( dirpath )      if c.startswith('lesson') and c.endswith('.py')]
    
    menu = [  A(  c[len("lesson"):].title(),     _href=URL(c, 'index') )     for c in controllers ]
    
    return UL(menu)
        
def exposed_functions( bla=None ):
    
    request = current.request
    
    app = request.application
    c = request.controller
    fpath = apath('%s/controllers/%s.py' % (app, c), r=request)
    data = open(fpath).read()
    
    items = find_exposed_functions(data)
    if 'get_active_code' in items:    items.remove( 'get_active_code' )
    return items
    
def menu( ): 
    """gives links to all exposed functions except currently used"""
    items = exposed_functions( )
    request = current.request
    return UL( [
                  item!=request.function 
                      and SPAN(   A( item , _href=URL(item)),  "*"*is_task(item) ) 
                  or item    
                  for item in items
              ] )
    
def is_task(fname):
    return '_task' in fname    or    fname.startswith('task')

def show_code( f ):
    def result():
        return CAT( 
                    f(),
                    BR(),  
                    SEMIHIDDEN_CONTENT("[ Kodas ]", get_active_code(f) ) if not is_task(f.__name__) else   "Užduotis: sugalvok kodą šiam pavyzdžiui"
                )
        
    return result

def show_menu( f ):
    def result():
        return CAT(  
                    f(), 
                    BR(),  
                    SEMIHIDDEN_CONTENT("[ Meniu ]", menu() ), 
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
    request = current.request
    
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
