from datetime import date
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from backend.app.models import Agent, BlogPost, Property, PropertyImage, Testimonial


def attach_public_image(instance, field_name, public_path):
    """Copy a file from /public into the model's ImageField."""
    if not public_path:
        return
    rel = public_path.lstrip('/')
    src = Path(settings.BASE_DIR).parent / 'frontend' / 'public' / rel
    if not src.exists():
        # Fallback if seed is run without the monorepo frontend folder
        src = Path(settings.BASE_DIR) / 'public' / rel
    if not src.exists():
        return
    with src.open('rb') as handle:
        getattr(instance, field_name).save(src.name, File(handle), save=False)


AGENTS = [
    {
        'id': 1,
        'name': 'John Mensah',
        'phone': '+233 50 123 4567',
        'email': 'john@propertyfinds.com',
        'image': '/agents/agent-1.png',
        'properties_count': 45,
        'rating': Decimal('4.8'),
        'bio': 'Experienced real estate agent with 10+ years in the industry specializing in luxury properties.',
    },
    {
        'id': 2,
        'name': 'Sarah Agyeman',
        'phone': '+233 55 987 6543',
        'email': 'sarah@propertyfinds.com',
        'image': '/agents/agent-2.png',
        'properties_count': 38,
        'rating': Decimal('4.7'),
        'bio': 'Dedicated agent focusing on residential properties and helping families find their dream homes.',
    },
    {
        'id': 3,
        'name': 'Michael Boateng',
        'phone': '+233 24 456 7890',
        'email': 'michael@propertyfinds.com',
        'image': '/agents/agent-3.png',
        'properties_count': 52,
        'rating': Decimal('4.9'),
        'bio': 'Commercial real estate specialist with expertise in business properties and investments.',
    },
]

PROPERTIES = [
    {
        'id': 1,
        'title': 'Luxury Modern House with Pool',
        'description': 'Beautiful 4-bedroom modern house with swimming pool, garden, and parking space.',
        'type': 'house',
        'price': 850000,
        'location': 'East Legon, Accra',
        'city': 'Accra',
        'bedrooms': 4,
        'bathrooms': 3,
        'area': 450,
        'image': '/properties/house-luxury.png',
        'images': ['/properties/house-luxury.png', '/properties/house-luxury-2.png', '/properties/villa-elegant.png'],
        'featured': True,
        'agent_id': 1,
        'posted_date': date(2024, 6, 15),
        'for_sale': True,
        'for_rent': False,
        'features': ['Swimming Pool', 'Garden', 'Parking', 'Modern Design', 'Home Theater'],
    },
    {
        'id': 2,
        'title': 'Spacious 3-Bedroom Apartment',
        'description': 'Modern apartment in the heart of the city with excellent amenities.',
        'type': 'apartment',
        'price': 450000,
        'location': 'Osu, Accra',
        'city': 'Accra',
        'bedrooms': 3,
        'bathrooms': 2,
        'area': 200,
        'image': '/properties/apartment-modern.png',
        'images': ['/properties/apartment-modern.png', '/properties/apartment-cozy.png', '/properties/apartment-studio.png'],
        'featured': True,
        'agent_id': 2,
        'posted_date': date(2024, 6, 10),
        'for_sale': True,
        'for_rent': True,
        'rent_price': 5000,
        'features': ['Elevator', 'Security', '24/7 Power', 'Gym', 'Swimming Pool'],
    },
    {
        'id': 3,
        'title': 'Prime Commercial Space',
        'description': 'High-traffic commercial property perfect for retail or office use.',
        'type': 'commercial',
        'price': 1200000,
        'location': 'Dzorwulu, Accra',
        'city': 'Accra',
        'area': 600,
        'image': '/properties/commercial-prime.png',
        'images': ['/properties/commercial-prime.png', '/properties/retail-shop.png', '/properties/office-executive.png'],
        'featured': True,
        'agent_id': 3,
        'posted_date': date(2024, 6, 12),
        'for_sale': True,
        'for_rent': True,
        'rent_price': 15000,
        'features': ['Parking Lot', 'Visible Signage', 'High Foot Traffic', 'Modern Facilities'],
    },
    {
        'id': 4,
        'title': 'Residential Land Plot',
        'description': 'Prime residential land in a developing area with excellent potential.',
        'type': 'land',
        'price': 180000,
        'location': 'East Legon Hills, Accra',
        'city': 'Accra',
        'area': 1000,
        'image': '/properties/land-residential.png',
        'images': ['/properties/land-residential.png', '/properties/villa-elegant.png', '/properties/house-luxury.png'],
        'featured': False,
        'agent_id': 1,
        'posted_date': date(2024, 6, 8),
        'for_sale': True,
        'for_rent': False,
        'features': ['Good Road Access', 'Flat Terrain', 'Good Neighbors', 'Developed Area'],
    },
    {
        'id': 5,
        'title': 'Cozy 2-Bedroom Apartment',
        'description': 'Affordable and comfortable apartment close to schools and shopping.',
        'type': 'apartment',
        'price': 280000,
        'location': 'Tema, Greater Accra',
        'city': 'Tema',
        'bedrooms': 2,
        'bathrooms': 1,
        'area': 120,
        'image': '/properties/apartment-cozy.png',
        'images': ['/properties/apartment-cozy.png', '/properties/apartment-modern.png', '/properties/apartment-studio.png'],
        'featured': False,
        'agent_id': 2,
        'posted_date': date(2024, 6, 14),
        'for_sale': True,
        'for_rent': True,
        'rent_price': 3000,
        'features': ['Close to Schools', 'Shopping Mall Nearby', 'Quiet Neighborhood'],
    },
    {
        'id': 6,
        'title': 'Executive Office Suite',
        'description': 'Premium office space in a prestigious business district.',
        'type': 'office',
        'price': 2000000,
        'location': 'Airport Area, Accra',
        'city': 'Accra',
        'area': 800,
        'image': '/properties/office-executive.png',
        'images': ['/properties/office-executive.png', '/properties/commercial-prime.png', '/properties/retail-shop.png'],
        'featured': True,
        'agent_id': 3,
        'posted_date': date(2024, 6, 13),
        'for_sale': False,
        'for_rent': True,
        'rent_price': 25000,
        'features': ['Conference Room', 'Furnished', 'Parking', 'WiFi Ready', 'Security'],
    },
    {
        'id': 7,
        'title': 'Industrial Warehouse',
        'description': 'Large warehouse space suitable for storage and light manufacturing.',
        'type': 'warehouse',
        'price': 3500000,
        'location': 'Industrial Zone, Tema',
        'city': 'Tema',
        'area': 2500,
        'image': '/properties/warehouse-industrial.png',
        'images': ['/properties/warehouse-industrial.png', '/properties/commercial-prime.png', '/properties/office-executive.png'],
        'featured': False,
        'agent_id': 1,
        'posted_date': date(2024, 6, 11),
        'for_sale': True,
        'for_rent': True,
        'rent_price': 40000,
        'features': ['High Ceiling', 'Loading Dock', 'Security Fence', 'Office Area'],
    },
    {
        'id': 8,
        'title': 'Elegant 5-Bedroom Villa',
        'description': 'Luxurious villa with stunning views, infinity pool, and modern amenities.',
        'type': 'house',
        'price': 1500000,
        'location': 'Ridge Area, Accra',
        'city': 'Accra',
        'bedrooms': 5,
        'bathrooms': 4,
        'area': 650,
        'image': '/properties/villa-elegant.png',
        'images': ['/properties/villa-elegant.png', '/properties/house-luxury.png', '/properties/house-luxury-2.png'],
        'featured': True,
        'agent_id': 2,
        'posted_date': date(2024, 6, 9),
        'for_sale': True,
        'for_rent': False,
        'features': ['Infinity Pool', 'Garden', 'Home Automation', 'Security System', 'Guest House'],
    },
    {
        'id': 9,
        'title': 'Studio Apartment - Perfect for Students',
        'description': 'Affordable studio apartment close to universities and transportation.',
        'type': 'apartment',
        'price': 150000,
        'location': 'Legon, Accra',
        'city': 'Accra',
        'bedrooms': 1,
        'bathrooms': 1,
        'area': 60,
        'image': '/properties/apartment-studio.png',
        'images': ['/properties/apartment-studio.png', '/properties/apartment-cozy.png', '/properties/apartment-modern.png'],
        'featured': False,
        'agent_id': 3,
        'posted_date': date(2024, 6, 16),
        'for_sale': True,
        'for_rent': True,
        'rent_price': 1500,
        'features': ['University Nearby', 'WiFi', 'Furnished', 'Secure Gate'],
    },
    {
        'id': 10,
        'title': 'Retail Shop Front',
        'description': 'Prime retail location with high visibility and foot traffic.',
        'type': 'commercial',
        'price': 500000,
        'location': 'Makola Market, Accra',
        'city': 'Accra',
        'area': 150,
        'image': '/properties/retail-shop.png',
        'images': ['/properties/retail-shop.png', '/properties/commercial-prime.png', '/properties/office-executive.png'],
        'featured': False,
        'agent_id': 1,
        'posted_date': date(2024, 6, 7),
        'for_sale': True,
        'for_rent': True,
        'rent_price': 8000,
        'features': ['Market Location', 'High Traffic', 'Display Windows', 'Stockroom'],
    },
    {
        'id': 11,
        'title': 'Toyota Camry 2022',
        'description': 'Well-maintained Toyota Camry with low mileage, leather interior, and full service history.',
        'type': 'car',
        'price': 185000,
        'location': 'East Legon, Accra',
        'city': 'Accra',
        'area': 0,
        'image': '/properties/car-camry-1.jpg',
        'images': ['/properties/car-camry-1.jpg', '/properties/car-camry-2.jpg', '/properties/car-camry-3.jpg'],
        'featured': True,
        'agent_id': 1,
        'posted_date': date(2024, 6, 10),
        'for_sale': True,
        'for_rent': False,
        'features': ['Automatic', 'Leather Seats', 'Reverse Camera', 'Fuel Efficient'],
    },
    {
        'id': 12,
        'title': 'Honda CR-V 2021',
        'description': 'Spacious SUV ideal for family use, with excellent road condition and updated features.',
        'type': 'car',
        'price': 220000,
        'location': 'Airport Residential, Accra',
        'city': 'Accra',
        'area': 0,
        'image': '/properties/car-crv-1.jpg',
        'images': ['/properties/car-crv-1.jpg', '/properties/car-crv-2.jpg', '/properties/car-crv-3.jpg'],
        'featured': True,
        'agent_id': 2,
        'posted_date': date(2024, 6, 12),
        'for_sale': True,
        'for_rent': True,
        'rent_price': 3500,
        'features': ['SUV', 'AWD', 'Bluetooth', 'Sunroof'],
    },
    {
        'id': 13,
        'title': 'Hyundai Elantra 2020',
        'description': 'Reliable sedan with great fuel economy, ideal for city commuting.',
        'type': 'car',
        'price': 95000,
        'location': 'Tema Community 25',
        'city': 'Tema',
        'area': 0,
        'image': '/properties/car-elantra-1.jpg',
        'images': ['/properties/car-elantra-1.jpg', '/properties/car-elantra-2.jpg', '/properties/car-elantra-3.jpg'],
        'featured': False,
        'agent_id': 3,
        'posted_date': date(2024, 6, 8),
        'for_sale': True,
        'for_rent': False,
        'features': ['Manual', 'Air Conditioning', 'USB Ports', 'Clean Title'],
    },
]

BLOG_POSTS = [
    {
        'id': 1,
        'title': 'Top 5 Tips for First-Time Home Buyers in Ghana',
        'excerpt': 'Learn essential strategies to make your first property purchase a success.',
        'content': 'Buying your first home is a major decision. Here are the top tips to guide you through the process...',
        'image': '/blog/blog-1.png',
        'date': date(2024, 6, 20),
        'author': 'John Mensah',
        'category': 'Buying Guide',
    },
    {
        'id': 2,
        'title': 'Understanding Property Values in Accra',
        'excerpt': 'Discover what factors influence real estate prices in the capital city.',
        'content': 'Property values in Accra are influenced by multiple factors including location, amenities...',
        'image': '/blog/blog-2.png',
        'date': date(2024, 6, 18),
        'author': 'Michael Boateng',
        'category': 'Market Analysis',
    },
    {
        'id': 3,
        'title': 'Investment Opportunities in Emerging Areas',
        'excerpt': 'Explore high-potential areas for real estate investment.',
        'content': 'Several emerging areas in Greater Accra show strong investment potential...',
        'image': '/blog/blog-3.png',
        'date': date(2024, 6, 15),
        'author': 'Sarah Agyeman',
        'category': 'Investment',
    },
]

TESTIMONIALS = [
    {
        'id': 1,
        'name': 'Akosua Baah',
        'role': 'Property Buyer',
        'content': 'Mydas Plus made finding my dream home incredibly easy. The AI search feature saved me so much time!',
        'image': '/testimonials/testimonial-1.png',
        'rating': 5,
    },
    {
        'id': 2,
        'name': 'Kwame Asante',
        'role': 'Business Owner',
        'content': 'Found the perfect commercial space for my business. The team was professional and helpful throughout.',
        'image': '/testimonials/testimonial-2.png',
        'rating': 5,
    },
    {
        'id': 3,
        'name': 'Ama Osei',
        'role': 'Investment Consultant',
        'content': 'Excellent platform for property investment. The price estimation tools are incredibly accurate.',
        'image': '/testimonials/testimonial-3.png',
        'rating': 4,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample property listing data'

    def handle(self, *args, **options):
        Property.objects.all().delete()
        BlogPost.objects.all().delete()
        Testimonial.objects.all().delete()
        Agent.objects.all().delete()

        for agent_data in AGENTS:
            payload = {**agent_data}
            image_path = payload.pop('image', '')
            agent = Agent(**payload)
            attach_public_image(agent, 'image', image_path)
            agent.save()

        for prop_data in PROPERTIES:
            payload = {**prop_data}
            image_path = payload.pop('image', '')
            gallery_paths = payload.pop('images', [])
            prop = Property(**payload)
            attach_public_image(prop, 'image', image_path)
            prop.save()

            for index, gallery_path in enumerate(gallery_paths):
                # Skip duplicate of main photo
                if gallery_path == image_path:
                    continue
                gallery = PropertyImage(property=prop, sort_order=index)
                attach_public_image(gallery, 'image', gallery_path)
                gallery.save()

        for post_data in BLOG_POSTS:
            payload = {**post_data}
            image_path = payload.pop('image', '')
            post = BlogPost(**payload)
            attach_public_image(post, 'image', image_path)
            post.save()

        for item_data in TESTIMONIALS:
            payload = {**item_data}
            image_path = payload.pop('image', '')
            item = Testimonial(**payload)
            attach_public_image(item, 'image', image_path)
            item.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Seeded {Agent.objects.count()} agents, '
                f'{Property.objects.count()} properties, '
                f'{PropertyImage.objects.count()} gallery photos, '
                f'{BlogPost.objects.count()} blog posts, '
                f'{Testimonial.objects.count()} testimonials.'
            )
        )
