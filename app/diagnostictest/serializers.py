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
# For this we would need to add custom logic but overriding the create and update diagnostic test method.

# This method will take the tags as input and either get the tag if it already exists or create one if it diesnt exist
    def _get_or_create_tags(self, tags, diagnostictest):
        """Handle getting or creating tags as needed."""
        # We first get the user
        auth_user = self.context['request'].user
        # For each tag included, we call a helper method thats available in the model manager which
        # gets the tag if it already exists and if not it creates a tag.
        # Then we add the tag to the diagnostictest.
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            diagnostictest.tags.add(tag_obj)

# We override the create method so that we can also incude tags along with creating a diagnostictest
    def create(self, validated_data):
        """Create a diagnostictest."""
# We first remove the tags from the request and store it in the tags variable
# This is because we cant pass tags to the create method of diagnostic test as it only expects fields
# and expects that tags will be assigned as a related field
        tags = validated_data.pop('tags', [])
# We then create the diagnostictest
        diagnostictest = DiagnosticTest.objects.create(**validated_data)
# We then call the method to get ot create tags.
        self._get_or_create_tags(tags, diagnostictest)
# return the diagnostictest
        return diagnostictest

# We override the update method so that we can also incude tags along with creating a diagnostictest
    def update(self, instance, validated_data):
        """Update diagnostictest."""
        # We remove the tags from the update request validated data and store it in the tags variable
        tags = validated_data.pop('tags', None)
# If the tags list contains something, then it clears the existing tags
# One thing to note here is that None is not the same as an empty list.
# So if an empty list was passed, it would enter this method and then would clear the existing tags
# And then it calls the method which creates or gets the tags.
# If its an empty list then no tags are created or retrieved
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
# Here we take the rest of the validated data and assign it to the instance.
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
