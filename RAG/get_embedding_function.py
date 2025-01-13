import warnings
from langchain_community.embeddings import HuggingFaceEmbeddings

warnings.simplefilter(action='ignore', category=FutureWarning)

def get_embedding_function():
    # Use CPU for embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="OrdalieTech/Solon-embeddings-large-0.1",
        model_kwargs={'device': 'cpu'}  # Force CPU usage
    )
    return embeddings