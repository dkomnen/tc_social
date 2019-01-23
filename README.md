# tc_social

**Setup**

Install postgres using docker

`docker run --name postgres-db -p 5432:5432 -e POSTGRES_PASSWORD=insert_your_password -d postgres`

Enter the container

`docker exec -it postgres-db bash`

Log in to postgres

`psql -U postgres -W`

Create database named "tsoc"

`CREATE DATABASE tsoc;`

Copy your postgres credentials to settings.py in tc_social/tsoc/settings.py

```json
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tsoc',
        'USER': 'postgres',
        'PASSWORD': 'your-postgres-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Run the server

`python manage.py runserver`

**Auto generator script**

Put list of emails into predefined_emails.json

If you don't want to use predefined emails, and want them to be randomly generated, set
`use_predefined_emails = True` in bot_config.ini and disable emailhunter and clearbit in settings.py with `CLEARBIT_ACTIVE = False,
HUNTER_ACTIVE = False`

Run the auto generator bot

`python run.py --config=bot_config.ini`

Output

```text
-----------CREATED USERS---------------
Email: billgates1@gmail.com, Password: , First Name: , Last Name:
Email: ronswanson1@gmail.com, Password: , First Name: , Last Name:
Email: timcook@gmail.com, Password: , First Name: , Last Name:
Email: benbenson1@gmail.com, Password: , First Name: , Last Name:
Email: johnjohnson1@gmail.com, Password: , First Name: , Last Name:
-----------CREATED POSTS---------------
Post text: This is a test post!, Poster ID: 100
Post text: This is a test post!, Poster ID: 100
Post text: This is a test post!, Poster ID: 100
Post text: This is a test post!, Poster ID: 100
Post text: This is a test post!, Poster ID: 100
Post text: This is a test post!, Poster ID: 100
Post text: This is a test post!, Poster ID: 100
Post text: This is a test post!, Poster ID: 100
Post text: This is a test post!, Poster ID: 100
Post text: This is a test post!, Poster ID: 101
Post text: This is a test post!, Poster ID: 101
Post text: This is a test post!, Poster ID: 101
Post text: This is a test post!, Poster ID: 103
Post text: This is a test post!, Poster ID: 103
-----------USER POST LIKES---------------
Post with id: 309, was liked by User with id: 103
Post with id: 314, was liked by User with id: 103
Post with id: 312, was liked by User with id: 101
Post with id: 310, was liked by User with id: 101
Post with id: 313, was liked by User with id: 101
```