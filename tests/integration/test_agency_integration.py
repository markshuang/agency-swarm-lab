import os
import pytest
from agency_swarm import Agency
from CodeSolutionAgency.BrowsingAgent import BrowsingAgent
from CodeSolutionAgency.Devid import Devid
from CodeSolutionAgency.PlannerAgent import PlannerAgent
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@pytest.fixture
def azure_client():
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        timeout=5,
        max_retries=3,
    )

def test_agency_integration(azure_client):
    # Set the OpenAI client
    from agency_swarm import set_openai_client
    set_openai_client(azure_client)

    # Initialize agents
    planner = PlannerAgent()
    devid = Devid()
    browsingAgent = BrowsingAgent()

    # Create the agency
    agency = Agency([planner, devid, browsingAgent],
                    shared_instructions='./agency_manifesto.md')

    # Perform a real operation that involves Azure OpenAI
    result = agency.demo_gradio(server_name="0.0.0.0")

    # Assert expected outcomes
    assert result is not None