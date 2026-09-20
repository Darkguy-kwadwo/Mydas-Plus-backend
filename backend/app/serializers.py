from rest_framework import serializers

from .models import Agent, BlogPost, Property, PropertyImage, Testimonial


def image_url(field, serializer):
    """Return an absolute media URL so a separately hosted frontend can load images."""
    if not field:
        return ''
    try:
        url = field.url
    except ValueError:
        return ''
    request = serializer.context.get('request')
    if request is not None:
        return request.build_absolute_uri(url)
    return url


def parse_bool(value):
    if isinstance(value, bool):
        return value
    if value is None or value == '':
        return False
    return str(value).lower() in ('1', 'true', 'yes', 'on')


class AgentSerializer(serializers.ModelSerializer):
    properties = serializers.IntegerField(source='properties_count', required=False)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Agent
        fields = [
            'id',
            'name',
            'phone',
            'email',
            'image',
            'properties',
            'rating',
            'bio',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['image'] = image_url(instance.image, self)
        data['rating'] = float(instance.rating)
        data['properties'] = instance.properties_count
        return data


class PropertySerializer(serializers.ModelSerializer):
    agentId = serializers.PrimaryKeyRelatedField(
        source='agent',
        queryset=Agent.objects.all(),
        required=False,
        allow_null=True,
    )
    postedDate = serializers.DateField(source='posted_date')
    forSale = serializers.BooleanField(source='for_sale', required=False)
    forRent = serializers.BooleanField(source='for_rent', required=False)
    rentPrice = serializers.IntegerField(source='rent_price', required=False, allow_null=True)
    image = serializers.ImageField(required=False, allow_null=True)
    images = serializers.SerializerMethodField(read_only=True)
    gallery = serializers.SerializerMethodField(read_only=True)
    features = serializers.JSONField(required=False)

    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'description',
            'type',
            'price',
            'location',
            'city',
            'bedrooms',
            'bathrooms',
            'area',
            'image',
            'images',
            'gallery',
            'featured',
            'agentId',
            'postedDate',
            'forSale',
            'forRent',
            'rentPrice',
            'features',
        ]

    def get_images(self, obj):
        return [item['url'] for item in self.get_gallery(obj)]

    def get_gallery(self, obj):
        items = []
        main = image_url(obj.image, self)
        if main:
            items.append({'id': f'main-{obj.pk}', 'url': main, 'isMain': True})
        for photo in obj.gallery_images.all():
            url = image_url(photo.image, self)
            if url:
                items.append({'id': str(photo.pk), 'url': url, 'isMain': False})
        return items

    def to_internal_value(self, data):
        # QueryDict cannot store real lists — convert to a plain dict first.
        if hasattr(data, 'lists'):
            mutable = {key: data.get(key) for key in data.keys()}
        else:
            mutable = dict(data)

        for key in ('featured', 'forSale', 'forRent'):
            if key in mutable:
                mutable[key] = parse_bool(mutable.get(key))

        if 'features' in mutable:
            import json

            raw = mutable.get('features')
            if isinstance(raw, list):
                mutable['features'] = raw
            elif raw in (None, ''):
                mutable['features'] = []
            elif isinstance(raw, str):
                try:
                    parsed = json.loads(raw)
                    mutable['features'] = parsed if isinstance(parsed, list) else [str(parsed)]
                except json.JSONDecodeError:
                    mutable['features'] = [part.strip() for part in raw.split(',') if part.strip()]
            else:
                mutable['features'] = []

        if 'agentId' in mutable and mutable.get('agentId') in ('', 'null', None):
            mutable['agentId'] = None
        for key in ('bedrooms', 'bathrooms', 'rentPrice', 'area'):
            if key in mutable and mutable.get(key) in ('', None):
                if key == 'area':
                    mutable[key] = 0
                else:
                    mutable.pop(key)
        return super().to_internal_value(mutable)

    def _save_gallery(self, property_obj, files):
        gallery_files = []
        if hasattr(files, 'getlist'):
            gallery_files = files.getlist('gallery') or files.getlist('gallery[]')
        if not gallery_files and files.get('gallery'):
            gallery_files = [files.get('gallery')]

        start = property_obj.gallery_images.count()
        for index, uploaded in enumerate(gallery_files):
            if not uploaded:
                continue
            PropertyImage.objects.create(
                property=property_obj,
                image=uploaded,
                sort_order=start + index,
            )

    def create(self, validated_data):
        property_obj = Property.objects.create(**validated_data)
        request = self.context.get('request')
        if request is not None:
            self._save_gallery(property_obj, request.FILES)
        return property_obj

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        request = self.context.get('request')
        if request is not None:
            self._save_gallery(instance, request.FILES)
            remove_raw = request.data.get('removeGalleryIds') or request.data.get('removeGalleryIds[]')
            if remove_raw:
                import json

                ids = remove_raw
                if isinstance(remove_raw, str):
                    try:
                        ids = json.loads(remove_raw)
                    except json.JSONDecodeError:
                        ids = [part.strip() for part in remove_raw.split(',') if part.strip()]
                if not isinstance(ids, (list, tuple)):
                    ids = [ids]
                clean_ids = [int(i) for i in ids if str(i).isdigit()]
                if clean_ids:
                    instance.gallery_images.filter(id__in=clean_ids).delete()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['image'] = image_url(instance.image, self)
        data['agentId'] = str(instance.agent_id) if instance.agent_id else None
        if data.get('bedrooms') is None:
            data.pop('bedrooms', None)
        if data.get('bathrooms') is None:
            data.pop('bathrooms', None)
        if data.get('rentPrice') is None:
            data.pop('rentPrice', None)
        return data


class BlogPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'excerpt',
            'content',
            'image',
            'date',
            'author',
            'category',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['image'] = image_url(instance.image, self)
        return data


class TestimonialSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'role', 'content', 'image', 'rating']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id)
        data['image'] = image_url(instance.image, self)
        return data
