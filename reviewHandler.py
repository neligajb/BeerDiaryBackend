from oauth2client import client, crypt
import json
import webapp2
import models
import logging


class ReviewsHandler(webapp2.RequestHandler):
    def post(self):
        review_data = json.loads(self.request.body, strict=False)

        try:
            idinfo = client.verify_id_token(review_data['idToken'],
                '805072041815-5ligrpf92hcoegjkq77kigglsflhemr3.apps.googleusercontent.com')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
                return

        except crypt.AppIdentityError:
            # Invalid token
            userid = idinfo['sub']
            self.response.set_status(400)
            self.response.write("400 invalid token. userId: " + userid)
            return

        if not review_data['beer'] or not review_data['brewery'] or not review_data['rating']:
            self.response.set_status(400)
            self.response.write("400 missing data")
            return

        new_review = models.Review(userId=idinfo['sub'])
        new_review.beerName = review_data['beer']
        new_review.style = review_data['style']
        new_review.brewery = review_data['brewery']
        new_review.rating = review_data['rating']
        new_review.put()

        review_dict = new_review.to_dict()
        review_dict['id'] = new_review.key.urlsafe()
        review_dict['self'] = '/reviews/' + new_review.key.urlsafe()
        self.response.write(json.dumps(review_dict))

    def get(self):
        header_data = self.request.headers
        try:
            idinfo = client.verify_id_token(header_data['Authorization'],
                                            '805072041815-5ligrpf92hcoegjkq77kigglsflhemr3.apps.googleusercontent.com')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
                return

        except crypt.AppIdentityError:
            # Invalid token
            userid = idinfo['sub']

        review_list = models.Review.query(models.Review.userId == idinfo['sub']).fetch()
        review_arr = []
        for review in review_list:
            review_dict = review.to_dict()
            review_dict['self'] = '/reviews/' + review.key.urlsafe()
            review_dict['id'] = review.key.urlsafe()
            review_arr.append(review_dict)
        self.response.write(json.dumps(review_arr))


    def put(self, id=None):
        review_data = json.loads(self.request.body)
        try:
            review = models.ndb.Key(urlsafe=id).get()
        except:
            self.response.set_status(404)
            self.response.write("404 not found")
            return

        review.beerName = review_data['beer']
        review.style = review_data['style']
        review.brewery = review_data['brewery']
        review.rating = review_data['rating']

        review.put()
        review_dict = review.to_dict()
        review_dict['self'] = '/reviews/' + id
        self.response.write(json.dumps(review_dict))


    def delete(self, id=None):
        try:
            review = models.ndb.Key(urlsafe=id).get()
        except:
            self.response.set_status(404)
            self.response.write("404 not found")
            return

        models.ndb.Key(urlsafe=id).delete()
        self.response.set_status(200, "Deleted")
        self.response.write("200 Deleted")
