# -*- coding: utf-8 -*-
"""Web2Py pagal puslapio URL iškviečia funkciją atitinkamame faile ("controller"'yje)."""

from plugin_introspect import tutor, menu


def index( ):
    response.view = 'default/index.html'
    response.title = "Temos"
    return dict(content=menu())


@tutor(extra_files=['lesson_comments.py'])
def hello():    # def - nuo žodžio "define" - aprašo funkciją
    """URL pabaigoje "hello", todėl iškviečiama funkcija "hello()" """
    return "Hello"  # grąžinamą reikšmę matote prie [ Pavyzdys ]

@tutor
def alio():   ###PLACEHOLDER:-->  def ():  
    return "Alio" ###PLACEHOLDER:-->  "Alio"

def add_comment():
    pass
    
@tutor(extra_files=['models/lesson_comments.py'])
def list_comments():
    return BEAUTIFY(  db().select(db.chat.ALL) )
