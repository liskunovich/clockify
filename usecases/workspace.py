import asyncio
import isodate
from clockify import api
from clockify.dto import Workspace, Task, EmployeeReport
from clockify.utils.get_interval import get_interval
from clockify.enums import TimeInterval
from datetime import datetime


async def get_workspace() -> list[Workspace] or Workspace:
    workspaces = await api.get_workspace_data()
    workspace = list(filter(lambda w: w.id == '648b6ba2120abb5b98c51126', workspaces))[0]
    # Here is the workspace call's 'CherryPickers' with id '648b6ba2120abb5b98c51126'
    return workspace


async def get_tasks(workspace, employee) -> list[Task]:
    start, end = get_interval(datetime.now(), TimeInterval.TWO_WEEKS)
    params = {'start': start.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 'end': end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}
    tasks = await api.get_time_entries(workspace.id, employee.id)
    return tasks


async def search_longest_task(tasks: list[Task]):
    longest_task = tasks[0]
    for task in tasks:
        if task.get_worktime() > longest_task.get_worktime():
            longest_task = task
    return longest_task


async def get_total_worktime(tasks: list[Task]):
    hours = 0
    for task in tasks:
        hours += round(task.get_worktime() / 3600, 2)
    return hours


async def get_details_about_workspace(workspace):
    reports = []
    for employee in workspace.employees:
        tasks = await get_tasks(workspace, employee)
        worktime = await get_total_worktime(tasks)
        longest_task = await search_longest_task(tasks)
        reports.append(
            EmployeeReport(employee=employee,
                           worktime=worktime,
                           longest_task=longest_task,
                           salary=worktime * 8)
        )
    return reports

    # workspace = await get_workspace()
    # await get_details_about_workspace(workspace)
