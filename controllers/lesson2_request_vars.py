# -*- coding: utf-8 -*-
from plugin_introspect import show_menu_and_code, menu

def index(): return menu()

@show_menu_and_code
def GET_vars():
    
    duomenys = request.vars  # request reiškia kreipimąsi į serverį. O "vars" -- atseit "variables" (pažodžiui būtų "kintamieji", bet realiai -- tiesiog duomenys su vardais) .
    
    link1 = URL( vars={'a':5, 'b':"labas" } ) 
    link2 = URL( vars={ 'z':[1, 3, 5] } ) 
    
    return CAT( 
            XML("GET parametrai paduodami per nuorodą. Išbandykite nuorodas ir žiūrėkite, kaip keičiasi adreso laukelis ir gauti kintamieji <br/> <br/>"),
            CAT( "Gauti duomenys: ", BEAUTIFY( duomenys ) if duomenys else "nieko..."),

            UL(
                A(link1, _href=link1 ) , 
                A(link2, _href=link2 ),
                A(URL(), _href=URL() )  # tiesiog nuoroda, iškviečianti dabartinę valdiklio funkciją 
            )
        )


@show_menu_and_code
def FORM_POST_vars():
    
    duomenys = request.vars  
    
    form = FORM( 
                INPUT(_name="kas"),     # duomenų įvedimo laukelis (pagal nutylėjimą,  _type="text")
                INPUT(_type="submit", _value="OK")   # siuntio mygtukas
           )
    
    return CAT( 
            XML("POST parametrai paduodami per formos laukus. Įveskite ką nors... <br/> <br/>"),
            CAT( "Gauti duomenys: ", BEAUTIFY( duomenys ) if duomenys else "nieko..."),

            DIV("Forma: ", form)
        )


@show_menu_and_code
def FORM_POST_vars_task():
    
    duomenys = request.vars  
    
    form = FORM( 
                "Kas:", INPUT(_name="kas"),    
                BR(),
                "Kiek:",  INPUT(_name="kiek", _type="number"),    
                BR(),
                INPUT(_type="submit", _value="OK")   # siuntio mygtukas
           )
    
    return CAT( 
            XML("POST parametrai paduodami per formos laukus. Įveskite ką nors... <br/> <br/>"),
            CAT( "Gauti duomenys: ", BEAUTIFY( duomenys ) if duomenys else "nieko..."),

            DIV("Forma: ", form)
        )



