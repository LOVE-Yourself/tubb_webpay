from .models import Course,CourseResource,Video,lesson
import xadmin

class CourseAdmin(object):

    list_display = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    search_fields = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums',]
    list_filter = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']

class CourseResourceAdmin(object):

    list_display = ['course', 'name', 'downlod', 'add_time',]
    search_fields = ['course', 'name', 'downlod']
    list_filter = ['course', 'name', 'downlod', 'add_time',]

class VideoAdmin(object):

    list_display = ['lesson', 'name','add_time',]
    search_fields = ['lesson', 'name',]
    list_filter = ['lesson', 'name','add_time',]

class lessonAdmin(object):

    list_display = ['course', 'name','add_time',]
    search_fields = ['course', 'name',]
    list_filter = ['course', 'name','add_time',]



xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(lesson,lessonAdmin)


