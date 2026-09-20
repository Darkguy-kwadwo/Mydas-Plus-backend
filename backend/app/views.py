from rest_framework import filters, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from .models import Agent, BlogPost, Property, Testimonial
from .permissions import IsStaffOrReadOnly
from .serializers import (
    AgentSerializer,
    BlogPostSerializer,
    PropertySerializer,
    TestimonialSerializer,
)

PROPERTY_CATEGORIES = [
    {'id': 'house', 'name': 'Houses', 'icon': '🏠'},
    {'id': 'apartment', 'name': 'Apartments', 'icon': '🏢'},
    {'id': 'land', 'name': 'Lands', 'icon': '🌳'},
    {'id': 'commercial', 'name': 'Commercial', 'icon': '🏬'},
    {'id': 'office', 'name': 'Offices', 'icon': '💼'},
    {'id': 'warehouse', 'name': 'Warehouses', 'icon': '📦'},
    {'id': 'car', 'name': 'Cars', 'icon': '🚗'},
]

CITIES = ['Accra', 'Tema', 'Kumasi', 'Sekondi-Takoradi', 'Cape Coast']


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [IsStaffOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location', 'city', 'type']
    ordering_fields = ['price', 'posted_date', 'area']

    def get_queryset(self):
        qs = Property.objects.select_related('agent').prefetch_related('gallery_images').all()
        params = self.request.query_params

        property_type = params.get('type')
        if property_type:
            qs = qs.filter(type=property_type)

        city = params.get('city')
        if city:
            qs = qs.filter(city__iexact=city)

        featured = params.get('featured')
        if featured is not None:
            qs = qs.filter(featured=featured.lower() in ('1', 'true', 'yes'))

        agent_id = params.get('agentId') or params.get('agent')
        if agent_id:
            qs = qs.filter(agent_id=agent_id)

        for_sale = params.get('forSale')
        if for_sale is not None:
            qs = qs.filter(for_sale=for_sale.lower() in ('1', 'true', 'yes'))

        for_rent = params.get('forRent')
        if for_rent is not None:
            qs = qs.filter(for_rent=for_rent.lower() in ('1', 'true', 'yes'))

        min_price = params.get('minPrice')
        if min_price:
            qs = qs.filter(price__gte=min_price)

        max_price = params.get('maxPrice')
        if max_price:
            qs = qs.filter(price__lte=max_price)

        bedrooms = params.get('bedrooms')
        if bedrooms:
            qs = qs.filter(bedrooms__gte=bedrooms)

        return qs


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsStaffOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsStaffOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'excerpt', 'content', 'category', 'author']


class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsStaffOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


@api_view(['GET'])
def meta_view(request):
    return Response(
        {
            'cities': CITIES,
            'propertyCategories': PROPERTY_CATEGORIES,
        }
    )


@api_view(['GET'])
def comparable_properties(request, pk):
    try:
        property_obj = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)

    comps = (
        Property.objects.select_related('agent')
        .prefetch_related('gallery_images')
        .filter(type=property_obj.type)
        .exclude(pk=pk)[:3]
    )
    return Response(PropertySerializer(comps, many=True, context={'request': request}).data)
