from django.contrib import admin

from .models import Card, Department, DepartmentLeader, DepartmentSummary, Team, Engineer, TeamLeader, TeamSummary, SeniorManager, Review

# Register your models here.
admin.site.register(Card)
admin.site.register(Department)
admin.site.register(DepartmentLeader)
admin.site.register(DepartmentSummary)
admin.site.register(Team)
admin.site.register(Engineer)
admin.site.register(TeamLeader)
admin.site.register(TeamSummary)
admin.site.register(SeniorManager)
admin.site.register(Review)
