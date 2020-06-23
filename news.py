import secrets, asyncio
from fastapi import FastAPI, Depends, HTTPException
from utils.apis.redditApi import RedditApi
from utils.apis.newsApi import NewsApi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import List
from model.models import News


app = FastAPI()
security = HTTPBasic()

""" Fake Db to authenticate users and password from request
"""
demoDb = {
    "Aladdin" : "password", #password
    "admin" : "abc123", #abc123
    "RaKesh" : "pass@123", #pass@123
}


def auth_user(credentials: HTTPBasicCredentials = Depends(security)):
	"""" Authenticate request with user and password from demoDb and use "compare_digest" to prevent time attack on username/password guessing
		TODO: store hashed password in actual db generated with bcypt and salt(12) which will help keeping the password secure.
    Parameters
    ----------
    credentials : HTTPBasicCredentials
    	Authenticate : Basic with username:password encoded in base64

    Raises
    ------
    HTTPException
        If request is un unauthorized
    """
	if credentials.username in demoDb:
		password = demoDb[credentials.username]
		correct_password = secrets.compare_digest(credentials.password, password) #hashed pass saved in db
		if(correct_password):
			return credentials
	raise HTTPException(
					status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated", headers={"WWW-Authenticate": "Basic"}
				)
	return None

@app.get("/", response_model=List[News])
async def read_root(query:str = None, auth:HTTPBasicCredentials = Depends(auth_user))-> List[News]:
	"""" Creates and returns a GET request and return Json
    Parameters
    ----------
    query : str, optional
    	Api Url for get request
    auth : str
    	Api Url for get request

    Raises
    ------
    Exception
         if there is some problem in async Coroutines get request.
    """
	if not auth:
		response = Response(
                    status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated", headers={"WWW-Authenticate": "Basic"}
                )
		return response
	r = await getAllNews(query)
	return r

async def getAllNews(q:str = None)-> List[News]:
	"""" Creates and returns a GET request and return list of News Model
    Parameters
    ----------
    q : str, optional
    	Api Url for get request

    Raises
    ------
    Exception
         if there is some problem in async Coroutines get request.
    """
	
	r = []
	try:
		[r.extend(item) for item in await asyncio.gather(*[RedditApi.getAllNews(q), NewsApi.getAllNews(q)])]
	except Exception as e:
		pass
	return r

