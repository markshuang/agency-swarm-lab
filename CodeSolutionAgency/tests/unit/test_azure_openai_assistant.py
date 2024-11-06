import os
import requests

from dotenv import load_dotenv
load_dotenv()


def test_assistant():
    
    import os
    from openai import AzureOpenAI
    from agency_swarm import Agent
    from agency_swarm import Agency
    from agency_swarm import set_openai_client

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
        api_version="2024-05-01-preview", #"2024-02-15-preview",
        # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        timeout=5,
        max_retries=5,
    )

    set_openai_client(client)
    
    agent1 = Agent(name="agent1", description="I am a simple agent", model="gpt-4o-mini")
    ceo = Agent(name="ceo", description="I am the CEO", model="gpt-4o-mini")
    agency = Agency([ceo, [ceo, agent1]])
    response = agency.get_completion("Say hi to agent1. Let me know his response.", yield_messages=False)
    print(response)
    
def test_assistant_create():    
    import os
    import json
    import requests
    import time
    from openai import AzureOpenAI

    client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_ENDPOINT"),
    api_key= os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview"
    )

    assistant = client.beta.assistants.create(
    model="gpt-4o-mini", # replace with model deployment name.
    instructions="",
    tools=[{"type":"code_interpreter"}],
    )


    # Create a thread
    thread = client.beta.threads.create()

    # Add a user question to the thread
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="what is 3+4?" # Replace this with your prompt
    )



    # Run the thread
    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
    )

    # Looping until the run completes or fails
    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        print(messages)
    elif run.status == 'requires_action':
    # the assistant requires calling some functions
        # and submit the tool outputs back to the run
        pass
    else:
        print(run.status)
