from bottle import Bottle,static_file,request,redirect
import sae
from lib.weibo import APIClient
import traceback
APP_KEY='2617528038'
APP_SECRET='7e936b98d36927653bbc2b9cd4a1d881'
CALLBACK_URL='1.reasonzz.sinaapp.com/callback'

app=Bottle()
at = ""
@app.route('/gosina')
def gosina():
	
	client =  APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)
	url = client.get_authorize_url()
	print url
	redirect(url)
	
		


@app.route('/callback')
def callback():
	code = requset.query.code
	# client = APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)
	# r = client.requset_access_token(code)
	# access_token = r.access_token
	# expires_in = r.expires_in
	# at = access_token
	# client.set_access_token(access_token,expires_in)
	# return client.get.statuses__user_timeline()
	return str(code)



application = sae.create_wsgi_app(app,debug=True)