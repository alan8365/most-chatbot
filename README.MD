flask run

```shell=
flask run --reload --debugger --host 0.0.0.0 --port 80
```

rasa run
```shell=
rasa run --model .\models\shou\20220903-212104.tar.gz
```

post to http://localhost:5005/webhooks/rest/webhook
format: {"sender": "Lucy", "message": "老人照護"}