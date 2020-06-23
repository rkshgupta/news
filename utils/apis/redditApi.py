from utils.apis.requestUrl import RequestUrl
from model.models import News
from typing import List

class RedditApi(RequestUrl):
	"""
	RedditApi child class from RequestUrl Class:
	Reddit api to fetch and search post from subreddit using  get Request

	...

	Attributes
	----------
	news_url : str
		url to fetch news from subreddit's hot section
	search_url : str
		url to search news from subreddit

	Methods
	-------
	getNews()
	searchNews()
	getAllNews()
	"""
	news_url = "https://www.reddit.com/r/news/hot/.json"
	search_url = "https://www.reddit.com/r/news/search/.json?"

	@classmethod
	async def getNews(self)-> dict:
		"""Get all news from subreddit news hot section with limit of 100 articles and return Json
		Parameters
		----------
		"""

		return await self.getAsJson(self.news_url, {"limit"  :100 })

	@classmethod
	async def searchNews(self, q:str= None)-> dict:
		"""Search news from subreddit news hot section and return Json
		Parameters
		----------
		q : str
			Search keywork for news
		"""
		return await self.getAsJson(self.search_url, {"q"  : q, "restrict_sr" : 1, "sort" : "hot" })

	@classmethod
	async def getAllNews(self, q:str  = None)-> List[News]:
		""" All News wrapper for getNews and searchNews. return list of News Model generated from returned json data
		Parameters
		----------
		q : str, optional
			Search keywork for news
		"""


		if q is not None:
			allNews = await self.searchNews(q)
		else:
			allNews =  await self.getNews()
		response = []
		if allNews is not None:
			response = [News(headline =news['data']['title'], link =news['data']['url'], source = "reddit") for news in allNews['data']['children']]
		return response

