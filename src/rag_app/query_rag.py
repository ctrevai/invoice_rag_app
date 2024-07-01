from dataclasses import dataclass
from typing import List
import boto3

model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
sourceType = "S3"
document_s3_uri = "s3://invoice-rag-app-cttrevai-dorje/invoice_policy.txt"

session = boto3.Session()
agent_client_runtime = session.client("bedrock-agent-runtime",region_name="us-east-1")


@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    sources: List[str]
    
def query_rag(query_text: str) -> QueryResponse:
    # Implement your RAG (Retrieval Augmented Generation) logic here
    # This could involve querying a knowledge base or other sources
    # For simplicity, we'll return a hardcoded response
    # response_text = "This is a response from RAG."
    sources = ["source1", "source2", "source3"]
    # return QueryResponse(query_text, response_text, sources)
    
    response = agent_client_runtime.retrieve_and_generate(
        input={'text': query_text},
        retrieveAndGenerateConfiguration={
            'type': 'EXTERNAL_SOURCES',
            'externalSourcesConfiguration': {
                'modelArn': model_id,
                'sources': [
                    {
                        'sourceType': sourceType,
                        's3Location': {'uri': document_s3_uri}
                    }
                ]
            }
        }
    )
    response_text = response['output']['text']
    source1 = response['citations'][0]['retrievedReferences'][0]['location']['s3Location']['uri']
    sources = [source1]
    return QueryResponse(query_text, response_text, sources)

if __name__ == "__main__":
    query = "What is the expense policy?"
    response = query_rag(query)
    print(f"Query: {response.query_text}")
    print(f"Response: {response.response_text}")
    print(f"Sources: {response.sources}")