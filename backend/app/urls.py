from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .auth_views import admin_stats_view, login_view, me_view
from .views import (
    AgentViewSet,
    BlogPostViewSet,
    PropertyViewSet,
    TestimonialViewSet,
    comparable_properties,
    meta_view,
)

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'agents', AgentViewSet, basename='agent')
router.register(r'blog-posts', BlogPostViewSet, basename='blog-post')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')

urlpatterns = [
    path('auth/login/', login_view, name='auth-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('auth/me/', me_view, name='auth-me'),
    path('admin/stats/', admin_stats_view, name='admin-stats'),
    path('meta/', meta_view, name='meta'),
    path('properties/<int:pk>/comparables/', comparable_properties, name='property-comparables'),
    path('', include(router.urls)),
]
