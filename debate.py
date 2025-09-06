from __future__ import annotations
import os
import asyncio
import dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.base import TaskResult

dotenv.load_dotenv()

def TeamConfig(
    topic: str,
    model_name: str = "gpt-4o",

    ) -> RoundRobinGroupChat:
    """Build a round-robin debate team (host, supporter, critic) for the given topic."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    
    model = OpenAIChatCompletionClient(
        model = model_name,
        api_key = api_key,
    )

    supporter = AssistantAgent(
        name="John",
        system_message="You are John, a supporter agent in a debate for the"
        f" topic: {topic}. You will be debatting against Jack, a critic agent. ",
        model_client=model,
    )  

    critic = AssistantAgent(
        name="Jack",
        system_message="You are Jack, a critic agent in a debate for the"
        f" topic: {topic}. You will be debatting against John, a supporter agent. ",
        model_client=model,
    )

    host = AssistantAgent(
        name="Jane",
        model_client=model,
        system_message="You are Jane, the host of the debate, between John, a supporter agent,"
        "and Jack, a critic agent, You will moderate the debate."
        f"The topic of the debate is: {topic}. "
        "At the beginning of each round, announce the round number."
        "At the beginning of the third round, that it will be "
        "the last round. After the last round, thank the audience and exactly "
        "say 'TERMINATE'"
    )  

    team = RoundRobinGroupChat(
        participants = [host, supporter,critic],
        max_turns = 20,
        termination_condition = TextMentionTermination("TERMINATE"),
    )
    return team


async def debate(team: RoundRobinGroupChat):
    """Stream debate messages as 'Source: content' strings."""
    async for message in team.run_stream(task="Start the debate!"):
        if isinstance(message, TaskResult):
            yield f"Stoping Reason: {message.stop_reason}"
        else:
            yield f"{message.source}: {message.content}"


async def main():
    topic = "All people should have the right to own guns"
    team = TeamConfig(topic)
    async for message in debate(team):
        print("==" * 20)
        print(message)


if __name__ == "__main__":
    asyncio.run(main())