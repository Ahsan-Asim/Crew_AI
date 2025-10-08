from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel

from tools.weather_tool import WeatherTool
from tools.email_tool import EmailTool

class TravelPlan(BaseModel):
    forecast: str
    packing_tips: str

@CrewBase
class TravelPlannerCrew:
    """Crew for weather + travel planning"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def weather_agent(self):
        return Agent(
            config=self.agents_config['weather_agent'],
            verbose=True,
            tools=[WeatherTool()],
        )

    @agent
    def packing_agent(self):
        return Agent(
            config=self.agents_config['packing_agent'],
            verbose=True,
        )

    @agent
    def email_agent(self):
        return Agent(
            config=self.agents_config['email_agent'],
            verbose=True,
            tools=[EmailTool()],
        )

    @task
    def fetch_weather_task(self):
        return Task(
            config=self.tasks_config['fetch_weather_task'],
        )

    @task
    def suggest_packing_task(self):
        return Task(
            config=self.tasks_config['suggest_packing_task'],
        )

    @task
    def send_email_task(self):
        return Task(
            config=self.tasks_config['send_email_task'],
        )

    @crew
    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
