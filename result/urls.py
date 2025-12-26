from django.urls import path

from result.views import *


urlpatterns = [
    path('result-checker', result_checker_view,  name='result_checker'),
    path('result-checker-ajax', result_checker_ajax_view, name='ajax_result_checker'),
    path('result-checker-output', result_checker_output_view,  name='result_checker_output'),
    path('result-updater-ajax', result_update_ajax_view, name='ajax_result_updater'),
]