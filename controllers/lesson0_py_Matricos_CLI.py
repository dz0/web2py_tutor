# -*- coding: utf-8 -*-
""""""

######## fake print ##########
from __future__ import print_function  # if print is function, we can override it
real_print = print   # save original function to different name

OUT = []  # global buffer , dirty hack

def print(*args, **kwargs):
    real_print( *args, **kwargs )  # call original
    OUT.append( ' '.join(map(str, args) ) )   # save to buffer

def flush_print(sep="\n"):
    """Flushes the OUT buffer and returns concatenated lines

    sep - newline separator"""

    global OUT
    result = sep.join( OUT )
    OUT = []
    return PRE(result, _style="color:black; border:none; background:none")

######## end fake print ##########



from plugin_introspect import tutor as original_tutor, menu
from tools import call_or_redirect
import urllib


# tutor = auth.requires_login(original_tutor)
def tutor (*args, **kwargs):
    if auth.is_logged_in():
        return original_tutor(*args, **kwargs)
    else:
        next = auth.here()
        session.flash = response.flash
        return call_or_redirect(auth.settings.on_failed_authentication,
                                auth.settings.login_url + '?_next=' + urllib.quote(next))


def index( ):
    response.view = 'default/index.html'
    response.title = "Temos"
    return dict(content=menu())

########### tasks

@tutor(imitateCLI=True)
def matricos():
    M = [
            [ 'O', 'X', ' ' ],
            [ 'O', 'X', 'O' ],
            [ 'X', ' ', ' ' ]
        ]
    M[2][1] = 'O'
    
    # atspausdinam matricą (po eilutę)
    for row in M:
        print( row )
        
    return flush_print()
        
        
@tutor(imitateCLI=True)
def criss_cross2():
    M = [
            [ 'O', 'X', ' ' ],
            [ 'O', 'X', 'O' ],
            [ 'X', ' ', ' ' ]
        ]
    M[0][2] = 'O'  ###PLACEHOLDER:--> M[?][?] = 'O'
    M[2][2] = 'X'  ###PLACEHOLDER:--> M[?][?] = 'X'
    
    # atspausdinam matricą (po eilutę)
    for row in M:
        print( row )
        
    return flush_print()


@tutor(imitateCLI=True)
def islaidos():
    columns = ['Food', 'Transport', 'Housing']
    
    M = [
            [ 10, 30, 54 ],
            [ 42, 0, 0 ],
            [ None, None, None ],  # None dažnai reiškia, kad nėra duomenų
            [ 2, 14, 8 ]
        ]
    
    # atspausdinam tik maisto išlaidas
    print( columns[0] )   # antraštė
    
    for row in M:          # imam po eilutę
        print( row[0] )    # ir joje spausdinam 0 el.

    return flush_print()


@tutor(imitateCLI=True)
def islaidos_fun1():
    columns = ['Food', 'Transport', 'Housing']
    
    M = [
            [ 10, 30, 54 ],
            [ 42, 0, 0 ],
            [ None, None, None ],  
            [ 2, 14, 8 ]
        ]
    
    def print_col(name):
        nr = columns.index(name) ###PLACEHOLDER:--> nr = columns.???(name)  # suranda, elemento "name" vietą/numerį sąraše 
        for row in M:         ###PLACEHOLDER:--> ? # imam po eilutę
            print( row[nr] )  ###PLACEHOLDER:--> ? # spausdinam jos nr-tąjį elementą
        
    # atspausdinam tik maisto išlaidas
    print_col('Housing')  # iškviečiam funkciją
    print()  # padarys tuščia eilutę
    print_col('Food')
    
    return flush_print()


