# student-ml-api

Minimal ML inference service used to demonstrate a professional CI/CD workflow
(feature branches → Pull Requests → CI → merge → semantic tag → release workflow → GHCR).

## Run locally
```bash
pip install -r requirements.txt
python app.py
curl http://localhost:5000/health
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"value": 10}'
```

## Test
```bash
pytest -v
```

## Docker
```bash
docker build -t student-ml-api:$(cat VERSION) .
docker run -d --name student-ml-api -p 5000:5000 student-ml-api:$(cat VERSION)
```
