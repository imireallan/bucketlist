import json
import unittest
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    """Represents the bucketlist Test Case"""

    def setUp(self):
        """Define test variables and initialize app"""

        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.bucketlist = {"name": "Visit Stamford Bridge"} 

        # Binds the app to the current context
        with self.app.app_context():
            # create tables
            db.create_all()

    def test_bucketlist_creation(self):
        """Test API can create bucketlist"""
        res = self.client.post("/bucketlists/", data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn("Visit Stamford", str(res.data))

    def test_api_can_return_all_bucketlists(self):
        """Test API can return all bucketlists"""
        res = self.client.post("/bucketlists/", data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client.get("/bucketlists/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Visit Stamford", str(res.data))

    def test_api_can_return_a_bucketlist_using_its_id(self):
        """Test API can return a single bucketlist"""
        res = self.client.post("/bucketlists/", data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        json_result = json.loads(res.data.decode("utf-8").replace("'", "\""))
        res = self.client.get(
            "/bucketlists/{}".format(json_result["id"])
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("Visit Stamford", str(res.data))

    def test_api_can_be_edited(self):
        """Test API can edit a bucketlist"""
        res = self.client.post("/bucketlists/", data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client.put(
            "/bucketlists/1",
            data = {"name": "Work in Andela"}
        )
        self.assertEqual(res.status_code, 200)
        rv = self.client.get("/bucketlists/")
        self.assertIn("Work in Andela", str(rv.data))

    def test_bucketist_deletion(self):
        """Test API can delete a bucketlist"""
        res = self.client.post("/bucketlists/", data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client.delete("/bucketlists/1")
        self.assertEqual(res.status_code, 200)
        rv = self.client.get("/bucketlists/1")
        self.assertEqual(rv.status_code, 404)

    def tearDown(self):
        """Remove all the test variables"""

        with self.app.app_context():
            # Removes all the tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
