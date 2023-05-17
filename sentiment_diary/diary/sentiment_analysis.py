from datetime import datetime


def sentiment_analyse(diary_list):
    weekly_result = {
        "happy": 0,
        "sad": 0,
        "angry": 0
    }
    monthly_result = {
        "happy": 0,
        "sad": 0,
        "angry": 0
    }

    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_week = now.isocalendar()[1]
    for diary in diary_list:
        if diary.create_date.year == current_year:
            if diary.create_date.month == current_month:
                monthly_result[diary.sentiment] += 1
                if diary.create_date.isocalendar()[1] == current_week:
                    weekly_result[diary.sentiment] += 1
    return weekly_result, monthly_result