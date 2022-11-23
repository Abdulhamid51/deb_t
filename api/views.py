from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            key = Token.objects.get(user=user)
            return Response({"key":key.__str__()})
        else:
            return Response({"error":"username or password incorrect"})

class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.create_user(username=username, password=password)
        key = Token.objects.create(user=user)
        return Response({"key":key.__str__()})


class ClientsList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query_set = Client.objects.filter(owner=request.user)
        serializer = ClientSerializer(query_set, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data.update({"owner":request.user.id})
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error":"data is not valid"})


class ClientDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        client = Client.objects.get(id=id)
        query_set = Debt.objects.filter(client=client.id)
        serializer = DebtSerializer(query_set, many=True)
        return Response({
            "name":client.name,
            "debt_mount":client.debt_mount,
            "debt_history":serializer.data
            })


class ClientUpdateDelete(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, id):
        client = Client.objects.get(id=id)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error":"data is not valid"})

    def delete(self, request, id):
        client = Client.objects.get(id=id)
        client.delete()
        return Response({"success":"deleted"})


class DebtCreateUpdateDelete(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        client_id = request.data['client']
        mount = request.data['mount']
        client = Client.objects.get(id=client_id)
        client.debt_mount += mount
        serializer = DebtSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            client.save()
            return Response(serializer.data)
        else:
            return Response({"error":"data is not valid"})
    
    def put(self, request, id):
        debt = Debt.objects.get(id=id)
        client_id = request.data['client']
        client = Client.objects.get(id=client_id)
        client.debt_mount -= debt.mount
        client.save()
        client.debt_mount += request.data['mount']
        serializer = DebtSerializer(debt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            client.save()
            return Response(serializer.data)
        else:
            return Response({"error":"data is not valid"})

    def delete(self, request, id):
        debt = Debt.objects.get(id=id)
        client = Client.objects.get(id=debt.client.id)
        client.debt_mount -= debt.mount
        client.save()
        debt.delete()
        return Response({"success":"deleted"})


class BaseInformations(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        loans = 0.0
        debts = 0.0
        alls = 0.0
        clients = Client.objects.filter(owner=request.user)
        for num in clients:
            if str(num.debt_mount)[0] == '-':
                debts += num.debt_mount
            else:
                loans += num.debt_mount
            alls += num.debt_mount
        return Response({
            "haqlar":loans,
            "qarzlar":debts,
            "holat":alls
        })


class Search(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query = request.GET.get("query")
        client = Client.objects.filter(name__icontains=query)
        serializer = ClientSerializer(client, many=True)
        return Response(serializer.data)

import csv
from django.http import HttpResponse

def getfile(request): 
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="file.csv"'  
    client = Client.objects.filter(owner=request.user)  
    writer = csv.writer(response)  
    for client in client:  
        writer.writerow([client.id, client.name, client.debt_mount])  
    return response  