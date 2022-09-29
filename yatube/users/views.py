# Create your views here.
# Функция reverse_lazy позволяет получить URL по параметрам функции path()
# Берём, тоже пригодится
from django.urls import reverse_lazy

# Импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm


class SignUp(CreateView):
    # из какого гласса берем форму
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную
    success_url = reverse_lazy("posts:index")
    # имя шаблона, куда будет передана переменная form с объектом HTML
    template_name = "users/signup.html"
