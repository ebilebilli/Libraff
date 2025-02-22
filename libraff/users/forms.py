from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomerUser

class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomerUser
        fields = ('username', 'email')


class CustomerUserChangeFomr(UserChangeForm):
    model = CustomerUser
    fields = ('username', 'email', 'bio', 'avatar')