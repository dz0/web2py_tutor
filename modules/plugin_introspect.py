# -*- coding: utf-8 -*-

# try:
from gluon import current
from gluon.html import * # URL, UL, A, B, CAT, PRE, CODE, BR, SPAN
from gluon.admin import apath
from gluon.compileapp import find_exposed_functions
# except ImportError as e:
    # print( e )


import inspect
import re
import os

def lessons_menu(return_plain=False):
    
    request = current.request
    
    app = request.application
    c = request.controller
    dirpath = apath('%s/controllers' % app, r=request)    
    
    controllers  = [ c[:-len('.py')]   for c in os.listdir( dirpath )      if c.startswith('lesson') and c.endswith('.py')]
    controllers.sort()
    
    menu = [  A(  c[len("lesson"):].title(),     _href=URL(c, 'index') )     for c in controllers ]
    
    if return_plain:
        return controllers
    else:
        return UL(menu)
        
def exposed_functions( ):
    
    request = current.request
    
    app = request.application
    c = request.controller
    fpath = apath('%s/controllers/%s.py' % (app, c), r=request)
    data = open(fpath).read()
    
    items = find_exposed_functions(data)
    if 'get_active_code' in items:    items.remove( 'get_active_code' )
    return items
    
def menu( ): 
    """gives links to all exposed functions except currently used"""
    items = exposed_functions( )
    request = current.request
    return UL( [
                  item!=request.function 
                      and SPAN(   A( item , _href=URL(item)),  "*"*is_task(item) ) 
                  or item    
                  for item in items
              ] )
    
def is_task(fname):
    return '_task' in fname    or    fname.startswith('task')


def SEMIHIDDEN_CONTENT(name, content):
    js_toggle = ''
    """
    d=this.nextElementSibling.style.display; this.nextElementSibling.style.display = (d=='block'||d=='') ? 'none': 'block';
    """
    
    return CAT( 
        BR(),
        SPAN( name, _class="button", _onclick=js_toggle, _style="cursor:hand"),
        SPAN( content , _class="togglable")
        # SPAN( content, _class="togglable", _style="display:none" )
        , BR(), SPAN("", _class="after_togglable")
    )

def CODEMIRROR(code, language="python", task_key=None):
    """code can be text or list of texts"""
    if task_key is None:
        req = current.request
        task_key = req.controller + "/" + req.function
    return XML(current.response.render('codemirror.html', dict(code=code, language=language, task_key=task_key)))
    


def tutor(f):
    """smart decorator"""
    def result():
        content = f()
        codes = SEMIHIDDEN_CONTENT("[ Kodas ]"  if not is_task(f.__name__) else "[ Užduoties kodas ]", get_task_code(f) )  
        
        # menu
         
        menu_ = SEMIHIDDEN_CONTENT("[ Meniu ]", menu() )
        
        # next menu
        items = exposed_functions( )
        req = current.request
        nr = items.index( req.function )
        next = items[nr+1] if nr < len(items)-1  else None
        prev = items[nr-1] if nr > 0  else None
        
        a_next = A("[ Pirmyn ]", _href=URL(next))   if  next!=None  else ""
        a_prev = A("[ Atgal ]", _href=URL(prev))   if  prev!=None  else ""
        menu_ = CAT( BR(), a_prev, a_next,  BR(), menu_ )
            
        return XML(current.response.render('tutor.html', dict( content=content, codes=codes, menu=menu_) ) )
        # return  gluon.template.render(content='...', context=<vars>)
    return result 
    
def get_task_code(f, decorate=True):
    from task_parser import task
    
    code = get_active_code( f, decorate=False) # inspect.getsource( f ) 
    
    t = task(  code )
    student_lines = t['student_lines']
    
    # group lines into chunks (of not/placeholders)
    chunks = []
    
    current_chunk = ""
    placeholder_line_nrs = [p['line_nr'] for p in t['placeholders']]
    
    # save answers in session
    req = current.request
    session = current.session
    session.setdefault( 'answers', {} )
    task_key = req.controller +'/'+ req.function
    session.answers[ task_key ]  = [p['expected'] for p in t['placeholders'] ]
    
    for nr, line in  enumerate( t['student_lines'] ):
        if nr in placeholder_line_nrs:
            if current_chunk: # flush current nonplaceholder chunk
                chunks.append( current_chunk[:-1] ) # strip last newline
                current_chunk = ""

            chunks.append( "###placeholder\n\n"+ line  ) # add placeholder
            
        else:
            current_chunk += line + "\n"

    if current_chunk:  # flush nonplaceholder chunk
            chunks.append( current_chunk[:-1] )

    
    if decorate:
        return CODEMIRROR( chunks, task_key=task_key )
    else:
        return chunks

    
def get_active_code(f=None, decorate=True):  
    """Gets code of either the request.function (it it is the callee) or the provided function"""

    
    if f is None:
        request = current.request
        name = inspect.currentframe().f_back.f_code.co_name
        if request.function == name:  # if the callee is active function
            f = globals()[request.function]
        else:
            return ""# we don't have info about function
    

    lines, start_line = inspect.getsourcelines( f ) 
    # code = inspect.getsource( f ) 
    code = ''.join( lines )
    
    # remove some function calls from code
    code = re.sub(r",\s*?get_active_code\(\s*?\)", "", code) 
    code = re.sub(r",\s*?index\(\s*?\)", "", code) 
    code = re.sub(r"^@show_.+?$", "", code, flags=re.MULTILINE) 
    code = re.sub(r"^@tutor.*?$", "", code, flags=re.MULTILINE) 
    # code = re.sub(r"@show_menu", "", code) 
    # code = re.sub(r"@show_code", "", code) 
    
    if decorate:
        # return  CODE(code, language="python", link='/examples/global/vars/', counter=start_line)
        return  CODEMIRROR(code)
    else:
        return  code


# def get_file_function_code(controller, function):
    # pass 

if __name__ == '__main__':
    def ftest():
        if True:
            ###GROUP_LINES
            print("labas "),  ###PLACEHOLDER: --> SPAN( "labas " , _style=""),
            print("Pasauli"),  ###            "Pasauli",
            ###GROUP_LINES_END
        print("!")
    tcode = get_task_code(ftest, decorate=False)
    print( tcode )
