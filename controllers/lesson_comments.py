# -*- coding: utf-8 -*-
"""Web2Py pagal puslapio URL iškviečia funkciją atitinkamame faile ("controller"'yje)."""

from plugin_introspect import tutor, menu


def index( ):
    response.view = 'default/index.html'
    response.title = "Temos"
    return dict(content=menu())


@tutor(extra_files=['models/chat.py'])
def forma():
    
    record = None
    if request.args:
        msg_id = request.args(0)
        record = db.chat(msg_id) 
    
    form = SQLFORM(db.chat, record).process()
    if form.accepted:
        response.flash = "Naujas įrašas įterptas"
    elif form.errors:
        response.flash = "Pataisykite duomenis"
    
    return CAT(
            LOAD(f='list', vars={'plain':1}, ajax=True), # užkrauna kitos kontrolerio funkcijos rezultatą 
            form, 
           )
    
    
@tutor(extra_files=['models/chat.py']) #, 'views/lesson_comments/list_chat.html'
def list():
    messages = []
    for msg in  db().select(db.chat.ALL):
        messages.append( DIV( STRONG( msg.vardas ) , ": ", BR(),
                              SPAN(msg.laikas, 
                                    A(" [edit]", _href=URL('forma', args=[msg.id] ) ),
                                    _class="neesme"
                              ),  
                             
                              DIV( XML( msg.atsiliepimas.replace('\n', '<br>'))   ), 
                              _class="msg"
        ) )
        
    style=STYLE("""
        .neesme {color: grey; font-size: 0.7em}
        .msg {margin-bottom: 10px;}
        
        """)
        
    
    return CAT(  # CAT sujungia kelis elementus
                UL( messages ), style, 
            )
            
            # LOAD(f='add_msg', vars={'plain':1}) # užkrauna kitos kontrolerio funkcijos rezultatą 
            
