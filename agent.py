from autogen import ConversableAgent
from typing import Annotated, Literal
import requests

from config import LLM_CONFIG

def search_papers(topic: str) -> list:
  url = "https://api.semanticscholar.org/graph/v1/paper/search"
  params = {
      "query": topic,
      "limit": 50,
      "fields": "title,year,url"
  }

  response = requests.get(url, params=params)
  if response.status_code != 200:
      print(f"Error: {response.status_code}")
      return []

  results = response.json().get("data", [])
  return results


def create_search_agent() -> ConversableAgent:
    agent = ConversableAgent(
        name="Search Agent",
        system_message=
            "You are a helpful assistant that can search for academic research papers. "
            "You can find papers based on the provided topic. "
            "Use the 'search_papers' tool to fetch papers relevant to the specified topic, "
            "and return the titles, authors, and publication year of the results."
            "format the output so it's pretty in terminal"
            "Return 'TERMINATE' when the task is done.",
        llm_config=LLM_CONFIG,
    )

    agent.register_for_llm(name="search_papers", description="A simple search_papers")(search_papers)
    return agent

def create_user_proxy():
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )
    user_proxy.register_for_execution(name="search_papers")(search_papers)
    return user_proxy

def main():
    user_proxy = create_user_proxy()
    calculator_agent = create_search_agent()
    chat_result = user_proxy.initiate_chat(calculator_agent, cache=None, message="Search academic papers on Software Test")
    print(chat_result)

if __name__ == "__main__":
    main()