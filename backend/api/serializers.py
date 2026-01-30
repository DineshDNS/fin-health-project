from rest_framework import serializers
from .models import GSTRecord, BankStatement

class GSTRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GSTRecord
        fields = "__all__"


class BankStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankStatement
        fields = "__all__"
