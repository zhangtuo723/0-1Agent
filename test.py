from langchain.chains import LLMChain
from langchain_community.llms import Tongyi
from langchain_community.tools.tavily_search import TavilySearchResults

import ChatGLM
from langchain.agents import AgentExecutor, create_structured_chat_agent, load_tools, create_react_agent

from langchain import hub
import os
from langchain.prompts import PromptTemplate
os.environ["DASHSCOPE_API_KEY"] = "sk-cc1c8314fdbd43ceaf26ec1824d5dd3b"
os.environ["SERPAPI_API_KEY"] = "9675cecd56acf05b5a881e6241b01dfd15aaf194"
os.environ["TAVILY_API_KEY"] = "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"

from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
llm = ChatGLM.ChatGLM_LLM()
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
search = TavilySearchResults()
tools = [search]
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools,verbose=True
)
output = agent_executor.invoke({"input": "2023年底中国大陆上映了哪些电影"})
print(output["output"])

