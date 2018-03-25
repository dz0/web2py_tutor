# -*- coding: utf-8 -*-

import random
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from plugin_introspect import tutor as original_tutor, menu, generate_exposed_functions_info, CODEMIRROR
import re


def get_code_samples():
    exposed_functions = generate_exposed_functions_info('lesson02_py_sarasai_CRUD_CLI')
    codes = [ re.sub('###PLACEHOLDER.*', '', x['code']).replace('return flush_print()', '')  for x in exposed_functions.values() ] 
    return codes

def index():
    return UL(map(PRE, get_code_samples()))
    # strip TASK replacements


# tutor = auth.requires_login(original_tutor)
def tutor (*args, **kwargs):
    """decorator to ask login for taks"""
    
    if request.function == 'index' \
    or not exposed_functions[request.function]['is_task']:
        return original_tutor(*args, **kwargs)
        
    # ask login for tasks
    if  auth.is_logged_in():
        return original_tutor(*args, **kwargs)
    else:
        next = auth.here()
        session.flash = response.flash = "užduoties atlikimui reikia prisijungti"
        return call_or_redirect(auth.settings.on_failed_authentication,
                                auth.settings.login_url + '?_next=' + urllib.quote(next))


def highlighted(code=""):
    result = highlight(code, PythonLexer(), HtmlFormatter(linenos=False)) 
    return result
    
    

def obfuscate(html, bla_words=['bla']):
    bla_words=[ x.decode('utf-8') for x in bla_words ]
    # bla_words += ['bla']*len(bla_words)
    def bla():
        classes = "n o mi k ow nb p".split()
        
        bla_ = ' '+random.choice(bla_words)+' '
        return '<span class="%s" style="margin-left:-%s; color:transparent;">%s</span>' % (
                            random.choice(classes), 
                            8*len(bla_), 
                            bla_)
    found = None
    result = []
    chunk = "</span>"
    for i, x in enumerate(html):
        result.append(x)
        if html[i-len(chunk)+1 : i+1] == chunk:
            result.append(bla())
    return ''.join(result)


def get_styles():
    return HtmlFormatter().get_style_defs('.highlight')

from test_helper_4automation import my_tokenizer
def check_mistakes(sample, user_code):

    def adapt(code):
        
        code = code.decode('utf-8')
        code = code.replace('\r', '')
        code = re.sub('#.*', '', code) # strip comments
        
        return code
    
    user_code = adapt(  user_code  )
    sample = adapt(  sample )
    original_user_code = user_code

    sample = my_tokenizer(sample)
    user_code = my_tokenizer(user_code)

    
    # def minify_spaces(code):
    #     import re
    #     return re.sub(r'\s+', ' ', code, re.MULTILINE)
    # sample = minify_spaces(sample)
    # user_code = minify_spaces(user_code)
    
    def get_token_place(token_nr_stop):
        place = 0
        for token_nr, token in enumerate(user_code):
            for ch in token:
                
                if token_nr == token_nr_stop:
                    return place

                if original_user_code[place] == ch:
                    place += 1
                else:
                    return "ERR  @%s" % place

            while original_user_code[place] in '\n\r\t ': # skip spaces
                place += 1

            
    # def get_original_index(stop):
    #     i = 0
    #     on_whitespace = False
    #     for orig_i, x in enumerate( original_user_code ):
    #         if x in '\n\t \r':
    #             if not on_whitespace:
    #                 i += 1
    #                 on_whitespace = True
    #         else:
    #             on_whitespace = False
    #             i += 1
    #         if i == stop:
    #             return orig_i+1
        
    if len(user_code) > len(sample):
        return "User code too long"
    

    for i in range(len(user_code)):
        if user_code[i] != sample[i]:
            # mistake_place = get_original_index(i)
            mistake_place = i
            mistake_place = get_token_place(i)
            mistake = original_user_code[mistake_place]

            if mistake in ' \t':
                mistake = "&nbsp;"
            if mistake in '\n\r':
                mistake += "&nbsp;"
            marked_mistake = (
                    original_user_code[ :mistake_place ] 
                    # + '<span class="mistake">'+ original_user_code[mistake_place] + "</span>"
                    # + '___MISTAKE_START___'+ mistake + '___MISTAKE_END___'
                    + '___MISTAKE___'
                    
                    + original_user_code[mistake_place+1:] 
                    )
            html = highlighted( marked_mistake )
            
            html = html.replace( '___MISTAKE___', 
                                '<span class="mistake" hint="'+ repr(user_code[i])+' instead of '+repr(sample[i])+'">'
                                        + mistake + "</span>"
                                )
            # html = html.replace( '___MISTAKE_START___', '<span class="mistake">')
            # html = html.replace( '___MISTAKE_END___', '</span>')

            return CAT( 
                    STYLE(".mistake {background-color: lightsalmon; }"),
                    XML( html ),  
                    # marked_mistake,
                   
                   )
    
    if len(user_code) < len(sample):
        return "User code too short"
    
    return None
        

def demo():
    sample = get_code_samples()[1]

    sample = """
n = 'ą'
for x in "[3, 5,  7]": # 123 
    suma += x  # ęąčę
    print( x, suma )
    """
    sample = sample.strip(" \n\t")

    user_code = request.vars.user_code or ''
    mistake = ''
    if user_code:
        mistake = check_mistakes(sample, user_code)

    form = FORM(TEXTAREA(user_code, _name='user_code'), INPUT(_type='submit'))

    return CAT(

        PRE(XML(obfuscate( highlighted(sample), bla_words=sample.split() ))),
        STYLE(get_styles()), 
        mistake,
        form,
        # CODEMIRROR(user_code) 
        BEAUTIFY(exposed_functions)
    )


