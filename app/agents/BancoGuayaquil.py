from langchain.agents import (
    AgentExecutor,
    create_react_agent,
) 
from langchain.prompts import (
    PromptTemplate
)
from .llms import chat_model
from tools.pokeapi import PokedexTool
from tools.bg_gateway import (
    CuentasTool,
    ClienteTool,
    MovimientosTool,
    TarjetasTool,
    SegurosTool
)
from cache.message_history import get_memory_runnable
from langsmith import traceable
from langsmith import Client
from .prompts import prompt_bg_v3

system_prompt_template = prompt_bg_v3

client = Client()

class ChatUserAgent:
    def __init__(self, enable_memory=True, session_id=None):
        self.enable_memory = enable_memory
        self.session_id = session_id
        self.agent_executor = self.setup_agent()

    def setup_agent(self):
        """Sets up the chat agent with the necessary configuration. """

        input_variables = ["input", "agent_scratchpad","tools", 'tool_names']  # Default input variables
        if self.enable_memory:
            input_variables.append("chat_history")

        prompt_template = PromptTemplate(
            input_variables=input_variables,
            template=system_prompt_template
        )

        # Add tool to the agent
        cuentas_tool = CuentasTool()
        clientes_tool = ClienteTool()
        movimientos_tool = MovimientosTool()
        tarjetas_tool = TarjetasTool()
        seguros_tool = SegurosTool()
        
        tools = [cuentas_tool, clientes_tool, movimientos_tool, tarjetas_tool, seguros_tool]

        agent = create_react_agent(
            llm=chat_model,
            prompt=prompt_template,
            tools=tools,
        )

        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

        if self.enable_memory:
            agent_with_memory = get_memory_runnable(agent_executor)
            return agent_with_memory

        return  agent_executor
    
    def run(self,input: str):
        if self.enable_memory:
            agent_executor = self.agent_executor
            return agent_executor.invoke(
                {"input": input},
                config = {
                    "configurable":{
                        "session_id": self.session_id
                    }
                }
            )
        else:
            agent_executor = self.agent_executor
            return agent_executor.invoke(
                {"input": input}
            )

