# -*- coding: utf-8 -*-
""""""

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

def __TEST_fake_print():        
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
def _kintamieji():   
    a = 5
    b = 3 ###PLACEHOLDER:--> ? 
    return a * b 

    
@tutor(imitateCLI=True)
def money_increase():  
    
    money = 99
    print( money )
    
    money = money + 1 ###PLACEHOLDER:--> money = money ? ? 
    print( money ) 
    
    return flush_print()  
    
@tutor(imitateCLI=True)
def money_spend():  
    
    money = 100
    beer = 2
    bread = 1
    
    # let's buy bread
    money = money - bread ###PLACEHOLDER:--> money = money ? ? 
    print( money ) 

    # let's buy 3 beer
    money = money - 3*beer ###PLACEHOLDER:--> money = money ? ? 
    print( money ) 
    
    return flush_print()      
      
    
@tutor(imitateCLI=True)
def _duomenu_tipai():   
    a = 5     # sveikas skaičius - "integer" (trumpina: int)
    b = 3.14  # slankaus kablelio - "floating point" (trumpina: float)
    c = "hello" + ' world' # teksto eilutė - "string" (trumpina: str)
                           # tekstą žymi viengubos arba dvigubos kabutės
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
    a_txt = str( a ) # skaičių į tekstą ("string" tipą)

    b_int = int( b ) # skaičių su kableliu į sveiką (numeta trupmeną)
    
    c_float = float( c ) # tekstą į skaičių
    
    # repr - reiškia "represent"  -- kaip reikšmė atrodytų programos kode 
    print( repr(a_txt) )
    print( repr(b_int) )
    print( repr(c_float) )
    
    return flush_print()

@tutor(imitateCLI=True)
def tekstas_plius_skaicius_klaida():
    # Tiesiogiai sudėt  teksto ir skaičiaus nepavyks - bus klaida
    
    a = "labas"
    b = 10
    
    c = a + b

@tutor(imitateCLI=True)
def tekstas_plius_skaicius():
    
    # Bet galima skaičių pirmiau paverst tekstu (žr užpraitą pvz ;)  
    
    a = "labas"
    b = 10
    
    c = a + str(b)  ###PLACEHOLDER:--> c = a + ?  
    return c


    

@tutor(imitateCLI=True)
def datos_tipas():
    import datetime

    jonines  = datetime.date(2017, 6, 23)
    print( jonines )
    
    siandien  = datetime.date.today()
    print( siandien )
    
    # datos aritmetika: kelinta dabar metų diena? 
    metu_riba  = datetime.date(2016, 12, 31) 
    skirtumas_dienomis = (siandien - metu_riba).days  
    print( skirtumas_dienomis )

    return flush_print()


@tutor(imitateCLI=True)
def _tekstas():
    # tekstą galima sudėti
    a = "labas"
    b = "rytas"
    
    mintis = a + " " + b
    print( mintis )
    print( "teksto ilgis:", len( mintis ) )  # "len" nuo "length"
    
    return flush_print()

@tutor(imitateCLI=True)
def teksto_dauginimas():
    # tekstą galima padauginti
    a = "labas"
    b = (a + " ") * 3 ###PLACEHOLDER:--> b = (a + " ") ?

    return b

@tutor(imitateCLI=True)
def multiline_tekstas():
    bla = """
        trigubos kabutės leidžia programoje
        rašyti tekstą per kelias eilutes.
        
        Taip pat jos naudojamos kaip komentarai programoje ("docstrings" - dokumentacijos tekstai)
        """
    
    return PRE( bla ) ###REPLACE print( bla )
    
    
@tutor(imitateCLI=True)
def _salygos_sakiniai():
    
    money = 5  # kiek turime eurų
    
    if  money  > 10:  # netenkinama sąlyga 
        print( "I can buy a stake" ) # nevykdoma

    if  money  > 2:   # tenkinama ###PLACEHOLDER:--> ? > 2:  # tenkinama
        print( "I can buy a beer" ) # vykdoma

    return flush_print()


@tutor(imitateCLI=True)
def else_():
    
    money = 1000  # kiek turime eurų
    
    if  money  >= 1000000:
        print( "I am milionnaire!" )
    
    # kitu atveju
    else:  ###PLACEHOLDER:--> ?
        print( "money is not everything..." ) 
        
    return flush_print()

@tutor(imitateCLI=True)
def elif_else():
    
    money = 1000  # kiek turime eurų
    
    if  money  >= 1000000:
        print( "I am milionnaire!" )
        
    # reiškia "else if"  -- žiūrima, kai netinka ankstesnė(s) sąlyga/os
    elif money >= 1000:  ###PLACEHOLDER:--> ? money >= 1000?
        print( "I have some money" ) 
    
    # jei netenkinamos ankstesnės sąlygos
    else:  ###PLACEHOLDER:--> ?
        print( "I am running out of money.." ) 
        
    return flush_print()

