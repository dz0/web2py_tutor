# -*- coding: utf-8 -*-

import random

from test_helper_4automation import my_tokenizer


KL = db.keyboard_learn
set_LearnTable(KL)


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




def _test__pick_task():
    return test__pick_task()

# def test__code_char_count():
#
#     lesson, task = "lesson02_py_sarasai_CRUD_CLI/elementu_numeravimas".split('/')
#     code = cached_exposed_functions(lesson, task)['code']
#     just_chars = hide_comments(adapt_code(code)).replace(" ", "")
#     chars_count = len(hide_comments(adapt_code(code)).replace(" ", ""))
#     return CAT( XML(highlighted(code)), PRE(just_chars),  chars_count )






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

    return dict(
        done_tasks_count=done_tasks_count(),
        contents=CAT(
        "Tema: ", task_record.task, BR(), docs,
        # PRE(XML(obfuscate( highlighted(sample), bla_words=sample.split() ))),


        TABLE(
            TR(["", "", "Kodo rezultatas: "]),
            TR(
                TD(
                    XML(sample_html),
                    STYLE(get_styles(), '.highlight > pre { background: #fbfbfb; }'),
                ),
                TD(""),
                TD(
                    LOAD( c=task_record.lesson, f=task_record.task, vars={"plain":""}, ajax=True, ajax_trap=True)
                ),
            )
        ),

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

