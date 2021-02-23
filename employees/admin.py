from django.contrib import admin

from .models import (
    Job, Manager, WorkPlace, Supervisor, Employee, Position,
)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkPlace)
class WorkPlaceAdmin(admin.ModelAdmin):
    pass


@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass
