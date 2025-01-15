

# PRD Task Generator with ReAct Agent

A Python application that uses OpenAI's GPT-3.5 to analyze Product Requirements Documents (PRDs) and automatically generate detailed project tasks. The system combines a ReAct agent with natural language processing to break down PRDs into actionable tasks with estimates, priorities, and categories.

## 🚀 Features

- **PRD Analysis**: Automatically processes and understands PRD content
- **Task Generation**: Creates detailed tasks with descriptions and estimates
- **Priority Assignment**: Assigns priorities to tasks (High/Medium/Low)
- **Category Classification**: Categorizes tasks (Frontend/Backend/DevOps/Design/Testing)
- **Analysis Steps**: Provides transparency into the agent's thought process
- **Summary Statistics**: Generates overview of task distribution
- **Dual Interface**: Supports both API and CLI usage

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- FastAPI
- uvicorn
- pydantic

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prd-task-generator.git
cd prd-task-generator
```

2. Install dependencies:
```bash
pip install fastapi uvicorn openai pydantic
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## 💻 Usage

### As a Web Service

1. Start the server:
```bash
python app.py
```

2. Access the API endpoints:
- Generate tasks: `POST /api/generate/tasks`
- Get sample PRD: `GET /api/sample-prd`

Example API request:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/generate/tasks",
    json={"prd_content": "Your PRD content here..."}
)
tasks = response.json()
```

### As a CLI Tool

Run in CLI mode:
```bash
python app.py cli
```

Follow the prompts to either:
1. Use the sample PRD
2. Enter your custom PRD content

## 🔍 Code Structure

### Main Components

1. **PRDTool Class**
```python
class PRDTool:
    def read_prd(self) -> str
    def analyze_section(self, section: str) -> str
```
- Handles PRD content reading and section analysis
- Provides methods to extract specific sections

2. **ReActAgent Class**
```python
class ReActAgent:
    def generate_tasks(self, prd_content: str) -> GenerationResponse
    def generate_summary(self) -> Dict[str, str]
```
- Manages the task generation process
- Interacts with OpenAI API
- Creates task summaries and analysis

3. **Data Models**
```python
class Task(BaseModel):
    title: str
    description: Optional[str]
    estimate: Optional[str]
    priority: Optional[str]
    category: Optional[str]
```

## 📤 Output Format

### Generated Tasks
```json
{
    "tasks": [
        {
            "title": "Task Name",
            "description": "Detailed description",
            "estimate": "2 days",
            "priority": "High",
            "category": "Backend"
        }
    ],
    "analysis": [
        {
            "thought": "Analysis step",
            "action": "Action taken",
            "observation": "Result"
        }
    ],
    "summary": {
        "total_tasks": "10",
        "categories": "{'Backend': 4, 'Frontend': 3, ...}",
        "priorities": "{'High': 3, 'Medium': 5, 'Low': 2}"
    }
}
```

## 🔄 Workflow

1. PRD Content Input
   - Accept PRD content through API or CLI
   - Validate and preprocess content

2. Task Generation
   - Parse PRD using OpenAI's GPT-3.5
   - Extract key requirements
   - Generate structured tasks

3. Analysis and Classification
   - Assign priorities and categories
   - Generate time estimates
   - Create summary statistics

4. Output Generation
   - Format tasks in structured JSON
   - Include analysis steps
   - Provide summary metrics

## ⚙️ Configuration

Key configuration options:
- `model`: GPT-3.5-turbo (configurable)
- `temperature`: 0.7 (adjustable for creativity vs. consistency)
- `max_tokens`: 2000 (adjustable based on PRD size)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## ⚠️ Limitations

- Requires OpenAI API key
- Processing time depends on PRD length
- Task estimates are AI-generated approximations
- May require manual review for complex PRDs



## 🙋‍♂️ Support

For issues and feature requests, please open an issue on the GitHub repository.
