# from app import app as application 
# uwsgiはcallableがapplicationを想定している
# そのためapplicationという別名にしないとNG

import apps.app as application
app = application.create_app()
print(app.url_map)
app.run()