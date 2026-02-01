from rest_framework import serializers
from .models import FinancialDocument


class FinancialDocumentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = FinancialDocument
        fields = "__all__"

    def get_file_name(self, obj):
        if obj.file:
            return obj.file.name.split("/")[-1]
        return ""
