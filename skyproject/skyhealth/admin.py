from django.contrib import admin

from .models import Card, Department, DepartmentSummary, Team, TeamSummary, Review, Profile

# Register your models here.
admin.site.register(Card)
admin.site.register(Department)
admin.site.register(DepartmentSummary)
admin.site.register(Team)
admin.site.register(TeamSummary)
admin.site.register(Review)
admin.site.register(Profile)