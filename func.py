from dotenv import load_dotenv
import os

import requests
import json


from openai import OpenAI


load_dotenv()


key = os.getenv('OPENAI_API_KEY')




