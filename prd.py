import os
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from datetime import datetime

# Initialize the FastAPI app
app = FastAPI()

# Data models for request and response
class PRDRequest(BaseModel):
    prd_content: str  # PRD content in Markdown format

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    estimate: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None

class AnalysisStep(BaseModel):
    thought: str  # What the agent is thinking
    action: Optional[str] = None  # What action is being taken
    observation: Optional[str] = None  # What was observed after the action

class GenerationResponse(BaseModel):
    tasks: List[Task]  # List of generated tasks
    analysis: List[AnalysisStep]  # Steps taken during analysis
    summary: Dict[str, str]  # Summary of the task generation process

# Tool to read the PRD content
class PRDTool:
    def __init__(self, content: str):
        self.content = content  # Store the PRD content

    def read_prd(self) -> str:
        """Returns the full PRD content."""
        return self.content

# ReAct Agent that uses the PRD tool to generate tasks
class ReActAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key  # Set the OpenAI API key
        self.analysis_steps = []  # Store steps taken during analysis
        self.tasks = []  # Store generated tasks

    def add_analysis_step(self, thought: str, action: Optional[str] = None, observation: Optional[str] = None):
        """Adds a step to the analysis log."""
        self.analysis_steps.append(
            AnalysisStep(thought=thought, action=action, observation=observation)
        )

    def generate_tasks(self, prd_content: str) -> GenerationResponse:
        """Generates tasks based on the provided PRD content."""
        prd_tool = PRDTool(prd_content)

        # Step 1: Start the analysis process
        self.add_analysis_step(
            thought="Starting PRD analysis to understand the scope and requirements",
            action="read_prd",
            observation="PRD content loaded successfully",
        )

        # Step 2: Use GPT-3.5 to generate tasks
        system_prompt = """You are a professional project manager and technical lead specialized in breaking down PRDs into actionable tasks. 
        Analyze the PRD and generate a comprehensive list of tasks with the following information:
        - Task title
        - Description
        - Time estimate
        - Priority (High/Medium/Low)
        - Category (Frontend/Backend/DevOps/Design/Testing)

        Format your response as a JSON array of tasks. Each task should be detailed enough for developers to understand and implement."""

        try:
            # Call the OpenAI API to generate tasks
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate detailed tasks for this PRD:\n\n{prd_content}"},
                ],
                temperature=0.7,  # Controls creativity
                max_tokens=2000,  # Limit the response length
            )

            # Parse the generated tasks
            content = response.choices[0].message.content
            try:
                import json

                tasks_data = json.loads(content)  # Parse the JSON response
                self.tasks = [Task(**task) for task in tasks_data]  # Convert to Task objects
            except json.JSONDecodeError:
                # Fallback if the JSON is malformed
                self.add_analysis_step(
                    thought="Error parsing JSON response, attempting to extract tasks manually",
                    action="parse_tasks",
                    observation="Using fallback parsing method",
                )
                # Add a placeholder task for manual review
                self.tasks = [
                    Task(
                        title="Review and fix task generation",
                        description="Task generation needs manual review",
                        priority="High",
                    )
                ]

            # Step 3: Generate a summary of the tasks
            summary = self.generate_summary()

            return GenerationResponse(
                tasks=self.tasks,
                analysis=self.analysis_steps,
                summary=summary,
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))  # Handle any errors

    def generate_summary(self) -> Dict[str, str]:
        """Generates a summary of the task generation process."""
        total_tasks = len(self.tasks)
        categories = {}  # Count tasks by category
        priorities = {"High": 0, "Medium": 0, "Low": 0}  # Count tasks by priority

        for task in self.tasks:
            if task.category:
                categories[task.category] = categories.get(task.category, 0) + 1
            if task.priority:
                priorities[task.priority] = priorities.get(task.priority, 0) + 1

        return {
            "total_tasks": str(total_tasks),
            "categories": str(dict(categories)),
            "priorities": str(dict(priorities)),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

# API Endpoint
@app.post("/generate/tasks", response_model=GenerationResponse)
async def generate_tasks(request: PRDRequest):
    """Endpoint to generate tasks from a PRD."""
    api_key = os.getenv("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")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not found")

    # Instantiate the ReAct Agent with the PRD content
    agent = ReActAgent(api_key)
    return agent.generate_tasks(request.prd_content)

# Run the app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)