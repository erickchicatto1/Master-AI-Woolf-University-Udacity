class Agent:
    """An AI Agent that can use tools to help answer questions"""

    def __init__(self, role: str = "Personal Assistant", instructions: str = "Help users with any question", model: str = "gpt-4o-mini", temperature: float = 0.0, tools: List[Any] = None):
        """Initialize the agent with its configuration and tools"""
        self.model = model
        self.role = role
        self.instructions = instructions
        self.tools = tools
        # Load environment variables from .env (or config.env)
        load_dotenv()
        # Ensure your .env (or config.env) includes OPENAI_BASE_URL set to https://openai.vocareum.com/v1 when using the Vocareum-hosted OpenAI endpoint.
        assert os.getenv('OPENAI_API_KEY') is not None
        assert os.getenv('OPENAI_BASE_URL') is not None
        assert os.getenv('TAVILY_API_KEY') is not None
        self.llm = LLM(model=model, temperature=temperature, tools=tools)

    def invoke(self, user_message: str) -> str:
        """Process a user message and return a response"""
        messages = [SystemMessage(content=f"You're an AI Agent and your role is {self.role}. Your instructions: {self.instructions}")]
        messages.append(UserMessage(content=user_message))
        ai_message = self.llm.invoke(messages)
        messages.append(ai_message)

        while ai_message.tool_calls:
            for call in ai_message.tool_calls:
                function_name = call.function.name
                function_args = json.loads(call.function.arguments)
                tool_call_id = call.id
                tool = next((t for t in self.tools if t.name == function_name), None)
                if tool:
                    result = tool(**function_args)
                    messages.append(ToolMessage(content=json.dumps(result), tool_call_id=tool_call_id, name=function_name))
            ai_message = self.llm.invoke(messages)
            messages.append(ai_message)

        for m in messages:
            print(m)
        return ai_message.content
