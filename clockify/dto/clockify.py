from __future__ import annotations

import inspect
from dataclasses import dataclass
import isodate


@dataclass
class EmployeeReport:
    employee: Employee
    worktime: int
    longest_task: Task
    salary: float


@dataclass
class TimeInterval:
    start: str
    end: str
    duration: str


@dataclass
class Task:
    id: str
    description: str
    employee: Employee
    time_interval: TimeInterval

    def get_worktime(self):
        return isodate.parse_duration(self.time_interval.duration).total_seconds()


@dataclass
class Employee:
    id: str
    name: str


@dataclass
class Workspace:
    id: str
    name: str
    employees: list[Employee]
