from src.contest.parser.contest_parser import ContestParser
from src.contest.contest import Contest

import click
import pickle


@click.group()
def messages():
  pass


@click.command(name="select-contest")
def selectContest():
	aviableContestsCount = ContestParser.getAviableHwCount()
	contests = list()
	for index in range(1, aviableContestsCount):
		contests.append(ContestParser.getHomework(index))
		print(f"Контест №{index} | {contests[-1][1]}")
	
	localId = int(input("Выберите контест: "))
	contest = Contest(contests[localId - 1][0])
	print(f"Контест №{localId} успешно выбран")
	with open("data.pkl", "wb") as f:
		pickle.dump(contest, f)

@click.command(name="select-task")
def selectTask():
	with open("data.pkl", "rb") as f:
		contest = pickle.load(f)
	contest.selectTask(int(input(f"Введите номер задачи: ")))
	print("Задача выбрана")
	with open("data.pkl", "wb") as f:
		pickle.dump(contest, f)
		

@click.command(name="show-cond")
def showTaskCond():
	with open("data.pkl", "rb") as f:
		contest = pickle.load(f)

	print(contest.task.getCondition())

@click.command(name="show-name")
def showTaskName():
	with open("data.pkl", "rb") as f:
		contest = pickle.load(f)

	print(contest.task.getName())

@click.command(name="send-task")
@click.argument("file", type=click.Path(exists=True))
def sendTask(file):
	with open("data.pkl", "rb") as f:
		contest = pickle.load(f)
	with open(file, "r") as file:
		contest.task.sendSolution(file.read())

@click.command(name="solution-status")
def getSolution():
	with open("data.pkl", "rb") as f:
		contest = pickle.load(f)
	print(contest.task.getStatus())


messages.add_command(selectContest)
messages.add_command(selectTask)
messages.add_command(showTaskCond)
messages.add_command(showTaskName)
messages.add_command(sendTask)
messages.add_command(getSolution)
