from django.contrib import admin
from .models import QuestionBinderTest , ClassTermTest , CourseTest, Answer


admin.site.register(ClassTermTest)
admin.site.register(QuestionBinderTest)
admin.site.register(CourseTest)
admin.site.register(Answer)