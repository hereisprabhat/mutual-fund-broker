# Mutual Fund Broker API

## Description
The project contains data Mutual Fund Broker APIs by means
of FastAPI.


## Dependencies
The project uses:
1. **FastAPI** - API web framework;

All used packages are listed in [requirements.txt](requirements.txt).


### Virtual environment
Command to build virtual environment under project root, it helps  isolate the project from 
other developments so there are no dependencies collisions:
```bash
python3 -m venv venv/
```

Activate virtual environment:
```bash
source venv/bin/activate
```

Command to install all dependencies from created virtual environment:
```bash
pip3 install -r requirements.txt
```

Command to run service:
```bash
uvicorn app.main:app
```
Or
```bash
uvicorn app.main:app --reload
```

More details on uvicorn - [read more](https://www.uvicorn.org) 


To see all the configurations and options, go to the Docker image page: 
[uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)


Points to be noted:
1. Made for local running, just update the credentials in env file and start using the API on local via the above given commands.
