from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Company, Watchlist
from .serializers import CompanySerializer, WatchlistSerializer, RegisterSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# -------------------------------
# 🔐 User Registration
# -------------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------------
# 🏢 Company List with Filtering
# -------------------------------
class CompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Company.objects.all()
        company_name = self.request.query_params.get('company_name')
        symbol = self.request.query_params.get('symbol')

        if company_name:
            queryset = queryset.filter(company_name__icontains=company_name)
        if symbol:
            queryset = queryset.filter(symbol__icontains=symbol)

        return queryset


# -------------------------------
# ⭐ Watchlist Views
# -------------------------------
class WatchlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = Watchlist.objects.filter(user=request.user)
        serializer = WatchlistSerializer(items, many=True)
        return Response(serializer.data)


class AddToWatchlist(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        company_id = request.data.get('company_id')

        if not company_id:
            return Response({'error': 'company_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        company = get_object_or_404(Company, id=company_id)
        watch_item, created = Watchlist.objects.get_or_create(user=request.user, company=company)

        if created:
            return Response({'message': 'Added to watchlist'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Already in watchlist'}, status=status.HTTP_200_OK)


class RemoveFromWatchlist(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        company_id = request.data.get('company_id')

        if not company_id:
            return Response({'error': 'company_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        company = get_object_or_404(Company, id=company_id)
        watch_item = Watchlist.objects.filter(user=request.user, company=company)

        if watch_item.exists():
            watch_item.delete()
            return Response({'message': 'Removed from watchlist'}, status=status.HTTP_200_OK)

        return Response({'error': 'Company not found in your watchlist'}, status=status.HTTP_404_NOT_FOUND)
