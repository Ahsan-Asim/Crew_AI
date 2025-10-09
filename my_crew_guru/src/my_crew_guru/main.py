#!/usr/bin/env python
import warnings
from crewai import Agent
from crewai.utilities.prompts import Prompts
from src.my_crew_guru.crew import TravelPlannerCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def preview_prompt(agent: Agent):
    prompt_generator = Prompts(
        agent=agent,
        has_tools=len(agent.tools) > 0,
        use_system_prompt=agent.use_system_prompt
    )
    return prompt_generator.task_execution()

def run():
    inputs = {
        "location": "Model Town, Lahore",
        "date": "2025-10-10"  # date required for weather tool
    }

    crew = TravelPlannerCrew().crew()
    
    print(preview_prompt(crew.agents[0]))

    print("===========================================[ CREW RESULT ]===========================================")
    result = crew.kickoff(inputs=inputs)
    print(result)
    print("===========================================[ CREW RESULT ]===========================================")

if __name__ == "__main__":
    run()
