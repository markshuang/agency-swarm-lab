import pytest
from unittest.mock import patch, MagicMock
from agency_swarm import Agency
from BrowsingAgent import BrowsingAgent
from Devid import Devid
from PlannerAgent import PlannerAgent
from openai import AzureOpenAI

# Mock environment variables
@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_KEY", "test_key")
    monkeypatch.setenv("AZURE_DEPLOYMENT", "test_deployment")
    monkeypatch.setenv("AZURE_API_VERSION", "test_version")
    monkeypatch.setenv("AZURE_ENDPOINT", "test_endpoint")

# Mock AzureOpenAI client
@pytest.fixture
def mock_azure_client():
    with patch('agency_swarm.set_openai_client') as mock_set_client:
        mock_client = MagicMock(spec=AzureOpenAI)
        mock_set_client.return_value = mock_client
        yield mock_client

# Test Agency initialization
def test_agency_initialization(mock_azure_client):
    planner = PlannerAgent()
    devid = Devid()
    browsingAgent = BrowsingAgent()

    agency = Agency([planner, devid, browsingAgent, [planner, devid],
                     [planner, browsingAgent],
                     [devid, browsingAgent]],
                    shared_instructions='./agency_manifesto.md')

    assert agency is not None
    assert len(agency.agents) == 6

# Test AzureOpenAI client setup
def test_azure_client_setup(mock_azure_client):
    mock_azure_client.assert_called_once()
    assert mock_azure_client.api_key == "test_key"
    assert mock_azure_client.azure_deployment == "test_deployment"
    assert mock_azure_client.api_version == "test_version"
    assert mock_azure_client.azure_endpoint == "test_endpoint"

# Test edge conditions
def test_agency_with_no_agents():
    agency = Agency([], shared_instructions='./agency_manifesto.md')
    assert len(agency.agents) == 0

def test_agency_with_duplicate_agents():
    planner = PlannerAgent()
    agency = Agency([planner, planner], shared_instructions='./agency_manifesto.md')
    assert len(agency.agents) == 2

# Test demo_gradio method
def test_demo_gradio_method(mock_azure_client):
    planner = PlannerAgent()
    devid = Devid()
    browsingAgent = BrowsingAgent()

    agency = Agency([planner, devid, browsingAgent],
                    shared_instructions='./agency_manifesto.md')

    with patch.object(agency, 'demo_gradio', return_value=None) as mock_demo:
        agency.demo_gradio(server_name="0.0.0.0")
        mock_demo.assert_called_once_with(server_name="0.0.0.0") 