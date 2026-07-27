from database import course_queries


def get_active_courses(user_id):
    return course_queries.get_active_courses(user_id)


def user_has_active_courses(user_id):
    return bool(get_active_courses(user_id))
