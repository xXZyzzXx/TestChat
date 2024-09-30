### Setup project

#### Environment
```bash
python -m venv venv

source venv/bin/activate
```

```bash
cp .env.template .env
```

```bash
pip install -r requirements.txt
```


#### Migrations

```bash
python manage.py migrate
```

#### Load test data

```bash
python manage.py loaddata initial_data.json
```

#### Run

```bash
python manage.py runserver
```


#### Testing

Superuser credentials:
```
Login: admin
Password: 123
```
