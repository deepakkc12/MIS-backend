from datetime import datetime
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from ..utils.response import ResponseHandler
from ..services.Whatsapp import WhatsAppService
from ..utils.decorators import token_required

class SendWhatsappMessage(APIView):
    def post(self,request):
        whatsapp_client = WhatsAppService()

        result = whatsapp_client.send_message(template_name='restaurant_day_summery',phone_number="+919947540498")

        if result:
            return ResponseHandler.success(data=result)
        
        return ResponseHandler.internal_server_error("Something went wrong")
