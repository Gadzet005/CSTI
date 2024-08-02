import re

import requests
from bs4 import BeautifulSoup

from config import FIO_PATERN, HOME_URL
from src.consts import PARSER_TYPE, REQUEST_TIME_LIMIT
from src.contest.exceptions import CantParseElement


class ContestParser(object):
	@staticmethod
	def getSessionId(html: bytes) -> str:
		soup = BeautifulSoup(html, PARSER_TYPE)
		script = soup.find("script", string=re.compile("var SID="))
		if script is None:
			raise CantParseElement("script")
		
		sessionIdMatches = re.findall(r'var SID="(\w{16})"', script.text)
		if len(sessionIdMatches) != 1:
			raise CantParseElement("session id")
		
		return sessionIdMatches[0]
 
	# TODO: Падает на githubclassrom
	@staticmethod
	def getHomework(localContestId: int) -> tuple[int, map]:
		response = requests.get(HOME_URL, timeout=REQUEST_TIME_LIMIT)
		soup = BeautifulSoup(response.content, PARSER_TYPE)
		tabcontent = soup.find("div", id=f"block_hw{localContestId}")
		if tabcontent is None:
			raise CantParseElement("tabcontent") 
		
		contestButton = tabcontent.find("a", class_="button")
		if contestButton is None:
			raise CantParseElement("contestButton") 
		
		contestIdMatches = re.findall(r"Контест (\d{4})", contestButton.text)
		if contestIdMatches is None or len(contestIdMatches) != 1:
			raise CantParseElement("contestIdMatches") 

		contestId = int(contestIdMatches[0])

		homeworksMathes = tabcontent.find_all("td", string=re.compile(FIO_PATERN))
		if homeworksMathes is None or len(homeworksMathes) != 1:
			raise CantParseElement("homework")
		
		tasks = homeworksMathes[0].parent.find_all(string=re.compile(r"\d"))

		return (contestId, tasks)

	@staticmethod
	def getAviableHwCount() -> int:
		response = requests.get(HOME_URL, timeout=REQUEST_TIME_LIMIT)
		soup = BeautifulSoup(response.content, PARSER_TYPE)
		nav = soup.find("nav")
		if nav is None:
			raise CantParseElement("nav")

		hwContestButtons = nav.find_all("a", href=re.compile(r"#hw\d+"))
		if hwContestButtons is None:
			raise CantParseElement("hwContestButtons")

		return len(hwContestButtons)
