# generator/views.py
from django.shortcuts import render
from django.conf import settings
import requests
import base64
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm # ADD THIS
# from django.urls import reverse_lazy # ADD THIS
# from django.views import generic # ADD THIS

# @login_required
def home_view(request):
    image_data = None # This will hold the image data to send to the template
    prompt_text = ""

    if request.method == 'POST':
        prompt_text = request.POST.get('prompt')
        
        # --- API Call Logic ---
        api_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.STABILITY_API_KEY}",
        }

        payload = {
            "text_prompts": [{"text": prompt_text}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        }

        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            base64_string = response_data["artifacts"][0]["base64"]
            
            # Format the base64 string so it can be used in an HTML img tag
            image_data = f"data:image/png;base64,{base64_string}"
        else:
            print(f"Error: {response.status_code} - {response.text}")

    context = {
        'image_data': image_data,
        'prompt_text': prompt_text,
    }
    return render(request, 'generator/index.html', context)

# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'
