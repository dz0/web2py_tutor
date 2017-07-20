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
    
    # Norim surašyt didesnius už ribą į atskirą sąrašą
     
    didesni = [] # paruošiam naują sąrašą ###PLACEHOLDER:-->  didesni = ? # paruošiam naują sąrašą
    
    for paz in Pazymiai:  ###PLACEHOLDER:--> for paz? :
        if paz > riba: ###PLACEHOLDER:--> if 
            didesni.append( paz ) ###PLACEHOLDER:--> papildom sarasa
    
    return didesni


@tutor(imitateCLI=True)
def elementu_numeravimas():
    pass
    


@tutor(imitateCLI=True)
def lygiagretus_perrinkimas():
    pass
    

""

# https://docs.google.com/document/d/15bBFcodY6f6aZ6D2Dco94fwbo2OBeZKPS-8gq7CsPAs/edit
    
#####
def _funkcijos():
    pass
    
