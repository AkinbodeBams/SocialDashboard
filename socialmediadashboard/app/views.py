
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SocialDashboardData
from .helper import SocialDashboardHelper
from .serializer import SocialDashboardDataSerializer
from datetime import datetime,timedelta
from django.utils import timezone
from django.db.models import  Q
from rest_framework import status
from rest_framework_api_key.permissions import HasAPIKey
import asyncio


class SocialMediaDashBoardProfile(APIView):
    """Requires an  Api-Key Header Authorization upon each call
        -Checks if an object exists or the last time a keyword was called  is more than X hours,
        -if not, calls the helper function 
            *SocialDashboardHelper().save_data(i) where i == keyword
            *takes approximately 10secs per new {param = keyword}
        -if object exists:
            * the following filters can be used:
                 ['network','language','sentiment','from_date','to_date' , 'keyword']
            """
    permission_classes = [HasAPIKey]
    def get(self,request,*args,**kwargs):
        keywords = request.GET.getlist('keyword')
        social_network_filter = request.query_params.get('network',None)
        language_filter=request.query_params.get('language',None)
        sentiment_filter=request.query_params.get('sentiment',None)
        from_date=request.query_params.get('from_date',None)
        to_date=request.query_params.get('to_date',None)
        all_params = ['network','language','sentiment','from_date','to_date' , 'keyword']
        all_keywords = SocialDashboardData.objects.all()
        filtering = SocialDashboardData.objects.filter(keyword__in=[i for i in keywords])
        distinct_rows =SocialDashboardData.objects.all().values_list('keyword', flat=True).distinct()

        if not keywords:
            return Response({"status":False,"Message":"You Need To Enter At least A Keyword"},
            status=status.HTTP_400_BAD_REQUEST)

        for i in all_params:
            for j in request.query_params:
                if j not in all_params:
                    return Response({"status":False, "message":f"Invalid Parameter {j} Entered"},status= status.HTTP_400_BAD_REQUEST)

        if all_keywords.exists():
            if from_date and to_date:
                filtering = filtering.filter(date_posted__range=(from_date, to_date))
            if social_network_filter:
                filtering=filtering.filter(network=social_network_filter)
            if language_filter:
                filtering=filtering.filter(language=language_filter)
            if sentiment_filter:
                filtering=filtering.filter(sentiment=sentiment_filter)
            
            distinct_rows =SocialDashboardData.objects.all().values_list('keyword', flat=True).distinct()
            caller = []
            for i in keywords:
                if i not in distinct_rows or ( (datetime.now(timezone.utc)) - (SocialDashboardData.objects.filter(keyword=i).last().modified_at)) > timedelta(hours=44) :
                    caller.append(i)
            if len(caller)>0:
                for i in caller:
                    SocialDashboardHelper().save_data(i)

            serializer = SocialDashboardDataSerializer(filtering,many=True)
            return Response({"MetaData":[{"Count":len(serializer.data),
                                "keywords":list(dict.fromkeys([i['keyword'] for i in serializer.data])),
                                "network_list":list(dict.fromkeys([i['network'] for i in serializer.data])),
                                "language_list":list(dict.fromkeys([i['language'] for i in serializer.data]))}],
                                "Data":serializer.data})        
        else:
           for key in keywords:
            SocialDashboardHelper().save_data(key)
        serializer = SocialDashboardDataSerializer(filtering,many=True)
        
        return Response({"MetaData":[{"Count":len(serializer.data),"network_list":list(dict.fromkeys([i['network'] for i in serializer.data])),
                                            "language_list":list(dict.fromkeys([i['language'] for i in serializer.data]))}],
                                            "Data":serializer.data})