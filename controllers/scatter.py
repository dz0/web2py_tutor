# -*- coding: utf-8 -*-

import random
import re

SL = db.scatter_learn
set_LearnTable(SL)

def split_lines_code_comment(code):
    """
    TODO: what if hashtag is used in a string?
    """
    lines = code.split('\n')
    result = []
    for line in lines:
        count = len( re.findall(r'#+', line) ) # count hashtag groups

        if count== 1:  # if exactly one group -- it should be simple comment
            code, hashtags, comment = re.split(r'(#+)', line)
            if code.strip() and comment.strip(): # if code and comment not empty
                comment = hashtags + comment
            else:
                code = line
                comment = ''
        else:
            code = line
            comment = ''

        result.append(  [code, comment])

    return result

@auth.requires_login()
# @auth.requires(lambda:request.client=='127.0.0.1' or auth.is_logged_in())
def task():
    task_record = pick_task_record(auth.user_id)

    if task_record is None:
        return list_user_tasks(auth.user_id)

    docs, sample = get_code_sample(task_record.lesson, task_record.task)


    split_lines = split_lines_code_comment(sample)

    scattered_comments = []
    def scatter(htmlize = True):
        for nr, line in enumerate(split_lines):
            code, comment = line
            if comment:
               # if  random.randint(1, 2) == 2:  # flip coin :)
                placeholder = None

                if htmlize:

                   # placeholder
                   id = "comment_%s" % nr
                   input_ = INPUT(_name=id, _id=id, _type="")
                   placeholder = SPAN(
                       DIV(XML("&nbsp;"*10),  _class='droppable'),
                       input_
                   )
                   # https://stackoverflow.com/questions/9317293/jquery-draggable-event-when-dropped-outside-of-parent-div

                   # comment
                   comment = XML( highlighted(comment)) #also hightlight it
                   comment = SPAN(comment, _class='draggable')


                line[1] = placeholder
                scattered_comments.append(comment)

    scatter()

    # highlight all codes
    for line in split_lines:
        line[0] = XML(highlighted(line[0]))

    def wrap_into_table(data):
        return TABLE(*[TR(*rows) for rows in data])

    form = FORM(
        wrap_into_table( split_lines )
    )

    form = wrap_into_table( [[form,  UL( scattered_comments ) ]])


    return  dict(contents=
        CAT(
            form,

            XML(highlighted(sample)),
            STYLE(get_styles())
         ),

    )

    user_code = request.vars.user_code or task_record.user_code or ''




