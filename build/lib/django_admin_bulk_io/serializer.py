from rest_framework.serializers import ModelSerializer


class BulkIODynamicSerializer(ModelSerializer):
    class Meta:
        model = None
        fields = "__all__"
