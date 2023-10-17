# DevsChat
Real-time chat application using Python, Django, and Redis. The application should allow users to send and receive messages in real-time, using a technology such as WebSockets.


1. Clone the Git repository:

```bash
   git clone https://github.com/wcreativo/DevsChat
   cd DevsChat
```

2. Run Docker

```bash
   docker-compose build
   docker-compose up 
```

3. Login

Go to http://localhost:8000/login/

# Highlights
- Use a database (PostgresSQL/MySQL)

```bash
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_NAME"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
    }
}
```

- The application should include proper logging and monitoring

```bash
# websocket_throttling.py
class WebSocketThrottlingMiddleware(BaseMiddleware):
    def __init__(self, inner, rate_limit=1):
        self.rate_limit = rate_limit
        self.message_timestamps = {}
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        user_id = scope.get("user").id

        if user_id:
            current_time = time.time()
            last_message_time = self.message_timestamps.get(user_id, 0)
    ...

```

- Initial data for sign up: name, last name, email.
```bash
# users/forms.py
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        ]
    ...

```

- Validation rules for signup data are up to you
```bash
# realchat/forms.py
name_validator = RegexValidator(
    regex=r"^[A-Za-z0-9_-]+$",
    message="Name can only contain letters, numbers, _, and -",
)


class RoomSelectionForm(forms.Form):
    selected_room = forms.ChoiceField(choices=(), widget=forms.Select())

    def __init__(self, *args, **kwargs):
        room_choices = kwargs.pop("room_choices", [])
        super(RoomSelectionForm, self).__init__(*args, **kwargs)
        self.fields["selected_room"].choices = room_choices
    ...

```
- It will be a big plus if you deploy the services somewhere in the cloud (heroku, gcloud, aws, azure, etc). (Pending)

- It's ok if you just do it locally, but use docker.

```bash
# Dockerfile
FROM python:3.10-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY ./src /app
    ...

```

- Use github (or other git repo). It's a big plus to include github actions.

```bash
# checks.yml
---
name: Checks

on: [push]

jobs:
  test-lint:
    name: Test and Lint
    runs-on: ubuntu-20.04
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKERHUB_USER }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - name: Checkout
        uses: actions/checkout@v2
      - name: Test
        run: docker-compose run --rm django sh -c "python manage.py wait_for_db && python manage.py test"
      - name: Lint
    ...
```

- Do tests and integrations tests.

```bash
# realchat/test_websocket_throtthling.py
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from apps.realchat.middleware.websocket_throttling import WebSocketThrottlingMiddleware
from apps.realchat.routing import websocket_urlpatterns


class WebSocketThrottlingMiddlewareTest(TestCase):
    async def test_chat_consumer(self):
        django_asgi_app = get_asgi_application()

        application = ProtocolTypeRouter(
            {
                "http": django_asgi_app,
                "websocket": AllowedHostsOriginValidator(
                    AuthMiddlewareStack(WebSocketThrottlingMiddleware(URLRouter(websocket_urlpatterns), rate_limit=1))
                ),
            }
        )
    ...
```

- BONUS: If you can implement API throttling for messages in real time, that's a big one. 

```bash
# config/asgi.py
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                WebSocketThrottlingMiddleware(
                    URLRouter(websocket_urlpatterns), rate_limit=1
                )
            )
        ),
    }
)
    ...
```

- Log every API call received, log format is up to you.

```bash
# realchat/views.py
class CreateRoomView(LoginRequiredMixin, FormView):
    template_name = "realchat/create_room.html"
    form_class = CreateRoomForm

    def form_valid(self, form):
        room_name = form.cleaned_data["name"]
        Chatrooms.objects.create(name=room_name)
        logger.info(f'The user {self.request.user.username} has created the room "{room_name}"')
        return redirect("room", room_name=room_name)
    ...
```

