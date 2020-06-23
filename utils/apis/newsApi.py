

#http://newsapi.org/v2/top-headlines?country=in&apiKey=e603267fd53c406cb4d230e6deac25d1
#http://newsapi.org/v2/top-headlines?q=trump&country=in&apiKey=e603267fd53c406cb4d230e6deac25d1
from utils.apis.requestUrl import RequestUrl
from model.models import News
from typing import List

class NewsApi(RequestUrl):

	"""
	NewsApi child class from RequestUrl Class:
	NewsApi api to fetch and search news article from newsapi using  get Request

	...

	Attributes
	----------
		news_url : str
			url to fetch news from newsapi
		apiKey : str
	   Api key to authenticate on newsapi serevr

	Methods
	-------
		getNews()
		searchNews()
		getAllNews()
	"""

	news_url = "http://newsapi.org/v2/top-headlines"
	apiKey = "e603267fd53c406cb4d230e6deac25d1"

	# instance attribute
	def __init__(self):
		pass

	@classmethod
	async def getNews(self)-> dict:
		"""Get all news for country india and return Json
		Parameters
		----------
		"""
		return await self.getAsJson(self.news_url, {"apiKey"  :self.apiKey, "country" : "in" , "pageSize" : 38 })

	@classmethod
	async def searchNews(self, q:str= None)-> dict:
		"""Get all news with query q and return Json
		Parameters
		----------
		q : str
			Search keywork for news
		"""
		return await self.getAsJson(self.news_url, {"apiKey"  :self.apiKey, "country" : "in", "q"  : q, "pageSize" : 38 })


	@classmethod
	async def getAllNews(self, q:str  = None)-> List[News]:
		""" All News wrapper for getNews and searchNews. return list of News Model generated from returned json data
		Parameters
		----------
		q : str, optional
			Search keywork for news
		"""
		
		if q is not None:
			allNews =  await self.searchNews(q)
		else:
			allNews =  await self.getNews()
		response = []
		if allNews is not None:
			response = [News(headline=news['title'], link=news['url'], source= "newsapi") for news in allNews['articles']]
		return response