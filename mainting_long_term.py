import os
from dotenv import load_dotenv
from lib.vector_db import VectorStoreManager

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
db = VectorStoreManager(OPENAI_API_KEY)

vector_store = db.get_or_create_store("test")

vector_store.add(Document(content="I prefer Nintendo games", metadata={"user_id": "1", "session_id": "games"}))
vector_store.add(Corpus([Document(content="I prefer Sony games", metadata={"user_id": "2", "session_id": "games"}), Document(content="I have an Electric Car", metadata={"user_id": "2", "session_id": "vehicles"})]))

@dataclass
class MemoryFragment:
    content: str
    owner: str
    namespace: str = "default"
    timestamp: int = field(default_factory=lambda: int(datetime.now().timestamp()))

@dataclass
class MemorySearchResult:
    fragments: List[MemoryFragment]
    metadata: Dict

@dataclass
class TimestampFilter:
    greater_than_value: int = None
    lower_than_value: int = None

class LongTermMemory:
    def __init__(self, db: VectorStoreManager):
        self.vector_store = db.create_store("long_term_memory", force=True)

    def register(self, memory_fragment: MemoryFragment, metadata: Optional[Dict[str, str]] = None):
        # Implementation for registering memory
        ...

    def search(self, query_text: str, owner: str, limit: int = 3, timestamp_filter: Optional[TimestampFilter] = None, namespace: Optional[str] = "default") -> MemorySearchResult:
        # Implementation for searching memory

    
