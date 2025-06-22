from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
import os

# Retrieve the SOP document
def retrieve_sop(fraudType: str) -> str:
    """
    This tool searches the SOP document and returns the relevant parts
    """    
    print(f"Tool called - Retrieving SOP document")

    DEFAULT_MODEL="gemini-2.0-flash-001"
    API_KEY=os.environ.get("GOOGLE_API_KEY")

    llm = GoogleGenAI(model=DEFAULT_MODEL,api_key=API_KEY)
    embedding_model_name = "text-embedding-004"
    Settings.llm = llm
    Settings.embed_model = GoogleGenAIEmbedding(model_name=embedding_model_name, api_key=API_KEY)
    
    storage_context = StorageContext.from_defaults(persist_dir="_index")

    # load index
    index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine()
    response = query_engine.query(fraudType)
    print(response)

    return response


def logIncident(
        queueName: str, 
        incidentType: str, 
        incidentDescription: str, 
        priority: str, severity: str) -> str:
    """
    A function that can log an incident into the incident reporting system

    Parameters:
    queueName: The queue name corresponding to the team to whom the ticket is to be assigned
    incidentType: Type of the incident, eg customer complaint, fraud, system failure
    incidentDescription: Details of the task
    priority: One of P0, P1, P2, P3, P4, P5. Lower number represents higher priority
    severity: One of S0, S1, S2, S3, S4, S5. Lower number represents higher priority
    """
    import uuid
    incidentId = str(uuid.uuid4())[:6]
    response = f"""Successfully created ticket:
    Incident Id: [{incidentId}], 
    Priority: [{priority}], 
    Severity [{severity}], 
    Queue [{queueName}],
    Incident Type: [{incidentType}],
    Incident Description: [{incidentDescription}]
    """
    return response

def blockCard(cardID: str) -> bool:
    """
    A function that can block a card given the card ID.

    Parameters:
    cardID: The ID of the card to be blocked

    Returns:
    0 - if successful
    1 - if failed
    """
    retval = 0
    if cardID == "XXXXX":
        retval = 1
    return retval

