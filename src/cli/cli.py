from src.contest.parser.contest_parser import ContestParser
from src.contest.contest import Contest

from dataclasses import dataclass

from typing import Callable

class CLI(object):
	line_format = "csti> "

	contest: Contest|None = None
	isQuit: bool = False

	@staticmethod
	def startSession():
		while CLI.isQuit is False:
			action = input(CLI.line_format)
			if action not in actions.keys():
				print(f"Действие {action} не найдено.")
				continue

			actions[action].func()
	
	@staticmethod
	def stopSession():
		CLI.isQuit = True

	@staticmethod
	def selectContest(localId: int|None = None):
		aviableContestsCount = ContestParser.getAviableHwCount()
		if localId:
			pass
			# TODO: Довабить возможность по параметру localId выбирать контест.
		else:
			# TODO: Костыль т.к не поддерживается github classrom
			contests = list()
			for index in range(2, aviableContestsCount):
				contests.append(ContestParser.getHomework(index))
				print(f"Контест №{index} | {contests[-1][1]}")
			
			localId = int(input("Выберите контест: "))
			CLI.contest = Contest(contests[localId - 1][0])
			print(f"Контест №{localId} успешно выбран")

	@staticmethod
	def selectTask():
		if CLI.contest is None:
			print("Контест не выбран")
			return
		
		CLI.contest.selectTask(int(input(f"Введите номер задачи: ")))
		print("Задача выбрана")
		

	@staticmethod
	def showTaskCond():
		if CLI.contest is None:
			print("Контест не выбран")
			return
		
		task = CLI.contest.task
		if task is None:
			print("Задача не выбрана")
			return

		print(task.getCondition())

	@staticmethod
	def help():
		for action in actions:
			print(f"\t{action}\t{actions[action].description}")


@dataclass
class Action:
	func: Callable
	description: str = ""


# TODO: Добавить описание
actions = {
	"selectContest":    Action(CLI.selectContest),
	"selectTask":       Action(CLI.selectTask),
	"showCondition":    Action(CLI.showTaskCond),
	
	"help":             Action(CLI.help),
	"exit":             Action(CLI.stopSession),
}
