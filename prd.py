from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool
from flask import Flask, request, jsonify, render_template_string

import os
app = Flask(__name__)

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "?"  # Replace with a secure way to store the key

# Define PRD reading tool
def read_prd_tool(prd_content: str) -> str:
    """Returns the full PRD content when asked about product requirements"""
    return prd_content

# Simple HTML homepage
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PRD Task Generator</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
        textarea { width: 80%; height: 150px; margin-top: 10px; }
        button { padding: 10px 20px; font-size: 16px; margin-top: 10px; }
        #result { margin-top: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <h1>PRD Task Generator</h1>
    <textarea id="prd_content" placeholder="Enter PRD content..."></textarea><br>
    <button onclick="generateTasks()">Generate Tasks</button>
    <p id="result"></p>

    <script>
        function generateTasks() {
            const prdContent = document.getElementById("prd_content").value;
            fetch('/generate/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prd_content: prdContent })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("result").innerText = "Tasks: " + data.tasks;
            })
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
"""

# Homepage route
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate/tasks', methods=['POST'])
def generate_tasks():
    # Check if the content type is text/plain
    if request.content_type == 'text/plain':
        prd_content = request.data.decode('utf-8')  # Read plain text input
    else:
        return jsonify({"error": "Invalid content type. Use 'text/plain'."}), 400
    
    # Create tool
    prd_tool = FunctionTool.from_defaults(
        fn=read_prd_tool,
        name="read_prd",
        description="Returns the full PRD content when asked about product requirements"
    )
    
    # Create tool
    prd_tool = FunctionTool.from_defaults(
        fn=read_prd_tool,
        name="read_prd",
        description="Returns the full PRD content when asked about product requirements"
    )

    # Initialize LLM
    llm = OpenAI(model="gpt-4", temperature=0)

    # Create OpenAIAgent
    agent = ReActAgent.from_tools(
        tools=[prd_tool],
        llm=llm,
        verbose=True
    )


    # Run agent
    response = agent.chat("Generate tasks for the PRD")

    return jsonify({"tasks": str(response)})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
