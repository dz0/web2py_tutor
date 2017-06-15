import datetime
db.define_table('chat',
                    # Field('user_id', db.auth_user, default=auth.user_id if auth.is_logged_in() else None ),
                    Field('user_name' ),
                    Field('msg'), 
                    Field('moment', 'datetime', default=lambda:datetime.datetime.now() ),
                )
