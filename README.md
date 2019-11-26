# Memelicious

Django based application to fetch latest videos with YouTube API, save it to database and expose an API to display all the videos from the database.


# Installation

The steps below are for debian family only. You may use equivalant steps for other systems.

Pre-requisites:

- Python 3.6+
- pip
- git

1. Clone the repository and go to the repository folder:

```bash
$ git clone git@github.com:ShraddhaAg/memelicious.git 'memelicious'
$ cd memelicious/
```

2. Create a virtual environment and activate it.

```bash
$ virtualenv venv
$ source venv/bin/activate
```

3. Install project requirements:

```bash
$ pip install -r requirements.txt
```
Install `redis-server` using [this](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04) helpful guide.

Note: Please make sure `redis-server` is running, refer documentation [here](https://redis.io/topics/quickstart#check-if-redis-is-working).

4. Setup YouTube API key: Checkout the `config.yml.example` in *memelicious* directory of the repository and create `config.yml` with your YouTube API key(s).

5. Setup database:

```
$ cd memelicious/
$ python manage.py migrate
$ python manage.py createsuperuser
```

# Usage


- Run server: `python manage.py runserver`
- Run celery-beat in a different terminal inside the *memelicious* directory (also has *manage.py*): `celery worker -A memelicious -B --loglevel=info`

Navigate to [localhost:8000](http://localhost:8000/app/list/?page=1). To view pagination, change the value of the query `page` in the URL.

