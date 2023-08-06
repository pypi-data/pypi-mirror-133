"""test api."""
import logging
import os
from dotenv import load_dotenv
from dataclasses import asdict
import json

load_dotenv()
from palabox.apis.garmin import GarminApiConfig, GarminApi

logging.basicConfig(level=logging.DEBUG)
api = GarminApi(
    GarminApiConfig(
        login=os.getenv("DUOLINGO_LOGIN"),
        password=os.getenv("DUOLINGO_PASSWORD"),
    )
)
api.connect()
print(api.config)
