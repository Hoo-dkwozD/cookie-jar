import requests
import unittest
from os import environ

environ["app.root_uri"] = "http://localhost:5000"


class CookiesTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls): 
        # Setup static call 
        super(CookiesTestCase, cls).setUpClass()
        
        # Prepare a series of cookies to log
        cls.cookies_list = [
            {
                "foo1": "bar1", 
                "foo2": "bar2"
            }, 
            {
                "{@&*^($*": "^*^*(&", 
                "||||\\\\?////": "\\?////"
            }, 
            {
                "', '', ''; DROP TABLE cookie; -- ": "", 
                "\", '', ''; DROP TABLE cookie; -- ": ""
            }
        ]

        # Make requests so cookies will be logged
        for cookie in cls.cookies_list:
            requests.get(environ.get("app.root_uri"), cookies = cookie)
            requests.get(environ.get("app.root_uri") + "/cookies", cookies = cookie)
            requests.get(environ.get("app.root_uri") + "/cookies/foo1", cookies = cookie)
        
        # Get all cookies and store in results to test
        cls.result = requests.get(environ.get("app.root_uri") + "/cookies").json()
    
    def test_http_code(self):
        self.assertEqual(CookiesTestCase.result["code"], 200)
    
    def test_data_type(self):
        self.assertEqual(type(CookiesTestCase.result["data"]), list)
    
    def test_data_len(self):
        self.assertEqual(len(CookiesTestCase.result["data"]), 24)
    
    def test_normal_1a(self):
        self.assertEqual(CookiesTestCase.result["data"][0]["key"], "foo1")

    def test_normal_1b(self):
        self.assertEqual(CookiesTestCase.result["data"][0]["value"], "bar1")
    
    def test_normal_2a(self):
        self.assertEqual(CookiesTestCase.result["data"][1]["key"], "foo2")

    def test_normal_2b(self):
        self.assertEqual(CookiesTestCase.result["data"][1]["value"], "bar2")
    
    def test_weird_1a(self):
        self.assertEqual(CookiesTestCase.result["data"][6]["key"], "{@&amp;*^($*")

    def test_weird_1b(self):
        self.assertEqual(CookiesTestCase.result["data"][6]["value"], "^*^*(&amp;")
    
    def test_weird_2a(self):
        self.assertEqual(CookiesTestCase.result["data"][7]["key"], "||||\\\\?////")

    def test_weird_2b(self):
        self.assertEqual(CookiesTestCase.result["data"][7]["value"], "\\?////")
    
    def test_sqli_1a(self):
        self.assertEqual(CookiesTestCase.result["data"][12]["key"], "&#34;, &#39;&#39;, &#39;&#39;")

    def test_sqli_1b(self):
        self.assertEqual(CookiesTestCase.result["data"][12]["value"], "")
    
    def test_sqli_2a(self):
        self.assertEqual(CookiesTestCase.result["data"][13]["key"], "DROP TABLE cookie")

    def test_sqli_2b(self):
        self.assertEqual(CookiesTestCase.result["data"][13]["value"], "")
    
    def test_sqli_3a(self):
        self.assertEqual(CookiesTestCase.result["data"][14]["key"], "--")

    def test_sqli_3b(self):
        self.assertEqual(CookiesTestCase.result["data"][14]["value"], "")
    
    def test_sqli_4a(self):
        self.assertEqual(CookiesTestCase.result["data"][15]["key"], "&#39;, &#39;&#39;, &#39;&#39;")

    def test_sqli_4b(self):
        self.assertEqual(CookiesTestCase.result["data"][15]["value"], "")


if __name__ == "__main__":
    unittest.main()