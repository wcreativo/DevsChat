from django.shortcuts import redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.views.generic.edit import FormView


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your account has been created! You are now able to login!")
        return redirect("login")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
