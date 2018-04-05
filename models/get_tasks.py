from plugin_introspect import tutor as original_tutor, menu, generate_exposed_functions_info,  unpack_def, CODEMIRROR
import re
import random

LearnTable = None # LearningTable

def set_LearnTable(LT):
    global LearnTable
    LearnTable = LT

def pick_new_task(user_id):
    # get already done/given tasks

    q_user = LearnTable.user_id == user_id
    already_given = [x.task_key for x in db(q_user).select(LearnTable.task_key)]
    # already_given_lessons = db(q_user).select(LearnTable.lesson)

    from plugin_introspect import lessons_menu
    lessons = lessons_menu(return_plain=True)
    lessons = [ x for x in lessons    if
                      (x.startswith('lesson0')    or x.startswith('lesson1'))
                        and 'matricos' not in x          and 'intro' not in x
                ]


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
        # or not task_key in already_given:          # TODO maybe prevent repetition of examples
            break
        else:
            logger.debug( "Skipped tas: too long (%s): %s ", chars_count, task_key )

    record = LearnTable.insert(
        user_id=user_id,

        task_key=task_key,
        lesson=lesson,
        task=task,

        scheduled_from=date.today(),
        scheduled_to=date.today() + TIME_INTERVAL

    )
    return record


def qs_current_tasks(user_id=None):

    now = request.now
    q_time_interval = (LearnTable.scheduled_from < now) & (LearnTable.scheduled_to > now)
    if user_id:
        q_user = LearnTable.user_id == user_id
        return q_user & q_time_interval
    else:
        return q_time_interval


def pick_task_record(user_id):

    q = qs_current_tasks(user_id)

    # check unfinished
    # print db(q)._select(LearnTable.task_key)

    q_unfinished = q & (LearnTable.mark != 100)
    count = db(q_unfinished).count()
    # if we have unfinished tasks - give last of them..
    if not db(q_unfinished).isempty():
        return db(q_unfinished).select().last()  # TODO: kažkodėl nesuveikia

    else:
        # pick new task
        q_finished = q & (LearnTable.mark == 100)
        count = db(q_finished).count()
        if count >= COUNT_PER_INTERVAL:
            return None

        else:
            return  pick_new_task(user_id, LearnTable)


def list_user_tasks(user_id):
    rows = db(qs_current_tasks(user_id)).select(LearnTable.task_key, LearnTable.task,  LearnTable.mark, LearnTable.submitted_on)
    rows = [ LI(B(r.task), " [%s]" % r.submitted_on.strftime("%H:%M")) for r in rows ]
    return CAT("Visos šios dienos užduotys atliktos. Lauksime ryt :)",
        UL( *rows )
        )

def  done_tasks_count():
    result = db((LearnTable.user_id==auth.user_id) & (LearnTable.mark==100)).count()
    return result

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
    result = re.sub('###.*$', '', def_code, flags=re.MULTILINE)
    result = re.sub(r'\n\s*return flush_print().*$', '', result, flags=re.MULTILINE)
    result = result.strip(" \n\t")
    return result

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
            code = code[len(docs ) +6:]
        except IndexError as e:
            print ("ERR: %s \n %s" % (e, code))
            logger.error(  "ERR: %s \n %s" % (e, code) )

    return name, docs, code
