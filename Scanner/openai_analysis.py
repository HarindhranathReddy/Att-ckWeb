import os
import openai

# Ensure your OpenAI API key is set as an environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("Please set your OPENAI_API_KEY environment variable.")
openai.api_key = OPENAI_API_KEY

def analyze_web_request(url, request_data, response_data):
    """
    Use the OpenAI API to analyze a web request and its corresponding response for potential vulnerabilities.
    
    Parameters:
      - url: The URL that was requested.
      - request_data: The full HTTP request as a string.
      - response_data: The full HTTP response as a string.
      
    Returns:
      A string containing OpenAI's analysis.
    """
    prompt = f"""
You are a world-class cybersecurity expert and penetration tester.
Analyze the following HTTP request and response for potential security vulnerabilities. 
Consider common issues like SQL Injection, XSS, Command Injection, SSRF, LFI/RFI, XXE, NoSQL Injection, open redirects, and business logic flaws.

URL: {url}

HTTP Request:
{request_data}

HTTP Response:
{response_data}

Provide a detailed explanation of any vulnerabilities you detect and recommendations for further testing.

Your analysis:
"""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # or another engine of your choice
            prompt=prompt,
            max_tokens=300,
            temperature=0.7,
            top_p=1,
            n=1,
            stop=None,
        )
        analysis = response.choices[0].text.strip()
        return analysis
    except Exception as e:
        return f"Error during analysis: {e}"

# Example usage for testing:
if __name__ == "__main__":
    sample_url = "https://example.com/test"
    sample_request = (
        "GET /test HTTP/1.1\r\n"
        "Host: example.com\r\n"
        "User-Agent: AdvancedScanner/1.0\r\n"
        "Accept: */*\r\n\r\n"
    )
    sample_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n\r\n"
        "<html><body>Welcome to Example!</body></html>"
    )
    analysis = analyze_web_request(sample_url, sample_request, sample_response)
    print("OpenAI Vulnerability Analysis:\n")
    print(analysis)
