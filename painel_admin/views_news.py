from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from noticias.models import Noticia
from noticias.forms import NoticiaForm

@method_decorator(staff_member_required, name='dispatch')
class AdminNewsListView(ListView):
    model = Noticia
    template_name = 'painel_admin/noticias_list.html'
    context_object_name = 'noticias'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-publicado_em')

@method_decorator(staff_member_required, name='dispatch')
class AdminNewsCreateView(CreateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'painel_admin/noticia_form.html'
    success_url = reverse_lazy('painel_admin:news_list')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class AdminNewsUpdateView(UpdateView):
    model = Noticia
    form_class = NoticiaForm  # usa o mesmo formulário estilizado
    template_name = 'painel_admin/noticia_form.html'  # mesmo template do Create
    success_url = reverse_lazy('painel_admin:news_list')


@method_decorator(staff_member_required, name='dispatch')
class AdminNewsDeleteView(DeleteView):
    model = Noticia
    template_name = 'admin/noticia_confirm_delete.html'
    success_url = reverse_lazy('painel_admin:news_list')
