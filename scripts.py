import random
from django.utils import timezone
from datacenter.models import Schoolkid, Subject, Lesson, Commendation, Mark, Chastisement


COMMENDATIONS = [
        "Молодец!",
        "Отлично!",
        "Хорошо!",
        "Гораздо лучше, чем я ожидал!",
        "Ты меня приятно удивил!",
        "Великолепно!",
        "Прекрасно!",
        "Ты меня очень обрадовал!",
        "Именно этого я давно ждал от тебя!",
        "Сказано здорово – просто и ясно!",
        "Ты, как всегда, точен!",
        "Очень хороший ответ!",
        "Талантливо!",
        "Ты сегодня прыгнул выше головы!",
        "Я поражен!",
        "Уже существенно лучше!",
        "Потрясающе!",
        "Замечательно!",
        "Прекрасное начало!",
        "Так держать!",
        "Ты на верном пути!",
        "Здорово!",
        "Это как раз то, что нужно!",
        "Я тобой горжусь!",
        "С каждым разом у тебя получается всё лучше!",
        "Мы с тобой не зря поработали!",
        "Я вижу, как ты стараешься!",
        "Ты растешь над собой!",
        "Ты многое сделал, я это вижу!",
        "Теперь у тебя точно все получится!"
    ]


def get_schoolkid(name_schoolkid):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name_schoolkid)
        return schoolkid
    except Schoolkid.DoesNotExist:
        print("Ошибка. Ученик не найден")
    except Schoolkid.MultipleObjectsReturned:
        print("Ошибка. Найдено несколько учеников, вместо одного")


def fix_marks(name):
    schoolkid = get_schoolkid(name)
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(point=5)


def remove_chastisements(name):
    schoolkid = get_schoolkid(name)
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(name, subject_title):
    schoolkid = get_schoolkid(name)
    lesson = Lesson.objects.filter(
        subject__title=subject_title,
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter
    ).order_by('-date').first()
    teacher = lesson.teacher
    subject = lesson.subject
    commendation = Commendation.objects.create(
        text=random.choice(COMMENDATIONS),
        created=timezone.now().date(),
        schoolkid=schoolkid,
        subject=subject,
        teacher=teacher
    )
