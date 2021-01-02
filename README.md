# Django DRF starter pack

Clone using git

```bash
git clone https://github.com/scasolari/Django-DRF-starter-pack.git
```

## Installation

Use the file requirements.txt to install all the packages.

```bash
pip install requirements.txt 
```

## Usage

Run in order:
* `python3 -m venv venv`
* `source venv/bin/activate`
* `python manage.py migrate`
* `python manage.py runserver`
* `python manage.py createsuperuser`

Type ```127.0.0.1:8000/admin``` in your browser to access to your admin dashboard.
<br/>
Type ```127.0.0.1:8000/api``` in your browser to have the entire list of the API endpoint.