"""
Promotion API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from service.models import db
from service.service import app, init_db
from datetime import datetime


# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  T E S T   C A S E S
######################################################################
class TestPromotionServer(TestCase):
    """ Promotion Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()


    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()
        pass

######################################################################
#  T E S T   C A S E S   S T A R T   H E R E 
######################################################################
    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        
    def _create_promotions(self, count):
        """ Factory method to create promotions in bulk """
        promotions = []
        for _ in range(count):
            test_promotion = promotionFactory()
            resp = self.app.post(
                "/promotions", json=test_promotion.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test promotion"
            )
            new_promotion = resp.get_json()
            test_promotion.id = new_promotion["id"]
            promotions.append(test_promotion)
        return promotions

    
    def test_create_promotion(self):
        """ Create a new promotion """
        test_promotion = {
            "name": "Default",
            "description": "default description",
            "start date": datetime.strptime('2001-01-01 00:00:00', '%Y-%d-%m %H:%M:%S'),
            "end date": datetime.strptime('2001-01-01 00:00:00', '%Y-%d-%m %H:%M:%S')
        }
        resp = self.app.post(
            "/promotions", 
            json=test_promotion, 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_promotion = resp.get_json()
        self.assertEqual(new_promotion["name"], test_promotion["name"], "Names do not match")
        self.assertEqual(new_promotion["description"], test_promotion["description"], "Descriptions do not match")
        self.assertEqual(datetime.strptime(new_promotion["start date"], '%a, %d %b %Y %H:%M:%S GMT'), test_promotion["start date"], "Start dates do not match")
        self.assertEqual(datetime.strptime(new_promotion["start date"], '%a, %d %b %Y %H:%M:%S GMT'), test_promotion["end date"], "End dates do not match")
        
        # TODO: When get_account is implemented, uncomment below
        # Check that the location header was correct
        # resp = self.app.get(location, content_type="application/json")
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # new_promotion = resp.get_json()
        # self.assertEqual(new_promotion["name"], test_promotion["name"], "Names do not match")
        # self.assertEqual(new_promotion["description"], test_promotion["description"], "Descriptions do not match")
        # self.assertEqual(new_promotion["start_date"], test_promotion["start_date"], "Start dates do not match")
        # self.assertEqual(new_promotion["end_date"], test_promotion["end_date"], "End dates do not match")
 
    def test_delete_promotion(self):
        """ Delete a Promotion """
        
        test_promotion = {
            "name": "Default",
            "description": "default description",
            "start date": datetime.strptime('2001-01-01 00:00:00', '%Y-%d-%m %H:%M:%S'),
            "end date": datetime.strptime('2001-01-01 00:00:00', '%Y-%d-%m %H:%M:%S')
        }
        resp = self.app.post(
            "/promotions", 
            json=test_promotion, 
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        new_promotion = resp.get_json()
        promotion_id = new_promotion["id"]

        resp = self.app.delete(
            "/promotions/{}".format(promotion_id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        
        # TODO: When get_account is implemented, uncomment below
        
        # make sure they are deleted
        # resp = self.app.get(
        #     "/promotions/{}".format(promotion_id), content_type="application/json"
        # )
        # self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)        

        
