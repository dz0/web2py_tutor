# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
from plugin_introspect import tutor, menu as tutor_menu

def index():
    redirect(URL('pages', args='one.html'))

@tutor( extra_files=['views/pages/one.html', 'views/pages/two.html'] )
def pages():
    if request.args:   
        page = request.args[0]  # could adapt another page extension/ending here 
    else: 
        return DIV("No page found, please choose :",  # could have default or so..
                UL( A('one.html', _href='one.html') , 
                    A('two.html', _href='two.html') , 
                  )
                )    
    return response.render( 'pages/'+page, {} ) # we just pick the view according to given page 