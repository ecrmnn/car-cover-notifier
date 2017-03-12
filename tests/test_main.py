import unittest
import xmltodict
import requests
from os import environ as env
from os.path import join, dirname
from dotenv import load_dotenv

# Load enviroment variables from .env
load_dotenv(join(dirname(__file__), '../.env'))

class TestMain(unittest.TestCase):

    def test_required_environment_variables(self):
        self.assertNotEqual(env.get('YR_PLACE'), None)
        self.assertNotEqual(env.get('SLACK_API_TOKEN'), None)
        self.assertNotEqual(env.get('SLACK_CHANNEL'), None)

    def test_can_load_xml_to_dict(self):
        url = 'http://www.yr.no/place/' + env.get('YR_PLACE') + '/forecast_hour_by_hour.xml'
        response = requests.get(url).text
        parsedXmlResponse = xmltodict.parse(response)
        self.assertTrue(parsedXmlResponse['weatherdata'])

if __name__ == '__main__':
    unittest.main()