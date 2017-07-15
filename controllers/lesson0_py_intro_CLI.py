# -*- coding: utf-8 -*-
"""Web2Py pagal puslapio URL iškviečia funkciją atitinkamame faile ("controller"'yje)."""

######## fake print ##########
from __future__ import print_function
real_print = print
OUT = []
def print(*args, **kwargs):
    real_print( *args, **kwargs )
    OUT.append( ' '.join(map(str, args) ) )

def flush_print(sep="\n"):
    global OUT
    result = sep.join( OUT )
    OUT = []
    return PRE(result, _style="color:black; border:none; background:none")

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
def _kintamieji():   
    a = 5
    b = 3 
    print( a, b )
    a = a + b
    print( a )
    return flush_print() 
    
@tutor(imitateCLI=True)
def kintamieji_1():   
    a = 5
    b = 3 ###PLACEHOLDER:--> ? 
    return a * b 
    
@tutor(imitateCLI=True)
def money():  
    
    money = 99
    print( money )
    
    money = money + 1 # padidinam kintamąjį
    print( money ) 
    
    return flush_print()  # could be automatically decorated
    
    
    
    
    
    
@tutor(imitateCLI=True)
def _duomenu_tipai():   
    a = 5
    b = 3.14
    c = "hello" + ' world' # tekstas gali būt ir tarp viengubų ir tarp dvigubų kabučių
    print( a, type(a) )
    print( b, type(b) )
    print( c, type(c) )
    return flush_print()

 
@tutor(imitateCLI=True)
def duomenu_tipu_konvertavimas():   
    a = 5
    b = 3.14
    c = "6.66"

    # konvertuojam
    a_txt = str( a ) # skaičių į tekstą
    
    b_int = int( b ) # skaičių su kableliu į sveiką (numeta trupmeną)
    
    c_float = float( c ) # tekstą į skaičių
    
    # repr - reiškia "represent"  -- kaip reikšmė atrodytų programos kode 
    print( repr(a_txt) )
    print( repr(b_int) )
    print( repr(c_float) )
    
    return flush_print()

@tutor(imitateCLI=True)
def datos_tipas():
    import datetime
    
    jonines  = datetime.date(2017, 6, 23)
    
    return jonines

@tutor(imitateCLI=True)
def datos_tipas_siandien():
    import datetime
    
    siandien  = datetime.date.today()
    
    return siandien
    

@tutor(imitateCLI=True)
def datos_skirtumas():
    """raskite kelinta dabar metų diena"""
    import datetime

    NM_riba  = datetime.date(2016, 12, 31) # metų riba
    siandien  = datetime.date.today()
    
    return (siandien - NM_riba).days  


@tutor(imitateCLI=True)
def _tekstas():
    # tekstą galima sudėti
    a = "labas"
    b = "rytas"
    
    return a + " " + b


@tutor(imitateCLI=True)
def teksto_dauginimas():
    # tekstą galima padauginti
    a = "labas"
    
    return (a + " ") * 3


@tutor(imitateCLI=True)
def multiline_tekstas():
    bla = """
        trigubos kabutės leidžia programoje
        rašyti tekstą per kelias eilutes.
        
        Taip pat jos naudojamos kaip komentarai programoje ("docstrings" - dokumentacijos tekstai)
        """
    
    return PRE( bla ) ###REPLACE return bla
    
@tutor(imitateCLI=True)
def tekstas_plius_skaicius_klaida():
    """Tiesiogiai sudėt 
    teksto ir skaičiaus 
    nepavyks - bus klaida
    """
    
    a = "labas"
    b = 10
    
    c = a + b

@tutor(imitateCLI=True)
def tekstas_plius_skaicius():
    """Bet galima skaičių pirmiau paverst tekstu ;) 
    """
    
    a = "labas"
    b = 10
    
    c = a + str(b)
    return c
    
@tutor(imitateCLI=True)
def _salygos_sakiniai():
    
    money = 5  # kiek turime eurų
    
    if  money  > 10:  # netenkinama sąlyga 
        print( "I can buy a stake" ) # nevykdoma

    if  money  > 2:   # tenkinama
        print( "I can buy a beer" ) # vykdoma

    return flush_print()

@tutor(imitateCLI=True)
def else_():
    
    money = 1000  # kiek turime eurų
    
    if  money  >= 1000000:
        print( "I am milionnaire!" )
    
    else: # reiškia "kitais atvejais" 
        print( "money is not everything..." ) 
        
    return flush_print()

@tutor(imitateCLI=True)
def elif_else():
    
    money = 1000  # kiek turime eurų
    
    if  money  >= 1000000:
        print( "I am milionnaire!" )
        
    elif money >= 1000:  # reiškia "else if" 
                         # žiūrima, kai netinka ankstesnė(s) sąlyga/os
        print( "I have some money" ) 
    
    else:  # jei netenkinamos ankstesnės sąlygos
        print( "I am running out of money.." ) 
        
    return flush_print()

