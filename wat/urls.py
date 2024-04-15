from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from waterflow.views import home_view, thank_you_view, source_water_pie_chart, flowchart_view, user_home_view, logout_view, source_dash_view, generate_pdf
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    # path('login/', LoginView.as_view(template_name='socialaccount/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),

    path('', home_view, name='home'),
    path('user_home/', user_home_view, name='user_home'),
    path('registration_done/', thank_you_view, name='registration_done'),
    path('questionnaire/', include('waterflow.urls')),
    path('thank-you/', thank_you_view, name='thank_you'),

    path('source-water-pie-chart/', source_water_pie_chart,
         name='source_water_pie_chart'),
    path('flowchart/', flowchart_view, name='flowchart'),

    path('accounts/', include('allauth.urls')),
    # path('accounts/', include('allauth.socialaccount.urls')),

    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('source-dash/', source_dash_view, name='source_dash_view'),
    path(
        "map.html", TemplateView.as_view(
            template_name="chennai_rainfall_map.html")
    ),
    path('generate-pdf/', generate_pdf, name='generate_pdf')


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
        path('hello', TemplateView.as_view(template_name='index.html')),
    ]