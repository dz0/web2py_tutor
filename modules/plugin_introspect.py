# -*- coding: utf-8 -*-

# try:
from gluon import current
from gluon.html import * # URL, UL, A, B, CAT, PRE, CODE, BR, SPAN
from gluon.admin import apath
from gluon.compileapp import find_exposed_functions
from gluon.myregex import regex_expose  # TODO: get the most recent function code manually parsing controller

from task_parser import task

# except ImportError as e:
    # print( e )

import inspect
import re
import os

def get_controller_code( c=None, app=None ):
    request = current.request
    app = app or request.application
    c = c or request.controller
    fpath = apath('%s/controllers/%s.py' % (app, c), r=request)
    with open(fpath) as f:
        code = f.read()

    return code

exposed_functions = {}  # for singleton

def generate_exposed_functions_info():


    global exposed_functions
    exposed_functions = getattr(current, 'exposed_functions', {} )
    current.exposed_functions = exposed_functions
    if not exposed_functions:
        for f in exposed_functions_names():
            d = exposed_functions[f] = {}
            d['code'] = code = get_exposed_function_code( f )
            d['is_task'] = '_task' in f or f.startswith('task')    or "###PLACEHOLDER" in code
    return exposed_functions

def get_exposed_function_code(fun_name, code=None):

    if code is None:
        code = get_controller_code()

    regex_myfun_header = re.compile(
        # r'^def\s+(?P<name>_?[a-zA-Z0-9]\w*)\( *\)\s*:',
        r'^def\s+(%s)\( *\)\s*:' % fun_name,
        flags=re.M)
    match = regex_myfun_header.search(code)
    myfun_header = match and match.group(0)
    start = code.find(myfun_header)

    lines = code[start:].split('\n')
    result = [lines[0]]

    for line in lines[1:]:
        if line and line[0] not in " \t\n#":  # if first character is indented or comment -- fixme: multiline strings could be gotchas here
            break
        else:
            result.append(line)

    # todo:  include decorators
    # prelines = reversed( code[:start].split('\n') )

    return "\n".join(result)


def lessons_menu(return_plain=False):
    
    request = current.request
    
    app = request.application
    c = request.controller
    dirpath = apath('%s/controllers' % app, r=request)    
    
    controllers  = [ c[:-len('.py')]   for c in os.listdir( dirpath )      if c.startswith('lesson') and c.endswith('.py')]
    controllers.sort()
    
    menu = [  A(  c[len("lesson"):].title(),     _href=URL(c, 'index') )     for c in controllers   ]
    
    if return_plain:
        return controllers
    else:
        return UL(menu)
        
def exposed_functions_names():
    
    request = current.request
    
    app = request.application
    c = request.controller
    fpath = apath('%s/controllers/%s.py' % (app, c), r=request)
    data = open(fpath).read()
    
    items = find_exposed_functions(data)
    items = [i for i in items if i != 'index']
    return items



def menu(only_category = False, item_decorator=None, cat_decorator=None, plain_menu=False):
    """gives list with links to all exposed functions except currently used

       optionally gives just current categorry
    """
    fun_names = exposed_functions_names()

    generate_exposed_functions_info()
    request = current.request

    if item_decorator is None:
        item_decorator = lambda item: item if item == request.function    else SPAN(A(item, _href=URL(item)), "*" * exposed_functions[item]['is_task'])

    if cat_decorator is None:
        cat_decorator = lambda cat_name, items: TOGGLABLE_CONTENT( cat_name, UL(items))

    decorated = [item_decorator(item) for item in fun_names]

    ctx  = {'current_cat':None}
    def transform_to_tree():
        "group menu items into categories -- if item name starts with _  it means new category"
        result = []
        cat = []
        cat_name = ""

        for name, html in zip( fun_names, decorated):
            if name.startswith('_'): # means category
                result .append ( cat_decorator( cat_name, cat ) )  #
                # result .append ( TOGGLABLE_CONTENT( cat_name, UL(cat)) )  #
                cat_name = name.replace("_", " ").title()
                cat = [ ]

            if only_category and name==request.function:
                return cat_name  # dirty hack to get current category name

            cat.append( html )

        result.append(cat_decorator(cat_name, cat))  # last category
        # result.append(TOGGLABLE_CONTENT(cat_name, UL(cat)))  # last category

        return result

    if only_category:
        current_category = transform_to_tree()
        return current_category

    if plain_menu:
        return transform_to_tree()

    if current.request.function in [ 'index', 'menu' ]:
        lesson_name = request.controller[len("lesson"):]
        lesson_name = " ".join(lesson_name.split("_")[1:]).title()
        return CAT(H3(lesson_name), UL( transform_to_tree() ))

    return  UL( transform_to_tree() )
    # return UL( htmlized )



def TOGGLABLE_CONTENT(name, content):
    js_toggle = ''
    """
    d=this.nextElementSibling.style.display; this.nextElementSibling.style.display = (d=='block'||d=='') ? 'none': 'block';
    """
    
    return CAT( 

        SPAN( name, _class="button", _onclick=js_toggle, _style="cursor:hand"),
        SPAN( content , _class="togglable")
        # SPAN( content, _class="togglable", _style="display:none" )
        ,SPAN("", _class="after_togglable")
    )

def CODEMIRROR(code, language="python", task_key=None):
    """code can be text or list of texts"""
    if task_key is None:
        req = current.request
        task_key = req.controller + "/" + req.function
    return XML(current.response.render('codemirror.html', dict(code=code, language=language, task_key=task_key)))
    

import traceback
def tutor(f):
    """smart decorator"""
    def result():
        try:
            content = f()
        except Exception as e:
            # content = repr( e )
            tb_str = traceback.format_exc()
            lines = tb_str.split("\n")
            # hide path and tutor decorator info
            for nr, line in enumerate(lines):
                if 'File "' in line and '/controllers/' in line:
                    a, b = line.split( 'File "', 1)
                    _, b = b.split('/controllers/', 1)
                    lines[nr] = a + 'File "'+b

            tb_str = "\n".join(  lines[:1]+ lines[3:]  ) # hide lines about plugin_introspect
            content =  CAT( "KLAIDA:", PRE(  tb_str, _style="color:brown" ) )

        if 'plain' in current.request.vars:
            return content

        about = get_module_doc( get_controller_code() )

        codes = TOGGLABLE_CONTENT("[ Kodas ]", get_task_code(f))
        
        # menu
         
        menu_ = TOGGLABLE_CONTENT("[ Meniu ]", menu())
        
        # next menu
        items = exposed_functions_names()
        req = current.request
        nr = items.index( req.function )
        next = items[nr+1] if nr < len(items)-1  else None
        prev = items[nr-1] if nr > 0  else None
        
        a_next = A("[ Pirmyn ]", _href=URL(next))   if  next!=None  else ""
        a_prev = A("[ Atgal ]", _href=URL(prev))   if  prev!=None  else ""
        navigate_prev_next = CAT( a_prev, " ",  a_next )
        # menu_ = CAT( BR(), a_prev, a_next,  BR(), menu_ )
        current_category = menu(only_category=True)


        return XML(current.response.render('tutor.html',
                                           dict( about=about, content=content, codes=codes, menu=menu_,
                                                 navigate_prev_next=navigate_prev_next,
                                                 current_category=current_category
                                                 )
                                           ) )
        # return  gluon.template.render(content='...', context=<vars>)
    return result 
    
def get_task_code(f, decorate=True):

    code = get_active_code( f, decorate=False) # inspect.getsource( f )

    # code = "\n"+code # workaround as otherwise first line dissapears

    t = task(  code )
    student_lines = t['student_lines']
    
    # group lines into chunks (of not/placeholders)
    chunks = []
    
    current_chunk = ""
    placeholder_line_nrs = [p['line_nr'] for p in t['placeholders']]
    
    # save answers in session
    req = current.request
    session = current.session

    task_key = req.controller +'/'+ req.function

    session.setdefault( 'answers', {} )
    session.answers[ task_key ]  = [p['expected'] for p in t['placeholders'] ]

    session.setdefault( 'initial_codes', {} )
    session.initial_codes[ task_key ]  = [p['given'] for p in t['placeholders'] ]

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
    

    code = get_exposed_function_code(f.__name__)


    # OPTION2: doesn't refresh without server reload
    # lines, start_line = inspect.getsourcelines( f )
    # # code = inspect.getsource( f )
    # code = ''.join( lines )
    
    # remove some function calls from code
    code = re.sub(r",\s*?get_active_code\(\s*?\)", "", code) 
    code = re.sub(r",\s*?index\(\s*?\)", "", code) 
    code = re.sub(r"^@show_.+?$", "", code, flags=re.MULTILINE) 
    code = re.sub(r"^@tutor.*?$", "", code, flags=re.MULTILINE) 
    # remove/hide lines by directive "###HIDE"
    code = re.sub(r"^.*?###HIDE.*?$", "", code, flags=re.MULTILINE)
    code = re.sub(r"^(\s*).*?###REPLACE:?\s*?(.*?)$", r"\1\2", code, flags=re.MULTILINE)


    # code = re.sub(r"@show_menu", "", code) 
    # code = re.sub(r"@show_code", "", code) 
    
    if decorate:
        # return  CODE(code, language="python", link='/examples/global/vars/', counter=start_line)
        code = CODEMIRROR(code)
        return code
    else:
        return  code


# def get_file_function_code(controller, function):
    # pass 

import ast
def get_module_doc(code):
    module = ast.parse(code)
    return ast.get_docstring(module)


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
