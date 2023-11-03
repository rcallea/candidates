# Settings
```
python -m venv env
source env/Scripts/activate
pip install -r requirements.txt 
```

# Run
```
uvicorn src.application:app --reload
```

# Test
```
coverage run -m pytest
coverage report -m --fail-under=90
```

# Docker
```
docker build -t candidates:latest .
docker run -d --name candidates -p 80:8000 candidates:latest
```

# Resources
```
pip freeze > requirements.txt
kubectl get svc
```