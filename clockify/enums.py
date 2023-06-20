from enum import Enum


class ApiRoute(Enum):
    WORKSPACES = 'https://api.clockify.me/api/v1/workspaces'
    USER_DATA = 'https://api.clockify.me/api/v1/workspaces/{workspaceId}/member-profile/{userId}'
    TIME_ENTRIES = 'https://api.clockify.me/api/v1/workspaces/{workspaceId}/user/{userId}/time-entries'


class TimeInterval(Enum):
    WEEK = 'week'
    TWO_WEEKS = '2week'
    THREE_WEEKS = '3week'
    MONTH = 'month'
