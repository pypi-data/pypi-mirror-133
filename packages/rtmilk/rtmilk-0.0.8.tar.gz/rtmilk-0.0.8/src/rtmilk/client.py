from asyncio import gather
from dataclasses import dataclass
from datetime import datetime
from logging import getLogger
from typing import List

from .api_async import APIAsync
from .api_sync import API
from .models import RTMError

_log = getLogger('rtmilk')

@dataclass
class _TaskPath:
	listId : str
	taskSeriesId: str
	taskId : str

class Task:
	def __init__(self, title, tags: List[str], startDate, dueDate, complete, note):
		self.path = None
		self.title = title
		self.tags = tags
		self.startDate = startDate # None means no start date
		self.dueDate = dueDate # None means no due date
		self.complete = complete
		self.note = note

	def __repr__(self):
		return f'<Task title={self.title}, startDate={self.startDate}, dueDate={self.dueDate}, tags={self.tags}, complete={self.complete}, note={self.note}>'

	def Attach(self, listId, taskSeriesId, taskId): # attach to the server-side copy
		self.path = _TaskPath(listId, taskSeriesId, taskId)

	def SetStartDate(self, client):
		if self.startDate is None:
			_ = client.api.TasksSetStartDate(timeline=client.timeline,
												list_id=self.path.listId,
												taskseries_id=self.path.taskSeriesId,
												task_id=self.path.taskId)
		else:
			_ = client.api.TasksSetStartDate(timeline=client.timeline,
												list_id=self.path.listId,
												taskseries_id=self.path.taskSeriesId,
												task_id=self.path.taskId,
												start=self.startDate,
												has_start_time=False)

	async def SetStartDateAsync(self, client):
		if self.startDate is None:
			_ = await client.apiAsync.TasksSetStartDate(timeline=client.timeline,
												list_id=self.path.listId,
												taskseries_id=self.path.taskSeriesId,
												task_id=self.path.taskId)
		else:
			_ = await client.apiAsync.TasksSetStartDate(timeline=client.timeline,
												list_id=self.path.listId,
												taskseries_id=self.path.taskSeriesId,
												task_id=self.path.taskId,
												start=self.startDate,
												has_start_time=False)

	def SetDueDate(self, client):
		if self.dueDate is None:
			_ = client.api.TasksSetDueDate(timeline=client.timeline,
											list_id=self.path.listId,
											taskseries_id=self.path.taskSeriesId,
											task_id=self.path.taskId)
		else:
			_ = client.api.TasksSetDueDate(timeline=client.timeline,
											list_id=self.path.listId,
											taskseries_id=self.path.taskSeriesId,
											task_id=self.path.taskId,
											due=self.dueDate,
											has_due_time=False)

	async def SetDueDateAsync(self, client):
		if self.dueDate is None:
			_ = await client.apiAsync.TasksSetDueDate(timeline=client.timeline,
											list_id=self.path.listId,
											taskseries_id=self.path.taskSeriesId,
											task_id=self.path.taskId)
		else:
			_ = await client.apiAsync.TasksSetDueDate(timeline=client.timeline,
											list_id=self.path.listId,
											taskseries_id=self.path.taskSeriesId,
											task_id=self.path.taskId,
											due=self.dueDate,
											has_due_time=False)

	def SetTags(self, client):
		_ = client.api.TasksSetTags(timeline=client.timeline,
								list_id=self.path.listId,
								taskseries_id=self.path.taskSeriesId,
								task_id=self.path.taskId,
								tags=self.tags)

	async def SetTagsAsync(self, client):
		_ = await client.apiAsync.TasksSetTags(timeline=client.timeline,
								list_id=self.path.listId,
								taskseries_id=self.path.taskSeriesId,
								task_id=self.path.taskId,
								tags=self.tags)

	@classmethod
	def CreateFromTaskSeries(cls, listId, taskSeries):
		task0 = taskSeries.task[0]
		result = Task(
			title=taskSeries.name,
			tags=taskSeries.tags.tag if hasattr(taskSeries.tags, 'tag') else taskSeries.tags,
			startDate=task0.start.date() if task0.start is not None else None, # None means no change
			dueDate=task0.due.date() if task0.due is not None else None, # None means no change
			complete=task0.completed is not None,
			note=''
		)
		result.Attach(listId, taskSeries.id, task0.id)
		return result

	@classmethod
	def CreateNew(cls, title, tags, startDate, dueDate=None, note=''):
		return Task(title=title, tags=tags, startDate=startDate, dueDate=dueDate, complete=False, note=note)

# Serialize python datetime object to string for use by filters
def FilterDate(date_):
	return datetime.strftime(date_, '%m/%d/%Y')

def _CheckDates(startDate, dueDate):
	# Cannot set start date earlier than due date
	if startDate is not None and dueDate is not None and startDate > dueDate:
		raise RuntimeError(f"Start date can't be strictly later than due date: {startDate}, {dueDate}")

def _CreateListOfTasks(listResponse):
	if listResponse.tasks.list is None:
		return []
	tasks = []
	for list_ in listResponse.tasks.list:
		if not hasattr(list_, 'taskseries') or list_.taskseries is None:
			continue
		for taskSeries in list_.taskseries:
			tasks.append(Task.CreateFromTaskSeries(listId=list_.id, taskSeries=taskSeries))
	return tasks

class Client:
	def __init__(self, clientId, clientSecret, token):
		self.api = API(clientId, clientSecret, token)
		self.apiAsync = APIAsync(clientId, clientSecret, token)
		self.timeline = self.api.TimelinesCreate().timeline

	async def GetAsync(self, filter_):
		_log.info(f'Get: {filter_}')
		listResponse = await self.apiAsync.TasksGetList(filter=filter_)
		return _CreateListOfTasks(listResponse)

	def Get(self, filter_):
		_log.info(f'Get: {filter_}')
		listResponse = self.api.TasksGetList(filter=filter_)
		return _CreateListOfTasks(listResponse)

	async def AddAsync(self, task):
		_log.info(f'AddAsync: {task}')
		# Adds to Inbox by default
		assert task.path is None, f'Already added: {task}'
		# need to wait for this one so that we have something to set the other properties on
		taskResponse = await self.apiAsync.TasksAdd(self.timeline, task.title)
		task.Attach(
			taskResponse.list.id,
			taskResponse.list.taskseries[0].id,
			taskResponse.list.taskseries[0].task[0].id)

		setTags = task.SetTagsAsync(self)

		_CheckDates(task.startDate, task.dueDate)

		# shouldn't have to order these since we know that startDate <= dueDate
		setDueDate = task.SetDueDateAsync(self)
		setStartDate = task.SetStartDateAsync(self)

		awaitables = [setTags, setDueDate, setStartDate]
		if task.note != '':
			awaitables.append(self.apiAsync.TasksNotesAdd(
				timeline=self.timeline,
				list_id=task.path.listId,
				taskseries_id=task.path.taskSeriesId,
				task_id=task.path.taskId,
				note_title='',
				note_text=task.note))
		await gather(*awaitables)

	def Add(self, task):
		_log.info(f'Add: {task}')
		# Adds to Inbox by default
		assert task.path is None, f'Already added: {task}'
		taskResponse = self.api.TasksAdd(self.timeline, task.title)
		task.Attach(
			taskResponse.list.id,
			taskResponse.list.taskseries[0].id,
			taskResponse.list.taskseries[0].task[0].id)
		task.SetTags(self)

		_CheckDates(task.startDate, task.dueDate)

		task.SetDueDate(self)
		task.SetStartDate(self)
		if task.note != '':
			_ = self.api.TasksNotesAdd(timeline=self.timeline,
										list_id=task.path.listId,
										taskseries_id=task.path.taskSeriesId,
										task_id=task.path.taskId,
										note_title='',
										note_text=task.note)

	async def EditAsync(self, task):
		_log.info(f'Edit: {task}')
		_log.debug(f'Setting {task.title} tags to {task.tags}')
		await task.SetTagsAsync(self)

		_log.debug(f'Setting {task.title} start date to {task.startDate}')
		_log.debug(f'Setting {task.title} due date to {task.dueDate}')
		try:
			await task.SetStartDateAsync(self)
			await task.SetDueDateAsync(self)
		except RTMError:
			_log.warning('Trying other ordering')
			await task.SetDueDateAsync(self)
			await task.SetStartDateAsync(self)

	def Edit(self, task):
		_log.info(f'EditAsync: {task}')
		_log.debug(f'Setting {task.title} tags to {task.tags}')
		task.SetTags(self)

		_log.debug(f'Setting {task.title} start date to {task.startDate}')
		_log.debug(f'Setting {task.title} due date to {task.dueDate}')
		try:
			task.SetStartDate(self)
			task.SetDueDate(self)
		except RTMError:
			_log.warning('Trying other ordering')
			task.SetDueDate(self)
			task.SetStartDate(self)

	async def DeleteAsync(self, task):
		_log.info(f'DeleteAsync: {task}')
		await self.apiAsync.TasksDelete(timeline=self.timeline,
								list_id=task.path.listId,
								taskseries_id=task.path.taskSeriesId,
								task_id=task.path.taskId)

	def Delete(self, task):
		_log.info(f'Delete: {task}')
		self.api.TasksDelete(timeline=self.timeline,
								list_id=task.path.listId,
								taskseries_id=task.path.taskSeriesId,
								task_id=task.path.taskId)
