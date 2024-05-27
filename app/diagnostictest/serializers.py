"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    DiagnosticTest,
    Tag,
)

# This is similar to the serializers in User App.
# Check the code comments in that file to understand what is happening here.


# Creating the TagSerializer above DiagnosticTest Serializer as we are going to reference tags in DiagnosticTest
class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class DiagnosticTestSerializer(serializers.ModelSerializer):
    """Serializer for DiagnosticTests."""
    # Add tags to our DiagnosticTests and we are making it optional by setting required to false
    # And we are saying many meaning one DiagnosticTest can have multiple tags.
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = DiagnosticTest
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

# As you can see , DiagnosticTestSerializer has become a nested Serializer as it has the TagSerilaizer within it.
# By default a nested serializer is readonly. This would mean that if we left this as is, then
# a tag would have to be created or updated first before it is assigned to a DiagnosticTest
# If we want to be able to create the tag if it doesnt already exist when adding it to a DiagnosticTest
# For this we would need to add custom logic but overriding the create diagnostic test method.

# COMMENTS FOR THIS CODE *******
    def _get_or_create_tags(self, tags, diagnostictest):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            diagnostictest.tags.add(tag_obj)

# COMMENTS FOR THIS CODE ********

    def create(self, validated_data):
        """Create a diagnostictest."""
        tags = validated_data.pop('tags', [])
        diagnostictest = DiagnosticTest.objects.create(**validated_data)
        self._get_or_create_tags(tags, diagnostictest)

        return diagnostictest

# COMMENTS FOR THIS CODE *********
    def update(self, instance, validated_data):
        """Update diagnostictest."""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# We are using DiagnosticTestSerializer as the detail will be an extension of the DiagnosticTestSerializer
class DiagnosticTestDetailSerializer(DiagnosticTestSerializer):
    """Serializer for recipe detail view."""


# So all the fields in DiagnosticTestSerializer plus the description.
    class Meta(DiagnosticTestSerializer.Meta):
        fields = DiagnosticTestSerializer.Meta.fields + ['description']
