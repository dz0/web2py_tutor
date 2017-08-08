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

def generate_exposed_functions_info(controller=None):
    controller = controller or current.request.controller
    global exposed_functions
    exposed_functions = getattr(current, 'exposed_functions', {} )
    current.exposed_functions = exposed_functions
    if not exposed_functions:
        full_file_code = get_controller_code(controller)

        for f in exposed_functions_names(controller):
            d = exposed_functions[f] = {}

            d['code'] = code = get_exposed_function_code( f, code=full_file_code )
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

    lessons  = [ c[:-len('.py')]   for c in os.listdir( dirpath )      if c.startswith('lesson') and c.endswith('.py')]
    lessons.sort()

    if return_plain:
        return lessons
    else:
        menu = [  A(  lesson[len("lesson"):].title(),  _href=URL(lesson, 'index') )     for lesson in lessons   ]
        return UL(menu)

def exposed_functions_names(controller=None):

    request = current.request

    app = request.application
    controller = controller or request.controller
    fpath = apath('%s/controllers/%s.py' % (app, controller), r=request)
    data = open(fpath).read()

    items = find_exposed_functions(data)
    items = [i for i in items if i != 'index']
    return items


def task_marker(item):
    """marks tasks in menu

    if user has done the task wil mark with "+"
    if user has tried, but not finished "-" (or percent of completion)

    if not tried (or not logged in) "*"
    """
    auth = current.auth
    db = current.db

    if auth.is_logged_in():
        task_key = current.request.controller + "/" + item
        q = query_unique_task_user = (db.learn.task_key==task_key) & (db.learn.user_id==auth.user_id)
        task_info = db( q ).select().first()
        if task_info:
            if task_info.mark == 100:
                # return "+"
                return SPAN("+", _class="task-marker done", _style="color:green; vertical-align: super; ")
            else:
                # return "-"
                return SPAN("(%s%%)" % task_info.mark, _class="task-marker unfinished", _style="color:red; vertical-align: super; font-size:0.6em;")
        return SPAN("*", _class="task-marker not-started", _style="color:red; vertical-align: super; ")

    return "*"
    # exposed_functions[item]

def menu(only_category = False, item_decorator=None, cat_decorator=None, plain_menu=False):
    """gives list with links to all exposed functions except currently used

       optionally gives just current categorry
    """
    fun_names = exposed_functions_names()

    generate_exposed_functions_info()
    request = current.request

    if item_decorator is None:
        item_decorator = lambda item: item if item == request.function    else SPAN(A(item, _href=URL(item)), task_marker(item) * exposed_functions[item]['is_task'] )

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
import functools

def tutor(f=None, extra_files=None, inject_tutor_as_block=False, imitateCLI=False, flush_print=None):
    """smart decorator"""

    if f is None:  # a hack to allow decorate with syntax:    @tutor(extra_files=['models/model.py', 'views/view.html'])
        return functools.partial(tutor, extra_files=extra_files, inject_tutor_as_block=inject_tutor_as_block, imitateCLI=imitateCLI, flush_print=flush_print)

    def result():
        try:
            content = f()
           
            if imitateCLI and flush_print:
                content = flush_print()            
                       
            if isinstance(content, dict):
                # req = current.request
                # view_root = apath("%s/views/" % (req.application), r=req)
                # view_file = "%s/%s.html" % (req.controller, f.__name__)
                # if os.path.isfile( view_root + view_file  ):
                #     content =  XML(current.response.render(
                #                         view_file,
                #                         content
                #                 ))
                # else:
                    content = current.response.render(
                        # 'generic.html',
                        content
                    )


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

        task_code = get_task_code(f, imitateCLI=imitateCLI)
        if extra_files:
            extra_codes = []
            request = current.request
            for fname in extra_files:
                fpath = apath('%s/%s' % (request.application, fname), r=request)
                with open(fpath) as file:
                    code = file.read()
                    extra_codes.append( CAT(BR(), SPAN(fname), CODEMIRROR(code, task_key="extra")) ) # TODO maybe refactro task_key usage


            task_code = CAT( task_code, *extra_codes )

        codes = TOGGLABLE_CONTENT("[ Kodas ]", task_code)

        if 'plain_item' in current.request.vars: # for overview functionallity -- when all tasks in same page -- called via LOAD
            return XML(current.response.render('tutor_item.html',
                                                dict(content=content, codes=codes)
                                               ))
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

        if inject_tutor_as_block:
            # injects tutor as floating block into any view
            tutor_content = XML(current.response.render('tutor_inject_as_block.html',
                                               dict( inject_tutor_as_block=True, # content=None,
                                                     about="", codes=codes, menu=menu_,
                                                     navigate_prev_next=navigate_prev_next,
                                                     current_category=current_category
                                                     )
                                               ) )
            return CAT( XML(content) , DIV(tutor_content) ) # TODO better inject into body, than append to html?


        else:
            return XML(current.response.render('tutor.html',
                                               dict( about=about, content=XML(content), codes=codes, menu=menu_,
                                                     navigate_prev_next=navigate_prev_next,
                                                     current_category=current_category
                                                     )
                                               ) )
        # return  gluon.template.render(content='...', context=<vars>)
    return result

def get_task_code(f=None, code=None, decorate=True, task_key=None, extra_files=None, imitateCLI=False):

    if code is None:
        code = get_active_code( f, decorate=False, imitateCLI=imitateCLI) # inspect.getsource( f )
    else:
        code = get_active_code(code=code, decorate=False, imitateCLI=imitateCLI)  # inspect.getsource( f )

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

    if task_key is None:
        task_key = req.controller +'/'+ req.function

    session.setdefault( 'answers', {} )
    session.answers[ task_key ]  = [p['expected'] for p in t['placeholders'] ]

    session.setdefault( 'full_codes', {} )
    session.full_codes[ task_key ] = code

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


def get_active_code(f=None, code=None, decorate=True, imitateCLI=False):
    """Gets code of either the request.function (it it is the callee) or the provided function"""

    if code is None:
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

    current.session.imitateCLI = imitateCLI  # TODO: refactor to be saved per each task (now one instance is for all, and if the task is switched in other tab without reloading, migt be problems)..

    if imitateCLI:
        # hide def
        code = re.sub(r"^def.*$", "", code, flags=re.MULTILINE)
        code = code.lstrip()

        # dedent by 4 spaces:
        code = re.sub(r"^    (.*)$", r"\1", code, flags=re.MULTILINE)


        if 'print' in code:
            # hide last return (as it should flush outputs of print)
            code = re.sub( r'(\s*?)(return)(.*?)\s*?$', '', code.rstrip() )
        else:
        # convert return to print (it should be on last line) # todo: maybe just hide it?
        # code = code.rstrip().replace( 'return', 'print(' ) + ' )'
        # if isinstance(imitateCLI, dict) and 'return' in imitateCLI:
            # code = re.sub( r'^(\s*?)(return)(.*?)\s*?$', r'\1'+imitateCLI['return']'+'(\3 )', code, flags=re.MULTILINE )
            code = re.sub( r'(\s*?)(return)(.*?)\s*?$', r'\1print(\3 )', code )



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
