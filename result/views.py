from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from academics.models import SubjectsModel
from accounts.models import StudentModel, StudentProfileModel
from result.models import ResultModel
from result.services import grade_calculation
from school_structure.models import AcademicSessionModel, AcademicTermModel, StudentClassArmModel, StudentClassModel

# Create your views here.

def result_checker_view(request):
    sessions = AcademicSessionModel.objects.all()
    class_list = StudentClassModel.objects.all()
    class_categories = ["creche", "pre-nursery", "nursery", "primary", "junior-secondary", "senior-secondary"]
    data = {
        "sessions": sessions,
        "class_list": class_list,
        "class_categories": class_categories,
    }
    return render(request, 'result/result_checker.html', data)


def result_checker_ajax_view(request):
    if request.method == 'GET':
        ajax_request = request.GET.get("request")
        if ajax_request:
            if ajax_request == 'term':
                session = request.GET.get("changed_value")
                terms = AcademicTermModel.objects.filter(academic_session=session).values('id', 'name')
                
                return JsonResponse({"requested_data": list(terms)})
            elif ajax_request == 'student_class':
                selected_category = request.GET.get("changed_value")
                classes = StudentClassModel.objects.filter(klass_type=selected_category.upper()).values('id', 'name', 'arm')
                class_list = list(classes)
                refined_class_list = []
                class_names = []
                # return JsonResponse({"class_list": class_list})
                for klass in class_list:
                    if len(refined_class_list) != 0:
                        for ref_class in refined_class_list:
                            if ref_class:
                                # return JsonResponse({"class_list": class_list})
                                if ref_class["name"].lower() == klass["name"].lower():
                                    if not ref_class["name"].lower() in class_names: # This line may be removed
                                        query = StudentClassArmModel.objects.filter(pk=klass["arm"]).values('name')
                                        for q in list(query):
                                            if q["name"].upper() in ref_class["arm"]:
                                                pass
                                            else:
                                                ref_class["arm"].append(q["name"].upper())
                                else:
                                    if not ref_class["name"].lower() in class_names:
                                        query = StudentClassArmModel.objects.filter(pk=klass["arm"]).values('name')
                                        
                                        refined_class_list.append({
                                            "id": klass["id"],
                                            "name": klass["name"].upper(),
                                            "arm": [query[0]["name"].upper()]
                                        })
                                        class_names.append(klass["name"])
                    else:
                        query = StudentClassArmModel.objects.filter(pk=klass["arm"]).values('name')
                        # return JsonResponse({"query": list(query)})
                        ext_klass = klass
                        refined_class_list.append({
                            "id": klass["id"],
                            "name": klass["name"].upper(),
                            "arm": [query[0]["name"].upper()]
                        })
                        class_names.append(klass["name"])
                    
                return JsonResponse({"requested_data": refined_class_list})
            elif ajax_request == 'class_arm':
                selected_class = request.GET.get("changed_value")
                arms = []
                refined_arms = []
                selected_class_list = StudentClassModel.objects.filter(name=selected_class.lower())
                # return selected_class_list
                for cls in selected_class_list:
                    if cls.arm not in arms:
                        arms.append(cls.arm)
                for arm in arms:
                    present_arm = StudentClassArmModel.objects.get(pk=arm).values('id', 'name')
                    refined_arms.append(present_arm)
                return JsonResponse({"requested_data": refined_arms})
        else:
            return JsonResponse({"Error": "There was an error with getting request"})
        
        
def result_checker_output_view(request):
    processed_results = []
    processed_results_pro = []
    if request.method == 'POST':
        academic_session = request.POST.get("academic-session")
        academic_term = request.POST.get("academic-term")
        student_class_category = request.POST.get("student-class-category")
        student_class = request.POST.get("student-class")
        student_class_arm = request.POST.get("student-class-arm")
        # return HttpResponse(academic_session, academic_term, student_class, student_class_arm, student_class_category)
        results = ResultModel.objects.filter(academic_session=academic_session, term=academic_term, student_class__id=student_class, student_class__arm=student_class_arm)
        student_list = StudentProfileModel.objects.filter(academic_session=academic_session, academic_term=academic_term)
        # for res in results:
        #     subjects_result = {
        #         int(sub_id): data
        #         for sub_res in res.report for sub_id, data in sub_res.items()
        #     }

        #     processed_results.append({
        #         'id': res.pk,
        #         'student': res.student,
        #         'subjects': subjects_result,
        #         'total_score': res.total_score,
        #         'last_updated': res.last_updated
        #     })
            
        data_structure = {}
        for result in results:
            real_result = result.report
            for res in real_result:
                subject_idxs = list(res.keys()) #This is subjet_idxs
                test_values = res[subject_idxs[0]]
                # return JsonResponse({"data": test_values})
                # return JsonResponse({"data": test_values})
                if processed_results_pro:
                    # return HttpResponse(pro_res.keys())
                    # subject_names = []
                    # for idx in subject_idxs:
                    #     subject_object = SubjectsModel.objects.filter(pk=int(idx)).values("name")
                    #     subject_object = list(subject_object)
                    #     subject_names.append(subject_object[0]["name"])
                        # subject_names.append(list(subject_object))
                    # return JsonResponse({"data": subject_names})
                    # result = list(pro_res.keys()) 
                    proc_subject_names = []
                    for processed_result in processed_results_pro:
                        key_list = list(processed_result.keys())
                        proc_subject_names.append(key_list[0])
                    # return JsonResponse({"data": res})
                    subject_id = list(res.keys())
                    subject_object = SubjectsModel.objects.filter(pk=int(subject_id[0])).values("name")
                    subject_object = list(subject_object)
                    subject_name = subject_object[0]["name"]
                    bool_result = subject_name in proc_subject_names
                    # return JsonResponse({"data": bool_result})
                    if subject_name in proc_subject_names:
                        for idx, processed_result in enumerate(processed_results_pro):
                            sub_name_list = list(processed_result.keys())
                            if subject_name == sub_name_list[0]:
                                
                                processed = processed_results_pro[idx]
                                student_result_data = processed[subject_name]
                                # subject = SubjectsModel.objects.get(pk=pro_res.keys()[0])
                                student_result_data[result.student.id] = {
                                    "student_name": f"{result.student.first_name} {result.student.last_name}",
                                    "admission_number": result.student.admission_number,
                                    "subject_id": int(subject_id[0]),
                                    "result_id": result.id,
                                    "scores": {
                                        "first_test": test_values["1st-test"],
                                        "secondtest": test_values["2nd-test"],
                                        "thirdtest": test_values["3rd-test"],
                                        "exam": test_values["exam"],
                                        "total": test_values["total"],
                                        "grade": test_values["grade"],
                                    }
                                }
                                break
                    else:
                        # for sub_id in subject_names:
                        # subject = SubjectsModel.objects.get(pk=sub_id)
                        
                        data_structure[subject_name] = {
                            result.student.id: {
                                "student_name": f"{result.student.first_name} {result.student.last_name}",
                                "admission_number": result.student.admission_number,
                                "subject_id": int(subject_id[0]),
                                "result_id": result.id,
                                "scores": {
                                    "first_test": test_values["1st-test"],
                                    "second_test": test_values["2nd-test"],
                                    "third_test": test_values["3rd-test"],
                                    "exam": test_values["exam"],
                                    "total": test_values["total"],
                                    "grade": test_values["grade"],
                                }
                            }
                        }
                        # processed_results_pro.append(data_structure)
                        # return JsonResponse({"datas": processed_results_pro})
                else:
                    subject = SubjectsModel.objects.get(pk=subject_idxs[0])
                    # return JsonResponse({"data": "Absent"})
                    data_structure[subject.name] = {
                        result.student.id: {
                            "student_name": f"{result.student.first_name} {result.student.last_name}",
                            "admission_number": result.student.admission_number,
                            "subject_id": int(subject.id),
                            "result_id": result.id,
                            "scores": {
                                "first_test": test_values["1st-test"],
                                "second_test": test_values["2nd-test"],
                                "third_test": test_values["3rd-test"],
                                "exam": test_values["exam"],
                                "total": test_values["total"],
                                "grade": test_values["grade"],
                            }
                        }
                    }
                    # return JsonResponse({"data": data_structure})
                    processed_results_pro.append(data_structure)
        # return JsonResponse({"data": processed_results_pro})
        [
            {
                "1": {
                    ("1", "Alice", "admission_number", "student_ing"): {
                        "first_test": "value",
                        "second_test": "value",
                        "third_test": "value"
                    }
                }
            },
            {
                "2": {
                    ("1", "Alice", "admission_number", "student_ing"): {
                        "first_test": "value",
                        "second_test": "value",
                        "third_test": "value"
                    }
                }
            },
        ]
    
        [
            {
                "subject_id": {
                    "student_id": {
                        "student_name": "value",
                        "admission_number": "value",
                        "student_img": "value",
                        "scores": {
                            "first_test": "value",
                            "second_test": "value",
                            "third_test": "value"
                        }
                    },
                    "student_id": {
                        "student_name": "value",
                        "admission_number": "value",
                        "student_img": "value",
                        "scores": {
                            "first_test": "value",
                            "second_test": "value",
                            "third_test": "value"
                        }
                    },
                    ("student_id", "student_name", "admission_number", "student_ing"): {
                        "first_test": "value",
                        "second_test": "value",
                        "third_test": "value"
                    }
                }
            },
            {
                "subject_id": {
                    ("student_id", "student_name", "admission_number", "student_ing"): {
                        "first_test": "value",
                        "second_test": "value",
                        "third_test": "value"
                    }
                }
            },
            {
                "subject_id": {
                    ("student_id", "student_name", "admission_number", "student_ing"): {
                        "first_test": "value",
                        "second_test": "value",
                        "third_test": "value"
                    }
                }
            }
        ]
        student_class_object = StudentClassModel.objects.get(pk=student_class)
        num_of_students = len(results)
        # return JsonResponse({"output": list(results)})
    else:
        results = None
        num_of_students = 0
        student_class_object = None
        
    
    sessions = AcademicSessionModel.objects.all()
    class_list = StudentClassModel.objects.all()
    class_categories = ["creche", "pre-nursery", "nursery", "primary", "junior-secondary", "senior-secondary"]
    
    real_academic_session = AcademicSessionModel.objects.get(pk=academic_session)
    real_academic_term = AcademicTermModel.objects.get(pk=academic_term)
    real_student_class_arm = StudentClassArmModel.objects.get(pk=student_class_arm)
    real_student_class = StudentClassModel.objects.get(pk=student_class)
    
    results_lookup = {}

    for result_block in processed_results_pro:  # outer list
        for subject_name, students_data in result_block.items():
            for student_id_str, payload in students_data.items():
                subject_id = payload["subject_id"]
                student_id = int(student_id_str)
                
                if subject_id not in results_lookup:
                    results_lookup[subject_id] = {}

                results_lookup[subject_id][student_id] = {
                    "student_name": payload["student_name"],
                    "admission_number": payload["admission_number"],
                    "result_id": payload["result_id"],
                    "scores": payload["scores"],
            }

    
    # return JsonResponse({"data": processed_results_pro})
        
    data = {
        "results": processed_results_pro[0] if processed_results_pro else {},
        "num_of_students": num_of_students,
        "sessions": sessions,
        "class_list": class_list,
        "class_categories": class_categories,
        "student_class_object": student_class_object,
        "student_list": student_list,
        "academic_session": real_academic_session,
        "academic_term": real_academic_term,
        "student_class": real_student_class,
        "student_class_arm": real_student_class_arm,
        "results_lookup": results_lookup
    }
        
    return render(request, 'result/result_checker_final.html', data)


def result_update_ajax_view(request):
    if request.method == 'GET':
        subject_id = request.GET.get("subject_id")
        result_id = request.GET.get("result_id")
        first_test = request.GET.get("first_test")
        second_test = request.GET.get("second_test")
        third_test = request.GET.get("third_test")
        exam = request.GET.get("exam")
        total_score = request.GET.get("total_score")
        student_id = request.GET.get("student_id")
        academic_session = request.GET.get("academic_session")
        academic_term = request.GET.get("academic_term")
        student_class = request.GET.get("student_class")
        student_class_arm = request.GET.get("student_class_arm")
        
        if result_id:
            total_score = 0
            result = ResultModel.objects.get(pk=result_id)
            result_list = result.report
            presence_counter = 0
            res_index = 0
            for idx, res in enumerate(result_list):
                # return JsonResponse({"value": res.__contains__(subject_id)})
                if res.__contains__(subject_id):
                    presence_counter += 1
                    res_index += idx
                    break
             
            if presence_counter > 0:
                report_data = result_list[res_index]
                # return JsonResponse({"value": report["1st-test"]})
                report = report_data[subject_id]
                report["1st-test"] = first_test
                report["2nd-test"] = second_test
                report["3rd-test"] = third_test
                report["exam"] = exam
                total = float(first_test) + float(second_test) + float(third_test) + float(exam)
                # return JsonResponse({"value": total})
                report["total"] = total
                calc_grade = grade_calculation(total)
                report["grade"] = calc_grade
                total_score += total
                # return JsonResponse({"data": report})
                result.save()
                    
            else:
                
                total = float(first_test) + float(second_test) + float(third_test) + float(exam)
                calc_grade = grade_calculation(total)
                result_stucture = {f"{subject_id}": {"1st-test": f"{first_test}", "2nd-test": f"{second_test}", "3rd-test": f"{third_test}", "exam": exam, "total": total, "grade": calc_grade}}
                result.report.append(result_stucture)
                result.save()
                
        else:
            student = StudentModel.objects.get(pk=student_id)
            academic_session = AcademicSessionModel.objects.get(pk=academic_session)
            academic_term = AcademicTermModel.objects.get(pk=academic_term)
            student_class = StudentClassModel.objects.get(pk=student_class)
            student_class_arm = StudentClassArmModel.objects.get(pk=student_class_arm)
            total = float(first_test) + float(second_test) + float(third_test) + float(exam)
            calc_grade = grade_calculation(total)
            result_stucture = [{f"{subject_id}": {"1st-test": f"{first_test}", "2nd-test": f"{second_test}", "3rd-test": f"{third_test}", "exam": exam, "total": total, "grade": calc_grade}}]
            new_student_result = ResultModel.objects.create(student=student, academic_session=academic_session, term=academic_term, student_class=student_class, student_class_arm=student_class_arm, report=result_stucture, total_score=total, average=total)
            new_student_result.save()
                    

        return JsonResponse({"total": total, "grade": calc_grade})
    else:
        return JsonResponse({"error": "Problem Encountered While Making Request!"})
    