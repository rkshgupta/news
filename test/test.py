from fastapi.testclient import TestClient
from news import app
import base64


client = TestClient(app)


def test_no_auth():
	response = client.get("/")
	assert response.status_code == 401

def test_wrong_auth():
	response = client.get("/", headers={'Authorization': 'Basic ' + base64.b64encode(bytes("Admin" + ":" + "abc123", 'ascii')).decode('ascii')})
	assert response.status_code == 401

def test_auth():
	response = client.get("/", headers={'Authorization': 'Basic ' + base64.b64encode(bytes("admin" + ":" + "abc123", 'ascii')).decode('ascii')})
	assert response.status_code == 200

def test_data():
	response = client.get("/", headers={'Authorization': 'Basic ' + base64.b64encode(bytes("admin" + ":" + "abc123", 'ascii')).decode('ascii')})
	assert response.status_code == 200
	assert len(response.json()) == 138

def test_data_news():
	response = client.get("/", headers={'Authorization': 'Basic ' + base64.b64encode(bytes("admin" + ":" + "abc123", 'ascii')).decode('ascii'), 'Content-Type': 'application/json'})
	assert response.status_code == 200
	assert len([news for news in response.json() if news['source'] == "newsapi"]) == 38

def test_data_reddit():
	response = client.get("/", headers={'Authorization': 'Basic ' + base64.b64encode(bytes("admin" + ":" + "abc123", 'ascii')).decode('ascii'), 'Content-Type': 'application/json'})
	assert response.status_code == 200
	assert len([news for news in response.json() if news['source'] == "reddit"]) == 100


##Query news Test

def test_data_query_no_auth():
	response = client.get("/", params ={"query" : "modi"})
	assert response.status_code == 401

def test_data_query_wrong_auth():
	response = client.get("/", params ={"query" : "modi"}, headers={'Authorization': 'Basic ' + base64.b64encode(bytes("Admin" + ":" + "abc123", 'ascii')).decode('ascii')})
	assert response.status_code == 401

def test_data_query_reddit():
	response = client.get("/", params ={"query" : "reddit"},headers={'Authorization': 'Basic ' + base64.b64encode(bytes("admin" + ":" + "abc123", 'ascii')).decode('ascii'), 'Content-Type': 'application/json'})
	assert response.status_code == 200
	assert len([news for news in response.json() if news['source'] == "newsapi"]) == 0

def test_data_query():
	response = client.get("/", params ={"query" : "modi"},headers={'Authorization': 'Basic ' + base64.b64encode(bytes("admin" + ":" + "abc123", 'ascii')).decode('ascii'), 'Content-Type': 'application/json'})
	assert response.status_code == 200
	assert len(response.json()) > 0 

## Wrogn query params

def test_data_wrongquery_no_auth():
	response = client.get("/", params ={"query" : "modi"})
	assert response.status_code == 401

def test_data_wrongquery_wrong_auth():
	response = client.get("/", params ={"query" : "modi"}, headers={'Authorization': 'Basic ' + base64.b64encode(bytes("Admin" + ":" + "abc123", 'ascii')).decode('ascii')})
	assert response.status_code == 401

def test_data_wrongquery_reditText():
	response = client.get("/", params ={"q" : "reddit"},headers={'Authorization': 'Basic ' + base64.b64encode(bytes("admin" + ":" + "abc123", 'ascii')).decode('ascii'), 'Content-Type': 'application/json'})
	assert response.status_code == 200
	assert len([news for news in response.json() if news['source'] == "newsapi"]) == 38

def test_data_wrongquery_newsapiText():
	response = client.get("/", params ={"q" : "newsapi"},headers={'Authorization': 'Basic ' + base64.b64encode(bytes("admin" + ":" + "abc123", 'ascii')).decode('ascii'), 'Content-Type': 'application/json'})
	assert response.status_code == 200
	assert len([news for news in response.json() if news['source'] == "reddit"]) == 100

def test_data_wrongquery():
	response = client.get("/", params ={"q" : "modi"},headers={'Authorization': 'Basic ' + base64.b64encode(bytes("admin" + ":" + "abc123", 'ascii')).decode('ascii'), 'Content-Type': 'application/json'})
	assert response.status_code == 200
	assert len(response.json()) == 138 
