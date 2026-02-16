from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import openai

def home(request):
    return render(request, 'index.html')

@csrf_exempt
def chat_api(request):
    """Handle chatbot API requests"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Check if API key is configured
        if not settings.OPENAI_API_KEY:
            return JsonResponse({
                'error': 'OpenAI API key not configured',
                'response': 'I apologize, but the AI service is not currently configured. Please contact support.'
            }, status=500)
        
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # System prompt for the chatbot
        system_prompt = """You are a helpful AI assistant for AI Assisted Business OS, a company that provides AI-powered business solutions including chatbots, automation, customer support, sales qualification, and various AI integrations.

Your role is to:
- Answer questions about AI Assisted Business OS services and capabilities
- Help visitors understand how AI can transform their business operations
- Provide information about the catalogue of AI capabilities
- Guide users to relevant solutions based on their needs
- Be friendly, professional, and knowledgeable

Key services include:
- AI Email Automation
- AI Course Creator Platform
- Generative Engine Optimisation (GEO)
- SEO Services
- Omnichannel AI Customer Support
- Voice AI Agents
- AI Sales & Lead Qualification
- Website AI Assistants
- And many more AI-powered solutions

Always be helpful and encourage visitors to explore the catalogue or book a demo if they're interested."""
        
        # Make API call to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        ai_response = response.choices[0].message.content
        
        return JsonResponse({
            'response': ai_response,
            'status': 'success'
        })
        
    except openai.APIError as e:
        return JsonResponse({
            'error': 'OpenAI API error',
            'response': 'I apologize, but I encountered an error processing your request. Please try again.'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'error': 'Internal server error',
            'response': 'I apologize, but something went wrong. Please try again later.'
        }, status=500)