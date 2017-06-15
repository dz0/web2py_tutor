import datetime
db.define_table('chat',
                    Field('vardas', requires=IS_NOT_EMPTY() ),
                    Field('email', requires=IS_EMAIL() ),
                    Field('atsiliepimas', requires=IS_NOT_EMPTY(), widget=SQLFORM.widgets.text.widget ), 
                    Field('laikas', 'datetime', default=lambda:datetime.datetime.now() ),
                )


db.chat.laikas.readable = False
db.chat.laikas.writable = False
