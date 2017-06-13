from oauth2client import client, crypt
import json
import webapp2
import models


class UsersHandler(webapp2.RequestHandler):
    def post(self):
        post_data = json.loads(self.request.body)
        try:
            idinfo = client.verify_id_token(post_data['idToken'],
                '805072041815-5ligrpf92hcoegjkq77kigglsflhemr3.apps.googleusercontent.com')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")

        except crypt.AppIdentityError:
            # Invalid token
            userid = idinfo['sub']

        self.response.write(json.dumps(idinfo))
