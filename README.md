Install the dependencies and start the server.

```sh
$ pip install -r requirement.txt
````
Once installation is complete run 
```sh
$ uvicorn news:app --reload
```
To fetch news authenticate using 
# Username : admin, Password : abc123
Verify the deployment by navigating to your server address in your preferred browser or postman.
```sh
127.0.0.1:8000
```
and Search news 
```sh
127.0.0.1:8000/?query=modi
```

*if you are using postman, click on 'Authorization' and select 'Basic Auth' enter username and password.
