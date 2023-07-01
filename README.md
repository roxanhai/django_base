# DRF Base

------------------

## Usage

---

### Run for dev

- install requirements

```
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt 
```

- Run server

```
python3 manage.py runserver
```

- Migrate and Migrations (After changing Orm Model)

```
python3 manage.py makemigrations
python3 manage.py migrate
```

- Check Swagger docs:
```
http://127.0.0.1:8000/swagger
```
