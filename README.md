Swagger Link: https://news-feed-new.herokuapp.com/swagger/


Base Url: https://news-feed-new.herokuapp.com/api/

Git Repository Link: https://github.com/Abhijitkulkarni18/news

Postman Collection APIs: 

Postman Documentation link: https://documenter.getpostman.com/view/7497641/T17AiAQ8

Postman Collection link : https://www.getpostman.com/collections/db17cccf482c1b3827a7


Django Set-Up:

pip3 install -r requirements.txt

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py runserver

Django Admin Credentials and URL:

URL: https://news-feed-new.herokuapp.com/admin/

username:abhijit

password:password


Loading Initial data:

python3 manage.py loaddata category_data.json

Loading Category data in Heroku:

heroku run python3 manage.py loaddata category_data.json


For more info about me, please visit: https://abhijitkulkarni.herokuapp.com/ 