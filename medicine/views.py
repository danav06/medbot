from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import base64
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def index(request):
    html = render_to_string('medicine/index.html')
    return HttpResponse(html, content_type='text/html')

@csrf_exempt
def analyze_medicine(request):
    if request.method == 'POST':
        try:
            image_file = request.FILES.get('image')
            user_question = request.POST.get('question', '')

            if not image_file:
                return JsonResponse({'error': 'No image provided'}, status=400)

            image_bytes = image_file.read()
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            mime_type = image_file.content_type or 'image/jpeg'
            language = request.POST.get('language', 'english')

            if language == 'urdu':
                prompt = f"""
                Analyze this medicine image. Provide the response in TWO parts:

                PART 1 - Write in Urdu script (for display on screen):
                [URDU_START]
                1. دوائی کا نام اور برانڈ
                2. اجزاء / ترکیب
                3. یہ دوائی کس لیے استعمال ہوتی ہے
                4. تجویز کردہ خوراک
                5. ضمنی اثرات
                6. احتیاطی تدابیر
                7. دوسری دواؤں کے ساتھ تعامل
                8. ڈاکٹر سے کب ملیں
                [URDU_END]

                PART 2 - Write EXACT SAME information in Roman Urdu using English alphabet only (for text to speech). Do NOT use any Urdu script in this part. Write everything like this example:
                [ROMAN_START]
                Dawai ka naam Paracetamol hai. Yeh 500mg ki tablet hai. Yeh dard aur bukhar ke liye istemal hoti hai. Rozana 3 baar lein. Khaane ke baad lein. Bachon ko mat dein. Doctor se mashwara zaroor karein.
                [ROMAN_END]

                {f"User also asked: {user_question}" if user_question else ""}
                """
            else:
                prompt = f"""
                You are a professional medical assistant AI. Analyze this medicine image and provide:
                1. Medicine Name and Brand
                2. Active Ingredients / Composition
                3. What this medicine is used for
                4. Recommended Dosage
                5. Side Effects
                6. Warnings and Precautions
                7. Drug Interactions
                8. When to see a doctor
                {f"User also asked: {user_question}" if user_question else ""}
                Always end with: Disclaimer: This information is for educational purposes only. Always consult a licensed doctor before taking any medicine.
                """

            response = client.chat.completions.create(
                model='meta-llama/llama-4-scout-17b-16e-instruct',
                messages=[
                    {
                        'role': 'user',
                        'content': [
                            {
                                'type': 'image_url',
                                'image_url': {
                                    'url': f'data:{mime_type};base64,{base64_image}'
                                }
                            },
                            {
                                'type': 'text',
                                'text': prompt
                            }
                        ]
                    }
                ],
                max_tokens=2000
            )

            full_response = response.choices[0].message.content

            if language == 'urdu':
                try:
                    urdu_text = full_response.split('[URDU_START]')[1].split('[URDU_END]')[0].strip()
                except:
                    urdu_text = full_response

                try:
                    roman_text = full_response.split('[ROMAN_START]')[1].split('[ROMAN_END]')[0].strip()
                except:
                    roman_text = urdu_text

                return JsonResponse({
                    'success': True,
                    'analysis': urdu_text,
                    'speech_text': roman_text
                })
            else:
                return JsonResponse({
                    'success': True,
                    'analysis': full_response,
                    'speech_text': full_response
                })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)