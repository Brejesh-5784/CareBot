from src.helper import load_pdf, text_split, download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now this should work
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

# Check if API key is loaded properly
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found. Make sure it's set in your .env file.")

# Set the environment variable explicitly (if needed)
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

extracted_data = load_pdf(data='Data/')
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define index name and model output dimension
index_name = "test"

# Create the index (if it doesn't already exist)
pc.create_index(
    name=index_name,
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1",
    )
)

docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name=index_name,
)


