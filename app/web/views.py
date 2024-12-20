from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic
from API.models import Car, Comment
from web.forms import CarForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View, RedirectView
from web.filters import CarFilter
from django.urls import reverse_lazy
from django.contrib import messages

class CarListView(generic.ListView):
    model = Car
    queryset = Car.objects.all()
    paginate_by = 5
    template_name = "web/car_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CarFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs



class CarCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = "web/car_new.html"
    success_message = "%(name)s успешно создан"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % {
        'name': f"{cleaned_data.get('make', 'Unknown')} {cleaned_data.get('model', 'Unknown')}"
    }


class CarDetailView(DetailView):
    model = Car
    template_name = "web/car_detail.html"
    context_object_name = "car"

    def get_context_data(self, **kwargs):
        comments = Comment.objects.filter(car=self.object)
        context = super().get_context_data(**kwargs)
        context['comments'] = comments
        return context


class CarUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Car
    template_name = "web/car_edit.html"
    fields = ["description", "make", "model", "year"]
    success_message = "%(name)s успешно обновлен"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.error(request, "Вы не можете редактировать чужую машину.")
            return redirect(reverse('web_car_detail', kwargs={'pk': obj.pk}))
        return super().post(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message % {
        'name': f"{cleaned_data.get('make', 'Unknown')} {cleaned_data.get('model', 'Unknown')}"
    }



class CarDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Car
    template_name = "web/car_delete.html"
    success_url = reverse_lazy("web_car_list")
    success_message = "%(name)s успешно удален"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.error(request, "Вы не можете удалить чужую машину.")
            return redirect(reverse('web_car_detail', kwargs={'pk': obj.pk}))
        return  super().dispatch(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message % {
            'name': "Автомобиль"
        }


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        car = get_object_or_404(Car, id=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = car
            comment.user = request.user
            comment.save()
            return redirect(reverse('web_car_detail', kwargs={'pk': car.pk}))
        else:
            print(form.errors)

