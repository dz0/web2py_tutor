# -*- coding: utf-8 -*-

import random
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from plugin_introspect import tutor as original_tutor, menu, generate_exposed_functions_info,  unpack_def
import re
from test_helper_4automation import my_tokenizer

def clean_task_code(def_code):
    return re.sub('###PLACEHOLDER.*', '', def_code).replace('return flush_print()', '')

def get_code_samples():
    exposed_functions = generate_exposed_functions_info('lesson02_py_sarasai_CRUD_CLI')
    codes = [clean_task_code  for x in exposed_functions.values() ] 
    
    return codes

def get_code_sample(lesson, task):
    functions = generate_exposed_functions_info(lesson)
    task_def = clean_task_code(functions[task]['code'])
    task_name, docs, sample = prepare_sample_from_def(task_def)
    return docs, sample


# def index():
#     return UL(map(PRE, get_code_samples()))
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

def check_mistakes(sample, user_code, return_mark=False):

    def adapt(code):
        
        code = code.decode('utf-8')
        code = code.replace('\r', '')
        code = re.sub('#.*', '', code) # strip comments
        
        return code
    
    user_code = adapt(  user_code  )
    sample = adapt(  sample )
    original_user_code = user_code
    original_sample = sample

    sample = my_tokenizer(sample)
    user_code = my_tokenizer(user_code)
    print('user_code', user_code)

    def mark_till_mistake_token(i):
        user_chars = len(''.join(user_code[:i]))  # [''] for empty user code
        all_sample_tokens_chars = len(''.join(sample))
        if all_sample_tokens_chars:
            return  100* user_chars / all_sample_tokens_chars
    
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
        


    for i in range(len(user_code)):
        if user_code[i] != sample[i]: # if mistake
            # mistake_place = get_original_index(i)
            mistake = user_code[i] 
            mistake_place = get_token_place(i)

            if return_mark:
                # return 100*mistake_place/len(original_sample)
                return mark_till_mistake_token(i)

            if mistake in ' \t':
                mistake = "&nbsp;"
            if mistake in '\n\r':
                mistake += "&nbsp;"
            marked_mistake = (
                    original_user_code[ :mistake_place ] 
                    # + '<span class="mistake">'+ original_user_code[mistake_place] + "</span>"
                    # + '___MISTAKE_START___'+ mistake + '___MISTAKE_END___'
                    + '___MISTAKE___'
                    
                    + original_user_code[mistake_place+len(mistake):] 
                    )
            html = highlighted( marked_mistake )
            
            html = html.replace( '___MISTAKE___', 
                                '<span class="mistake" hint="'+ repr(mistake)+' instead of '+repr(sample[i])+'">'
                                        + mistake + "</span>"
                                )
            # html = html.replace( '___MISTAKE_START___', '<span class="mistake">')
            # html = html.replace( '___MISTAKE_END___', '</span>')

            return CAT( 
                    STYLE(".mistake {background-color: lightsalmon; }"),
                    XML( html ),  
                    # marked_mistake,
                   
                   )      



    if return_mark:
        return mark_till_mistake_token(len(user_code))


    if len(user_code) > len(sample):
        return "User code too long"

    if len(user_code) < len(sample):
        return "User code too short"
    
    return ''


def qs_current_tasks(user_id=None):
    kl = db.keyboard_learn
    now = request.now
    q_time_interval = (kl.scheduled_from < now)  &  ( kl.scheduled_to > now)
    if user_id:
        q_user = kl.user_id==user_id 
        return q_user  &   q_time_interval
    else:
        return q_time_interval

def pick_task_record(user_id):
    kl = db.keyboard_learn
    
    q = qs_current_tasks(user_id)

    # check unfinished
    # print db(q)._select(kl.task_key)

    q_unfinished =  q &  (kl.mark != 100)
    count = db(q_unfinished).count()
    # if we have unfinished tasks - give last of them..
    if not db(q_unfinished).isempty() :
        return db(q_unfinished).select().last()  # TODO: kažkodėl nesuveikia
    
    else:
        #pick new task
        q_finished =  q & ( kl.mark == 100 )
        count = db(q_finished).count()      
        if count >= COUNT_PER_INTERVAL:
            return None

        # else
        def pick_new_task():
            # get already done/given tasks
            q_user = kl.user_id==user_id
            already_given = [x.task_key for x in db(q_user).select(kl.task_key) ]
            # already_given_lessons = db(q_user).select(kl.lesson)

            from plugin_introspect import lessons_menu
            lessons = lessons_menu(return_plain=True)
            # while True: # TODO maybe prevent repetition of examples
            lesson = random.choice( lessons )
            tasks = generate_exposed_functions_info(lesson)
            task = random.choice( tasks.keys() )
            task_key = lesson + '/' + task

            record = kl.insert(
                user_id=user_id,
                
                task_key=task_key,
                lesson=lesson,
                task=task,

                scheduled_from=request.now,
                scheduled_to=request.now+TIME_INTERVAL
                
            )
            # if not task_key in already_given:
            return record
            # def_code = clean_task_code(tasks[task]['code'])
            # task_name, docs, sample = prepare_sample_from_def(sample)
            # return lesson, task_name, docs, sample
            
        return pick_new_task()



# def demo_task():
#     sample = """
# n = 'ą'
# for x in "[3, 5,  7]": # 123 
#     suma += x  # ęąčę
#     print( x, suma )
#     """
    # task_key=lesson+'/'+task_name

@auth.requires_login()
# @auth.requires(lambda:request.client=='127.0.0.1' or auth.is_logged_in())
def task():

    task_record = pick_task_record(auth.user_id) 

    if task_record is None:
        return CAT( "All tasks for current period are done :)", 
                db( qs_current_tasks(auth.user_id) ).select()
        )

    docs, sample = get_code_sample(task_record.lesson, task_record.task)
    # task_name, docs, sample = prepare_sample_from_def(sample)
                # return lesson, task_name, docs, sample

    sample = sample.strip(" \n\t")

    kl = db.keyboard_learn
    # id_query = (kl.task_key==task_key) & (kl.user_id==auth.user_id)

    # TODO
    # time_interval = (kl.scheduled_from < request.now) & (request.now  < kl.scheduled_to)

    # record = db(id_query).select().first()
    
    user_code = request.vars.user_code or task_record.user_code or ''
    mistake = check_mistakes(sample, user_code)
    mark = check_mistakes(sample, user_code, return_mark=True)
    
    # if True:
    if user_code:
        
        task_record.update_record( 
            user_code=user_code,
            mark=mark,
            tries_count=task_record.tries_count+1

        )
        # db.keyboard_learn.update_or_insert(  id_query,
        #     lesson=lesson,
        #     task=task_name,
        #     task_key=task_key,
        #     user_code=user_code,
        #     mark=mark
        # )
    
    form = FORM(TEXTAREA(user_code, _name='user_code'), INPUT(_type='submit'))
    if mark == 100:
        form = ""
        
    


    return CAT(
        task_record.task, BR(), docs,
        # PRE(XML(obfuscate( highlighted(sample), bla_words=sample.split() ))),
        PRE(XML(( highlighted(sample) ))),
        STYLE(get_styles()), 
        DIV("Pažymys: ", mark, _class='mark'),
        DIV("Klaida: " *bool(mistake), mistake, _class='mistake_info'),
        form,
        # CODEMIRROR(user_code) 
        # BEAUTIFY(exposed_functions)
    )



def prepare_sample_from_def(orig_code):
    # return "name", "docs", orig_code
    
    code = orig_code.strip()
    name = re.findall('^def\s+(.*?)\s*\(', code, re.MULTILINE)[0]
    code = unpack_def(code).strip()
    if code.startswith('"""'):
        docs = re.findall('^"""(.*?)"""', code, re.MULTILINE)[0]
        code = code[len(docs)+6:]
    else:
        docs = ""
    return name, docs, code