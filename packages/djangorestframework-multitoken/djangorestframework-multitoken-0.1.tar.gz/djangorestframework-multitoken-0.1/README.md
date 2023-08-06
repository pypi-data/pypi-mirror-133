# djangorestframework-multitoken

Version of Django REST Framework auth Token allowing multiple Tokens per User.

## Usage

**Install:**

```shell
pip install djangorestframework-multitoken
```

**Enable:**

```python
# settings.py

INSTALLED_APPS = [
    ...
    'rest_framework_multitoken',
    ...
]
```

**Migrate:**

```shell
python manage.py migrate
```

**Sync:**

To create MultiTokens from existing Django REST Framework auth Tokens run:

```shell
python manage.py multitoken_sync
```

If you want to switch back to regular Django REST Framework auth Tokens run:

```shell
# WARNING be careful as data may be lost
python manage.py multitoken_sync --backwards
```

WARNING: The `--backwards` sync may lose data if you have created multiple MultiToken instances for a User.
Only one of the MultiToken instances can be moved back to a regular Django REST Framework auth Token. 
The MultiToken selected to be moved back will be the primary token which is the newest active token for the User.

Note: to run either of those commands you must have both `rest_framework.authtoken` and `rest_framework_multitoken` in `INSTALLED_APPS` and respective database migrations applied.

**Enjoy:**

View and manage Tokens in the Django Admin under `Multi Token`.

Use MultiTokenAuthentication globally or on a per-view basis.

```python
# settings.py - use MultiTokenAuthentication globally
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        ...
        'rest_framework_multitoken.authentication.MultiTokenAuthentication',
        ...
    ],
    ...
}


# views.py - use MultiTokenAuthentication on a per-view basis
from rest_framework_multitoken.authentication import MultiTokenAuthentication
class MyView(APIView):
    authentication_classes = [MultiTokenAuthentication]
    ...
```

Access the MultiToken instances for a User with the `get_user_primary_token` utility method or the `multi_tokens` backwards relationship.

```python
# get_user_primary_token utility method
from rest_framework_multitoken.utils import get_user_primary_token
multi_token = get_user_primary_token(user)

# backwards relationship
multi_tokens = user.multi_tokens.filter(is_active=True)
```

### License

[BSD-3-Clause](LICENSE)
