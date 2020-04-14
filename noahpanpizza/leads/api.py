from leads.models import Lead
from rest_framework import viewsets, permissions
from .serializers import LeadSerializer

#Lead Viewset 
#Lets us create a full CRD(Create Read and Delete) API without defining methods. 

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    permission_classes= [
        permissions.AllowAny
    ]
    serializer_class = LeadSerializer