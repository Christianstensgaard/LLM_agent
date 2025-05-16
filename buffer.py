from autogen import ConversableAgent
import json
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
    search_agent = ConversableAgent(
        name="Search Agent",
        system_message=(
            "You are a helpful assistant that can search for academic research papers. "
            "You can find papers based on the provided topic. "
            "Use the 'search_papers' tool to fetch papers relevant to the specified topic, "
            "and return the titles, authors, and publication year of the results. "
            "Return 'TERMINATE' when the task is done."
        ),
        llm_config=LLM_CONFIG,
    )
    search_agent.register_for_llm(name="search_papers", description="A simple search_papers")(search_papers)
    search_agent.register_for_execution(name="search_papers")(search_papers)
    return search_agent



def create_critic_agent() -> ConversableAgent:
    critic_agent = ConversableAgent(
        name="Critic Agent",
        llm_config=LLM_CONFIG,
        system_message=(
            "You are evaluating an AI product recommendation agent. "
            "Evaluate the response based on these criteria: "
            "- Completeness (1-5): addresses every part of the request. "
            "- Quality (1-5): accurate, clear, and effectively structured. "
            "- Robustness (1-5): handles ambiguities, errors, or nonsensical input well. "
            "- Consistency (1-5): maintains consistent reasoning with specified user needs. "
            "- Specificity (1-5): provides detailed and relevant recommendations with clear justifications. "
            "Additionally, check if the agent response provided clear context and justifications. "
            "Assess realism, practicality, and feasibility of recommendations."
        ),
    )
    return critic_agent


def create_user_proxy():
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )
    return user_proxy


def main():
    user_proxy = create_user_proxy()
    search_agent = create_search_agent()
    critic_agent = create_critic_agent()

    prompts = [
        "Search academic papers on federated learning.",
        "Find papers related to deep reinforcement learning.",
        "Search for recent papers on AI.",
        "Look up academic papers on Software Test."
    ]
    
    for prompt in prompts:
        agent_response = search_agent.initiate_chat(user_proxy, cache=None, message=prompt)
        critic_prompt = f"""
        You are evaluating an AI product recommendation agent.

        Evaluate the response based on these criteria:
        - Completeness (1-5): addresses every part of the request.
        - Quality (1-5): accurate, clear, and effectively structured.
        - Robustness (1-5): handles ambiguities, errors, or nonsensical input well.
        - Consistency (1-5): maintains consistent reasoning with specified user needs.
        - Specificity (1-5): provides detailed and relevant recommendations with clear justifications.

        Additionally:
        - Check if the agent response provided clear context and justifications.
        - Determine if the agent accurately interpreted ambiguous prompts.
        - Assess realism, practicality, and feasibility of recommendations.

        User Prompt: {prompt}
        Agent Response: {agent_response}

        Provide your evaluation as JSON with fields:
        - completeness
        - quality
        - robustness
        - consistency
        - specificity
        - feedback (a brief descriptive explanation including specific examples from the response)
        """

        critic_evaluation = critic_agent.initiate_chat(user_proxy, cache=None, message=critic_prompt)
        result = json.loads(critic_evaluation)

        print(f"Prompt: {prompt}\nAgent Response: {agent_response}\nCritic Evaluation: {result}\n")


if __name__ == "__main__":
    main()
