import requests

class WhatsAppService:

    __BASE_URL = "https://api.telinfy.net/gagp/whatsapp/templates/message"
    __API_KEY = "6ebb7675-df3f-44ac-a545-8829289f8513"
    def __init__(self):

        self.api_key = self.__API_KEY
        self.base_url = self.__BASE_URL
    
    def send_message(self, phone_number, template_name, language='en', 
                     var1='20', var2='50', var3='20', var4='50', 
                     var5='20', var6='50', var7='20'):
        
        """
        Send a WhatsApp template message
        
        :param phone_number: Recipient's phone number with country code
        :param template_name: Name of the WhatsApp message template
        :param language: Language of the template (default: 'en')
        :param var1-var7: Text parameters for the template message
        :return: API response
        """
        # Prepare the headers
        headers = {
            'Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        # Prepare the payload
        payload = {
            "to": phone_number,
            "templateName": template_name,
            "language": language,
            "header": None,
            "body": {
                "parameters": [
                    {"type": "text", "text": var1},
                    {"type": "text", "text": var2},
                    {"type": "text", "text": var3},
                    {"type": "text", "text": var4},
                    {"type": "text", "text": var5},
                    {"type": "text", "text": var6},
                    {"type": "text", "text": var7}
                ]
            },
            "button": None
        }
        
        # Send the API request
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.RequestException as e:
            print(f"Error sending WhatsApp message: {e}")
            return None