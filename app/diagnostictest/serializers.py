"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    DiagnosticTest,
)

# This is similar to the serializers in User App.
# Check the code comments in that file to understand what is happening here.


class DiagnosticTestSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        model = DiagnosticTest
        fields = ['id', 'title', 'time_minutes', 'price', 'link', ]
        read_only_fields = ['id']


# We are using DiagnosticTestSerializer as the detail will be an extension of the DiagnosticTestSerializer
class DiagnosticTestDetailSerializer(DiagnosticTestSerializer):
    """Serializer for recipe detail view."""


# So all the fields in DiagnosticTestSerializer plus the description.
    class Meta(DiagnosticTestSerializer.Meta):
        fields = DiagnosticTestSerializer.Meta.fields + ['description']
