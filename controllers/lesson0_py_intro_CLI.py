# -*- coding: utf-8 -*-
"""Web2Py pagal puslapio URL iškviečia funkciją atitinkamame faile ("controller"'yje)."""

######## fake print ##########
from __future__ import print_function
real_print = print
OUT = []
def print(*args, **kwargs):
    real_print( *args, **kwargs )
    OUT.append( ' '.join(map(str, args) ) )

def flush_print(sep="<br>\n"):
    global OUT
    result = sep.join( OUT )
    OUT = []
    return result

def TEST_fake_print():        
    x = 2
    print(1)
    print('ad')
    print(x, 4, 'asdf')

    real_print( flush_print(sep='\n') )
    
######## end fake print ##########



from plugin_introspect import tutor, menu

def index( ):
    response.view = 'default/index.html'
    response.title = "Temos"
    return dict(content=menu())




@tutor(imitateCLI=True)
def hello_world():    
    return "Hello, world"  

@tutor(imitateCLI=True)
def print_():  
    print( "Alio" )
    print( "Malio", 3, 2, 5 ) 
    return flush_print()  # could be automatically decorated


@tutor(imitateCLI=True)
def kintamieji_1():  
    money = 99
    print( money )
    money = money + 1
    print( money ) 
    return flush_print()  # could be automatically decorated
    
