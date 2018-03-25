# -*- coding: utf-8 -*-
"""Web2Py pagal puslapio URL iškviečia funkciją atitinkamame faile ("controller"'yje)."""

from plugin_introspect import tutor, menu as sys_menu


def index( ):
    response.view = 'default/index.html'
    response.title = "Temos"
    return dict(content=sys_menu())

@tutor
def intro():
    # pavyzdys, kaip įvest duomenis
    forma = FORM( "kiekis:", 
                 INPUT( _name="kiek" ),  
                 BUTTON("siųsti", _type="submit") 
              )
    # duomenys bus  request.vars (patiunint'am žodyne)
    return DIV(forma, 
               P(request.vars)
              )
    
@tutor
def start():
    session.tikslas = 7
    session.spejimai = [ ]
    return A("eik spėliot..", _href="speliok")

@tutor
def speliok():
    rez = FORM( "kiek:", INPUT( _name="kiek" ),
                 BUTTON("siųsti", _type="submit")
              )
    rez2 = "bandyk laimę.."
    if request.vars.kiek: # None, ""  veikia kaip Fasle
        kiek = int(request.vars.kiek)
        session.spejimai.append(kiek)#papildom spejimus
        if kiek == session.tikslas:
            rez2 = "Valio!"
 
    return  DIV(rez, BEAUTIFY(request.vars),
                rez2, UL(session.spejimai))
