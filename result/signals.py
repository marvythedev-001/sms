from django.dispatch import receiver
from result.models import ResultModel
from django.db.models.signals import post_save


@receiver(post_save, sender=ResultModel)
def get_total_score_and_average(sender, instance, created, **kwargs):
    result = instance
    student_class = result.student_class
    subjects = student_class.subjects_taught.all
    sub_ids = []
    for sub in subjects:
        sub_ids.append(str(sub.id))
    result_list = result.report
    total = 0.0
    i = 0
    for result in result_list:
        for s_id in sub_ids:
            main_result = result[s_id]
            if main_result:
                total += main_result["total"]
                i += 1
    average = float(total / i)
    result.total_score = total
    result.average = average