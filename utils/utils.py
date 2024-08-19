import pathlib
import uuid


def generate_filename_user_avatar(instance, filename):
    return generate_filename(instance, filename, 'users')


def generate_filename_course_preview(instance, filename):
    return generate_filename(instance, filename, 'courses')


def generate_filename_lesson_preview(instance, filename):
    return generate_filename(instance, filename, 'lessons')


def generate_filename(instance, filename, subdir):
    return pathlib.Path(subdir) / f"{uuid.uuid4().hex}.{filename.split('.')[-1]}"
