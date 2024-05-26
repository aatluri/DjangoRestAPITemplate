"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Its used for translation. When used it will assist in translation of your page to other languages.
from django.utils.translation import gettext_lazy as _

# imports all the custom models we wrote
from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    # will order the users by ID
    ordering = ['id']
    # Will only display the email address and name of the users in the list display.
    list_display = ['email', 'name']
    # We are customising the fieldsets class variable. Fieldsets are used to control the layout of certain admin pages.
    fieldsets = (
        # Define a tuple with no title ie None, and the fields as email, password
        (None, {'fields': ('email', 'password')}),
        # The _ is for translation as we have defined in the imports above.
        (
            # Permissions and the fields to display in that section.
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        # Another section that has the last_login
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    # this will make the last login field readonly.
    readonly_fields = ['last_login']
    # add fields is used to customise the create user page.
    # we define the fields that are part of user.
    add_fieldsets = (
        (None, {
            # classes is how we can assign custom css classes
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


# Register Models.User.
# So if you were to just type models like user, then it would register the user model, but it wouldn't
# assign the actual custom user model here.
# So what we're going to do is add a comma here and tell it to use user admin, which is our custom user clause.
# So if you don't specify user in this part of is optional.
# If you if you left this out, then what it would do is it would just basically use the default model
# manager with a simple create read update operations wouldn't apply these changes that we've added here
# for the ordering and for the list display.
admin.site.register(models.User, UserAdmin)
