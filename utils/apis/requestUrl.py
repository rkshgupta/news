import aiohttp, json
from aiohttp import ClientError
from abc import ABC, abstractmethod 

class RequestUrl:
	__header = {}
	__params = None
	__contentType  = "content-type"
	__json  = "application/json;charset=utf-8"
	__urlencode  = "application/x-www-form-urlencoded;charset=utf-8"
	__session = aiohttp.ClientSession()

	@classmethod
	async def getAsJson(self, url: str = None, params: dict = None,  header: dict = None) -> dict:
		"""" Creates and returns a GET request and return Json and set default Json content type header when None
		Parameters
		----------
		url : str
			Api Url for get request
		params : dict, optional
			Parameterskey values fetch api url data
		header : dict, optional
			Header key values to fetch api url data

		Raises
		------
		ClientError
			 if there is some problem fetching completing the get request.
		"""

		self.__header.update({
			'User-agent': 'News Aggregator V2'
			})
		self.__header.update({self.__contentType : self.__json})

		if header is not None:
			self.__header.update(header)

		if params is not None:
			self.__params = params
		if url is not None:
			async with self.__session.get(url,  params = params, headers = header) as resp:
				try:
					if resp.status == 200:
						r = json.loads(await resp.read())
						return r
				except ClientError as e:
					return None


		return None

	@abstractmethod
	def getNews(self):
		pass

	@abstractmethod
	def searchNews(self):
		pass

	@abstractmethod
	def getAllNews(self):
		pass