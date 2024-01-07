Проект DjangoStripe
Описание
Django Модель Item с полями (name, description, price) API с двумя методами:

GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и полученный session.id выдаваться в результате запроса
GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее с помощью JS библиотеки Stripe происходить редирект на Checkout форму stripe.redirectToCheckout(sessionId=session_id)
Бонусные задачи:
☑ Запуск используя Docker

☑ Использование environment variables

☑ Просмотр Django Моделей в Django Admin панели

☑ Запуск приложения на удаленном сервере, доступном для тестирования

☑ Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items

☑ Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме.

☑ Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте (скорее попытка костыля)))

☑ Реализовать не Stripe Session, а Stripe Payment Intent.

Чтобы развернуть проект локально:
склонировать репозиторий
в папке infr задать переменные окружения в файле .env
SECRET_KEY = 'Место для секретного ключа'

STRIPE_PUBLIC_KEY = 'Публичный API key Stripe' 
STRIPE_SECRET_KEY = 'Секретный API key Stripe'

ALLOWED_HOSTS = 'Используемые хосты'
 
DEBUG=int

POSTGRES_DB='Имя БД'
POSTGRES_USER='Пользователь БД'
POSTGRES_PASSWORD='Пароль от БД'
POSTGRES_HOST=db
POSTGRES_PORT=5432
Далее:

docker-compose up -d --build
Выполняем миграции:
docker exec djangostripe_web-app_1 python manage.py makemigrations
docker exec djangostripe_web-app_1 python manage.py migrate --noinput
Создайте суперюзера :
docker exec -it djangostripe_web-app_1 python manage.py createsuperuser
