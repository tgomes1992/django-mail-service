from waitress import serve
from mailservice.wsgi import application





serve(application ,  host="0.0.0.0" ,  port=5001)




