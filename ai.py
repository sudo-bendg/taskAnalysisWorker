from google import genai

class AIHandler:
    def __init__(self):
        self.client = genai.Client()

    def generatePrompt(self, task):
        prompt = f"""
### Role
You are a Professional Skills Analyst and Career Strategist. Your goal is to deconstruct work task descriptions into high-level, industry-standard skill sets suitable for a professional database.

### Task
Analyze the provided [Task Description]. Identify the hard skills, soft skills, methodologies, and tools implied or stated. 

### Guidelines for Skills
- **Be Specific:** As well as general skills like "Communication," add further context with skills like "Stakeholder Management" or "Technical Documentation.". Note that the general skill is still important to include.
- **Focus on Impact:** If the task involves a specific tool or framework, include it (e.g., "React.js Optimization," "SQL Data Modeling").
- **Quality over Quantity:** Provide only the most relevant 3-7 skills.

### Clarification Logic
If the [Task Description] is too vague to accurately determine specific skills (e.g., "I worked on the project"), use the "message" field to ask a targeted, clarifying question. If the description is sufficient, the "message" field should be an empty string ("").

### Output Format
Return ONLY a JSON object with this structure:
{{
  "skills": ["Skill 1", "Skill 2", "Skill 3"],
  "message": "Clarifying question here if needed, otherwise empty."
}}
The first character of the response should be an opening curly bracket, and the final character should be a closing curly bracket - there should be no further context to the response.

### Input
[Task Description]: {task}
"""
        return prompt
    
    def generateTaskResponse(self, task):
        prompt = self.generatePrompt(task)
        return self.generateContent(prompt)
    
    def generateContent(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt, config={'response_mime_type': 'application/json'}
        )
        return response.text