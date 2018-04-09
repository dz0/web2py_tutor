# -*- coding: utf-8 -*-

db.define_table('categories', 
        Field('title', 'string')
)


# Skelbimai
db.define_table('posts', 
        Field('author', db.auth_user, 
                    default=auth.user.id,  # reikia, kad naudotojas būtų prisijungęs 
                    writable=False,  # kad neleistų keisti autoriaus
            ),
        Field('title', 'string'),
        Field('category', db.categories), # susieja su kategorijų lentele
        Field('body', 'text'),            # text - duoda  texarea widget'ą
        Field('time_', 'datetime', default=request.now)  # request.now - užklausos laikas
)

