from flask_webtest import TestApp


class CustomTestApp(TestApp):

    def __init__(self, app, db=None, use_session_scopes=False, cookiejar=None,
                 extra_environ=None, *args, **kwargs):
        self.app = app
        super(CustomTestApp, self).__init__(app, db, use_session_scopes, cookiejar, extra_environ, *args, **kwargs) # noqa
