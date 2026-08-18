class MemoryAgent:
    def __init__(self, model_name: str, instructions: str, tools: List[Tool] = None, temperature: float = 0.7):
        self.instructions = instructions
        self.tools = tools if tools else []
        self.model_name = model_name
        self.temperature = temperature
        
        # Initialize memory and state machine
        self.memory = ShortTermMemory()
        self.workflow = self._create_state_machine()
