# -*- coding: utf-8 -*-

import random
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from plugin_introspect import tutor as original_tutor, menu, generate_exposed_functions_info,  unpack_def, CODEMIRROR
import re
from test_helper_4automation import my_tokenizer
from datetime import date

KL = db.keyboard_learn


# tutor = auth.requires_login(original_tutor)
def tutor(*args, **kwargs):
    """decorator to ask login for taks"""

    if request.function == 'index' \
            or not exposed_functions[request.function]['is_task']:
        return original_tutor(*args, **kwargs)

    # ask login for tasks
    if auth.is_logged_in():
        return original_tutor(*args, **kwargs)
    else:
        next = auth.here()
        session.flash = response.flash = "užduoties atlikimui reikia prisijungti"
        return call_or_redirect(auth.settings.on_failed_authentication,
                                auth.settings.login_url + '?_next=' + urllib.quote(next))


def highlighted(code=""):
    result = highlight(code, PythonLexer(), HtmlFormatter(linenos=False))
    return result


def obfuscate(html, bla_words=['bla'],
              msg=u"        Aš matau, kad tu kopijuoji! ;)       "
              ):
    bla_words = [guarantee_unicode(x) for x in bla_words]
    bla_words.append(msg)

    # bla_words += ['bla']*len(bla_words)
    def bla():
        classes = "n o mi k ow nb p".split()

        bla_ = ' '+random.choice(bla_words)+' '
        return '<span class="%s" style=" margin-left:-%spx; color:transparent;">%s</span>' % (
            random.choice(classes),
            8*len(bla_)-5,
            bla_)
    found = None
    result = []
    chunk = "</span>"

    for i, x in enumerate(html):
        result.append(x)
        if html[i-len(chunk)+1: i+1] == chunk:
            result.append(bla())

    return ''.join(result)


def get_styles():
    return HtmlFormatter().get_style_defs('.highlight')


"""Mistakes"""
# def highlight_mistake(token_nr, code_text=original_user_code):


def highlight_mistake(token_nr, code_text):
    code_invisible_comments = hide_comments(code_text)
    code_tokens = my_tokenizer( code_invisible_comments  )

    def get_token_place(token_nr_stop):
        place = 0
        for token_nr, token in enumerate(code_tokens):

            while code_invisible_comments[place] in '\n\r\t ':  # skip spaces
                place += 1 # increase cursor

            if token_nr == token_nr_stop:  # could be before inner for
                return place

            place += len(token) # increase cursor

            # for ch in token:
            #     # increase place only if
            #     if code_invisible_comments[place] == ch:
            #         place += 1
            #     else:
            #         return "ERR  @%s" % place


    # mistake_place = get_original_index(token_nr)
    mistake = code_tokens[token_nr]
    mistake_place = get_token_place(token_nr)

    if mistake in ' \t':
        mistake = "&nbsp;"
    if mistake in '\n\r':
        mistake += "&nbsp;"
    marked_mistake = (
        code_text[:mistake_place]
        + '___MISTAKE___'
        + code_text[mistake_place+len(mistake):]
    )

    html = highlighted(marked_mistake)  # pygments

    MISTAKE_BACKGROUND_STYLE = "background-color: yellow;"
    html = html.replace('___MISTAKE___',
                        '<span class="mistake" style="%s">' % MISTAKE_BACKGROUND_STYLE
                        + mistake + "</span>"
                        )
    return html
    # CAT(
    #     STYLE(".mistake {background-color: yellow; }"),
    #     XML( html ),
    #     # marked_mistake,

    #     )


def check_mistakes(sample, user_code, return_mark=False):
        # TODO: bėda su lietuviškais komentarais... 


    user_code = adapt_code(user_code)
    sample = adapt_code(sample)

    original_user_code = user_code
    original_sample = sample

    user_code = hide_comments(user_code)
    sample = hide_comments(sample)

    sample = my_tokenizer(sample)
    user_code = my_tokenizer(user_code)
    # print('user_code', user_code)

    def mark_till_mistake_token(i):
        """Calculates mark for the user_code, 
        Counts how many tokens were entered OK (before possible error).
        """
        if i < 0:
            return 0

        user_chars = len(''.join(user_code[:i]))  # [''] for empty user code
        all_sample_tokens_chars = len(''.join(sample))
        if all_sample_tokens_chars:
            return 100 * user_chars / all_sample_tokens_chars

    for i in range(min(len(user_code), len(sample))):
        if user_code[i] != sample[i]:  # if mistake

            if return_mark:
                return mark_till_mistake_token(i)
            else:
                return i

    if len(user_code) > len(sample):
        if return_mark:
            too_much = len(user_code)-len(sample)
            return mark_till_mistake_token(len(sample) - too_much)
        else:
            return "Per ilgas kodas"

    if return_mark:
        return mark_till_mistake_token(len(user_code))

    if len(user_code) < len(sample):
        return "Per trumpas kodas"

    return ''  # viskas OK


def qs_current_tasks(user_id=None):
    now = request.now
    q_time_interval = (KL.scheduled_from < now) & (KL.scheduled_to > now)
    if user_id:
        q_user = KL.user_id == user_id
        return q_user & q_time_interval
    else:
        return q_time_interval


def test__pick_task():

    user_id = 1
    tasks = []
    for x in range(50):
        task = pick_new_task( user_id )
        docs, code = get_code_sample(task.lesson, task.task)
        chars_count =  len( hide_comments( adapt_code(code) ).replace(" ", "") )
        tasks.append(  {task.task_key: [ docs, BR(), XML(highlighted(code)), BR(), chars_count ]})

    return CAT(
        STYLE(get_styles()),
        BEAUTIFY( tasks ), 
        list_user_tasks( user_id ),

    )

def test__code_char_count():

    lesson, task = "lesson02_py_sarasai_CRUD_CLI/elementu_numeravimas".split('/')
    code = cached_exposed_functions(lesson, task)['code']
    just_chars = hide_comments(adapt_code(code)).replace(" ", "")
    chars_count = len(hide_comments(adapt_code(code)).replace(" ", ""))
    return CAT( XML(highlighted(code)), PRE(just_chars),  chars_count )


def pick_new_task(user_id):
    # get already done/given tasks
    q_user = KL.user_id == user_id
    already_given = [x.task_key for x in db(q_user).select(KL.task_key)]
    # already_given_lessons = db(q_user).select(KL.lesson)

    from plugin_introspect import lessons_menu
    lessons = lessons_menu(return_plain=True)
    lessons = [ x for x in lessons      if x.startswith('lesson0') and 'matricos' not in x  and 'intro' not in x ]            # while True: # TODO maybe prevent repetition of examples


    while True:
        lesson = random.choice(lessons)
        # tasks = generate_exposed_functions_info(lesson)
        tasks = cached_exposed_functions(lesson)
        task = random.choice(tasks.keys())
        task_key = lesson + '/' + task

        # check that task is not too long
        code = cached_exposed_functions(lesson, task)['code']
        chars_count = len(hide_comments(adapt_code(code)).replace(" ", ""))
        if chars_count <= CODE_CHARS_COUNT_LIMIT:
        # or not task_key in already_given:
            break
        else:
            logger.debug( "Skipped tas: too long (%s): %s ", chars_count, task_key )

    record = KL.insert(
        user_id=user_id,

        task_key=task_key,
        lesson=lesson,
        task=task,

        scheduled_from=date.today(),
        scheduled_to=date.today() + TIME_INTERVAL

    )
    return record



def pick_task_record(user_id):

    q = qs_current_tasks(user_id)

    # check unfinished
    # print db(q)._select(KL.task_key)

    q_unfinished = q & (KL.mark != 100)
    count = db(q_unfinished).count()
    # if we have unfinished tasks - give last of them..
    if not db(q_unfinished).isempty():
        return db(q_unfinished).select().last()  # TODO: kažkodėl nesuveikia

    else:
        # pick new task
        q_finished = q & (KL.mark == 100)
        count = db(q_finished).count()
        if count >= COUNT_PER_INTERVAL:
            return None

        else:
            return  pick_new_task(user_id)


def list_user_tasks(user_id):
    rows = db(qs_current_tasks(user_id)).select(KL.task_key, KL.task,  KL.mark, KL.submitted_on)
    rows = [ LI(B(r.task), " [%s]" % r.submitted_on.strftime("%H:%M")) for r in rows ]
    return CAT("Visos šios dienos užduotys atliktos. Lauksime ryt :)",
        UL( *rows )
        )


@auth.requires_login()
# @auth.requires(lambda:request.client=='127.0.0.1' or auth.is_logged_in())
def task():

    task_record = pick_task_record(auth.user_id)

    if task_record is None:
        return list_user_tasks(auth.user_id)

    docs, sample = get_code_sample(task_record.lesson, task_record.task)

    # TODO
    # time_interval = (KL.scheduled_from < request.now) & (request.now  < KL.scheduled_to)

    # record = db(id_query).select().first()

    user_code = request.vars.user_code or task_record.user_code or ''

    mark    = check_mistakes(sample, user_code, return_mark=True)
    mistake = check_mistakes(sample, user_code)

    if isinstance(mistake, int):
        sample_html = highlight_mistake(mistake, sample)

        user_token = my_tokenizer(hide_comments(adapt_code(user_code)))[mistake]
        # mistake = u'Netinka žodis/ženklas: "%s" (nr.: %s): ' % (user_token, (mistake+1))
        mistake = u'Netinka žodis/ženklas: "%s" ' % user_token
    else:
        sample_html = highlighted(sample)
    sample_html = obfuscate(sample_html, bla_words=sample.split())

    # if True:
    if user_code:

        task_record.update_record(
            user_code=user_code,
            mark=mark,
            tries_count=task_record.tries_count+1

        )


    form = FORM(TEXTAREA(user_code, _name='user_code',
                         _id='user_code'), INPUT(_type='submit'))
    CodeMirror_js = SCRIPT(
        "cm = CodeMirror.fromTextArea(document.getElementById('user_code')); cm.refresh(); ")

    if mark == 100:
        form = ""
        
    return dict(content=CAT(
        "Tema: ", task_record.task, BR(), docs,
        # PRE(XML(obfuscate( highlighted(sample), bla_words=sample.split() ))),
        XML(sample_html),
        STYLE(get_styles(), '.highlight > pre { background: #fbfbfb; }'),
        DIV("Atlikta: %s%%" % mark, _class='mark'),
        DIV("Klaida: ", mistake, _class='mistake_info') if mistake else B(A("Kita užduotis", _href="")),
        
        BR(),
        CAT("Perrašykite kodą (komentarų rašyt nereikia, o tarpus galit dėlioti, kaip patogu)",
        form, 
        CodeMirror_js) * bool(form)
        # CODEMIRROR(user_code)
        # BEAUTIFY(exposed_functions)
    )
    )


"""       INTROSPECTION SAMPLES"""




from pprint import pformat

exposed_functions_by_lesson = {} # for singleton/cashe
def cached_exposed_functions(lesson, task=None):
    # logger.debug( "get_code %s/%s" , lesson, task )
    if not lesson in exposed_functions_by_lesson:
        functions = generate_exposed_functions_info(lesson, force_reset=True)
        # logger.debug("%s  functions: \n%s", lesson, pformat(functions, indent=4) )

        exposed_functions_by_lesson[lesson] = functions
    
    # logger.debug("exposed_functions_by_lesson: \n%s",  pformat(exposed_functions_by_lesson, indent=4) )
    
    if task is None:
        return exposed_functions_by_lesson[lesson]
    else: 
        return exposed_functions_by_lesson[lesson][task]


def clean_task_code_from_meta(def_code):
    return  re.sub('###.*', '', def_code)  \
            .replace('return flush_print().*', '') \
            .strip(" \n\t")

def guarantee_unicode(txt):
    if not isinstance(txt, unicode):
        txt = txt.decode('utf-8')
    return txt

def hide_comments(code):
    """makes comments invisible
    replaces with spaces (not just delete) -- this is needed for later place detection by token nr."""
    def make_spaces(matchobj):
        txt = matchobj.group(0)
        return ' ' * len(txt)

    # find simple comments
    code = re.sub(r'(#.*$)', make_spaces, code, flags=re.MULTILINE)  # strip comments

    # # find docstring
    # code = re.sub(r'(?<=^def\s+.*?:\s*)"""[\s\S]*?"""', make_spaces, code, flags=re.DOTALL)

    # replace multiline string -- but only at line start  # TODO: don't know why it works also for non line-start
    code = re.sub(r'(?<=[^\n])\s*"""[\s\S]*?"""', make_spaces, code)
    code = re.sub(r"(?<=[^\n])\s*'''[\s\S]*?'''", make_spaces, code)

    return code

def adapt_code(code):

    code = guarantee_unicode(code)
    code = code.replace('\r', '')
    code = clean_task_code_from_meta(code)

    return code


def get_code_sample(lesson, task):
    # functions = generate_exposed_functions_info(lesson, force=True)
    task_def = cached_exposed_functions(lesson, task)['code']
    task_def = adapt_code(task_def)
    if lesson.endswith("_CLI"):
        # hide def title and take docstring
        task_name, docs, sample = prepare_sample_from_def(task_def)
        return docs, sample
    else:
        return "", task_def


def prepare_sample_from_def(orig_code):
    # return "name", "docs", orig_code

    code = orig_code.strip()
    name = re.findall(r'^def\s+(.*?)\s*\(', code, re.MULTILINE)[0]

    code = unpack_def(code).strip()
    docs = ""
    if code.startswith('"""'):
        try:
            docs = re.findall(r'^\s*"""(.*?)"""', code, re.DOTALL)[0]
            code = code[len(docs)+6:]
        except IndexError as e:
            print ("ERR: %s \n %s" % (e, code))
            logger.error(  "ERR: %s \n %s" % (e, code) )
        
    return name, docs, code
