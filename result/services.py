def grade_calculation(score):
    if score >= 80:
        return 'A'
    elif score >= 70 and score < 80:
        return 'B'
    elif score >= 60 and score < 70:
        return 'C'
    elif score >= 50 and score < 60:
        return 'D'
    elif score >= 40 and score < 50:
        return 'E'
    else:
        return 'F'