from agency_swarm import Agency
from BrowsingAgent import BrowsingAgent
from Devid import Devid
from PlannerAgent import PlannerAgent
from openai import AzureOpenAI
from agency_swarm import set_openai_client
import os

from dotenv import load_dotenv
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
    api_version=os.getenv("AZURE_API_VERSION"),
    # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    timeout=5,
    max_retries=5,
)

set_openai_client(client)

planner = PlannerAgent()
devid = Devid()
browsingAgent = BrowsingAgent()

agency = Agency([planner, devid, browsingAgent, [planner, devid],
                 [planner, browsingAgent],
                 [devid, browsingAgent]],
                shared_instructions='./agency_manifesto.md')

if __name__ == '__main__':
    agency.demo_gradio(server_name="0.0.0.0")