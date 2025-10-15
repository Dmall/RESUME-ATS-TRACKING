import google.generativeai as genai
import PyPDF2 as pdf
from PyPDF2 import PdfReader
import json

def configure_genai(api_key): # 1. CONFIGURE API-KEY
    """Configure The Generative AI API With Error Handling"""
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        raise Exception(f"Failed To Configure Generative AI: {str(e)}")
    

def get_gemini_response(prompt): # 4. Send Input Data As A Prompt To Gemini Model To Get Response From Gemini
    """Generate a response using Gemini with enhanced error handling and response validation."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        
        # Ensure response is not empty
        if not response or not response.text:
            raise Exception("Empty response received from Gemini")
            
        # Try to parse the response as JSON
        try:
            response_json = json.loads(response.text)
            
            # Validate required fields
            required_fields = ["JD Match", "MissingKeywords", "Profile Summary"]
            for field in required_fields:
                if field not in response_json:
                    raise ValueError(f"Missing required field: {field}")
                    
            return response.text
            
        except json.JSONDecodeError:
            # If response is not valid JSON, try to extract JSON-like content
            import re
            json_pattern = r'\{.*\}'
            match = re.search(json_pattern, response.text, re.DOTALL)
            if match:
                return match.group()
            else:
                raise Exception("Could not extract valid JSON response")
                
    except Exception as e:
        raise Exception(f"Error generating response: {str(e)}")
    

def extract_pdf_text(uploaded_file): # 2. EXTRACT TEXTS FROM PDF OR RESUME
    """Extract Text From PDF With Enhanced Error Handling"""
    try:
        reader = pdf.PdfReader(uploaded_file)
        if len(reader.pages) == 0:
            raise Exception("PDF File Is Empty")
        
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

    
        if not text:
            raise Exception("No Text Could Be Extracted From The PDF")
        
        return " ".join(text)
    
    except Exception as e:
        raise Exception(f"Error Extracting PDF Text: {str(e)}")
    
def prepare_prompt(resume_text, job_description): # 3. READY PROMPT TO GIVE GEMINI FOR GETTING RESPONSE
    """Prepare The Input Prompt With Improved Structure And Validation."""
    if not resume_text or not job_description:
        raise ValueError("Resume Text And Job Description Cannot Be Empty.")
    
    prompt_template = """
    Act as an Expert ATS (Application Trcking System) specialist with deep experties in: 
    - Technical Fields
    - Software Engineering
    - Data Science 
    - Data Analysis 
    - Big Data Engineering

    Evaluate the following resume against the job description. Consider that the job market 
    is highly competitive. Provide detailed feedbacks for resume improvement.

    Resume:   
    {resume_text}

    Job Description:
    {job_description}

     Provide a response in the following JSON format ONLY:
    {{
        "JD Match": "percentage between 0-100",
        "MissingKeywords": ["keyword1", "keyword2", ...],
        "Profile Summary": "detailed analysis of the match and specific improvement suggestions"
    }}
    """
    
    return prompt_template.format(
        resume_text=resume_text.strip(),
        job_description=job_description.strip()
    )










# import google.generativeai as genai

# Configure your API key
# genai.configure(api_key="YOUR_API_KEY") 

# List all available models
# for m in genai.list_models():
#     # Filter for models that support specific methods, if needed
#     # For example, to list models supporting 'generateContent':
#     # if "generateContent" in m.supported_generation_methods:
#     print(f"Model Name: {m.name}, Supported Methods: {m.supported_generation_methods}")
