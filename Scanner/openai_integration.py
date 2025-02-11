import os
import openai
import json

# Ensure your OpenAI API key is set as an environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("Please set your OPENAI_API_KEY environment variable.")
openai.api_key = OPENAI_API_KEY

def generate_summary(scan_results):
    """
    Generate a natural language summary of the scan results using OpenAI.
    """
    prompt = (
        "You are a cybersecurity expert. Summarize the following vulnerability scan results "
        "and provide actionable recommendations:\n\n"
    )
    prompt += json.dumps(scan_results, indent=2)
    prompt += "\n\nSummary:"
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Change if needed
            prompt=prompt,
            max_tokens=200,
            temperature=0.7,
            top_p=1,
            n=1,
            stop=None
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        return f"Error generating summary: {e}"

# For testing the module independently:
if __name__ == "__main__":
    dummy_results = [{"url": "http://example.com/test", "vulnerability": "SQL Injection", "details": "Test payload triggered error"}]
    print(generate_summary(dummy_results))
