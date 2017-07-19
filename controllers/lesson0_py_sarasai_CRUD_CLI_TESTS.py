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



from plugin_introspect import tutor, menu

def index( ):
    response.view = 'default/index.html'
    response.title = "Temos"
    return dict(content=menu())


@tutor(imitateCLI=True)
def sarasai():
    
    Finansai = [ 10, 12, 0, 20, 8, -25, -5 ]  # pajamos/išlaidos per savaitę
    
    print("Finansai", Finansai)  
    
    # susumuojam balansą
    balansas = sum(Finansai) ###PLACEHOLDER:--> balansas = ?(Finansai) 
    print("Dabar turim:", balansas ) 

    return flush_print()

@tutor(imitateCLI=True)
def vidurkis():
    
    Pazymiai = [6, 8, 4, 10] 

    suma = sum( Pazymiai )
    kiek = len( Pazymiai )  # asdf  ###PLACEHOLDER:--> kiek = ?(Pazymiai)  # hint: sąrašo ilgis
    print("Vidurkis:", suma / kiek ) 

    return flush_print()
    
@tutor(imitateCLI=True)
def perrinkimas_grafikas():
    
    Pazymiai = [6, 9, 3, 7] 
    
    print( "Stulpelinė diagrama (horiz.):" )
    
    for pazymys in Pazymiai: # imam po pažymį iš sąrašo 
        # nurodėm kintamojo pavadinimą "pazymys",
        # ir su juo atitraukę nuo krašto darom, ką norim 
        print( pazymys, "#" * pazymys) # spausdinam reikšmę ir tiek pat simbolių

    return flush_print()


            
@tutor(imitateCLI=True)
def saraso_pertvarkymas():
    money = [10, 2, 5]  # centai...
    
    money.append( 100 ) # gavom eurą!
    print( money )
    
    money[1] = 30  # pakoreguojam antrąją reikšmę
    print( money )
    
    del money[0]   # pašalinam pirmąją reikšmę
    print( money )
    
    money.insert(0, 13) # į priekį įterpiam 13
    print( money )
    
    return flush_print()
            
@tutor(imitateCLI=True)
def filtravimas_i_nauja_sarasa():
    
    Pazymiai = [6, 9, 3, 7] 
    riba = 5
    
    # Norim surašyt didesnius už vidurkį į atskirą sąrašą
     
    didesni = [] # paruošiam naują sąrašą ###PLACEHOLDER:-->  didesni = ? # paruošiam naują sąrašą
    
    for paz in Pazymiai:  ###PLACEHOLDER:--> for ? :
        if paz > riba: ###PLACEHOLDER:--> if 
            didesni.append( paz ) ###PLACEHOLDER:--> papildom sąrašą
    
    return didesni


@tutor(imitateCLI=True)
def elementu_numeravimas():
    pass
    


@tutor(imitateCLI=True)
def lygiagretus_perrinkimas():
    pass
    


    
#####
def _funkcijos():
    pass
    
