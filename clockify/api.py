import asyncio
import os

from dacite import from_dict
from aiohttp import ClientSession

from .enums import ApiRoute
from .dto import Task, Employee, TimeInterval, Workspace


class ClockifyAPI:
    DEFAULT_HEADERS = {
        'x-api-key': os.environ.get('API_KEY')
    }

    async def fetch(self, url, response_format="json", **kwargs):
        async with ClientSession() as session:
            response = await session.get(url, headers=self.DEFAULT_HEADERS, **kwargs)
            if hasattr(response, response_format):
                format_prop = getattr(response, response_format)
                return format_prop if not callable(format_prop) else await format_prop()
            return response

    async def get_user_data(self, workspace_id, user_id) -> Employee:
        url = ApiRoute.USER_DATA.value.format(workspaceId=workspace_id, userId=user_id)
        response = await self.fetch(url)
        return from_dict(data_class=Employee, data={"id": user_id, **response})

    async def get_time_entries(self, workspace_id, user_id, **kwargs) -> list[Task]:
        url = ApiRoute.TIME_ENTRIES.value.format(workspaceId=workspace_id, userId=user_id)
        response = await self.fetch(url, **kwargs)

        time_entries = []

        for time_entry in response:
            user_data = await self.get_user_data(workspace_id, time_entry.get('userId'))
            time_interval = time_entry.get('timeInterval')

            task = Task(id=time_entry.get('id'),
                        description=time_entry.get('description'),
                        employee=Employee(id=time_entry.get('userId'), name=user_data.name),
                        time_interval=TimeInterval(start=time_interval.get('start'),
                                                   end=time_interval.get('start'),
                                                   duration=time_interval.get('duration')))
            time_entries.append(task)
        return time_entries

    async def get_workspace_data(self) -> list[Workspace]:
        url = ApiRoute.WORKSPACES.value
        response = await self.fetch(url)
        workspaces = []
        for w in response:
            memberships = w.get('memberships')
            employees = await asyncio.gather(
                *list(map(lambda ms: self.get_user_data(w.get('id'), ms.get("userId")), memberships)))
            workspace = Workspace(id=w.get('id'), name=w.get('name'), employees=employees)
            workspaces.append(workspace)
        return workspaces


api = ClockifyAPI()

# async def get_projects_data(self, workspace_id) -> list:
#     url = ApiRoute.PROJECTS.value.format(workspaceId=workspace_id)
#     return await self.fetch(url)
#
# async def get_tasks_on_project(self, workspace_id, project_id) -> list:
#     url = ApiRoute.TASKS.value.format(workspaceId=workspace_id, projectId=project_id)
#     return await self.fetch(url)
