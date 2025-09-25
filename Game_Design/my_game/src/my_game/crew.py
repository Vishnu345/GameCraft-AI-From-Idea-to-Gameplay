from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

# call gemini model
llm = LLM(model="gemini/gemini-2.0-flash",
                            verbose=True,
                            api_key=os.getenv('GOOGLE_API_KEY')
                            )


@CrewBase
class MyGame():
    """MyGame crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def game_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['game_designer'],
            llm=llm,
            verbose=True,
        )

    @agent
    def game_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['game_developer'],
            llm=llm,
            verbose=True,
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            llm=llm,
            verbose=True,
        )
    

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task'],
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
        ) 
    
    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )