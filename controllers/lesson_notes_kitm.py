# -*- coding: utf-8 -*-
"""Web2Py pagal puslapio URL iškviečia funkciją atitinkamame faile ("controller"'yje)."""

from plugin_introspect import tutor, menu as sys_menu


def index( ):
    response.view = 'default/index.html'
    response.title = "Temos"
    return dict(content=sys_menu())

@tutor
def reset():
    session.clear()
    redirect('notes')

@tutor
def notes():
    if session.notes is None: 
        session.notes = []
    
    note = request.vars.get('note')
    if note:
        session.notes.append(  note )
    
    rez = FORM( "žn.:", INPUT( _name="note", _type="text" ),
             BUTTON("siųsti", _type="submit")
          )
    return DIV( UL(session.notes), rez)
