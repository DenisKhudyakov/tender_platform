<h1 align="center">Development by <a href="https://github.com/DenisKhudyakov/drf_course_paper" target="_blank">Denis Khudyakov</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>


![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

<h3>Тендерная площадка</h3>
<p>Разработано специально для компании ООО "ЧЗМЭК"</p>




	Установка и запуск:
		1) Установите Python и Poetry если они не установлены.
		2) Клонируйте репозиторий git clone https://github.com/DenisKhudyakov/tender_platform.git
		3) Установаите Docker и Docker Desktop
        4) Запустите в директории проекта команду docker compose up --build

<h2>Руководство пользователя.</h2>

<h3>Для поставщиков:</h3>

Для начала пользования зарегистрируйтесь на площадке
![img.png](scrins/img.png) 

Для Сотрудников только электронная почта и пароль<br>
Для Поставщиков при регистрации заполняются все поля 

![img.png](scrins/Регистрация.png)

После успешной регистрации, вас попросят ввести ваш логин пароль для авторизации.<br>
Вы их вводите и попадаете на Страницу со списком заявок для поставщиков.<br>

На главной странице список заявок, в каждую заявку можно перейти и посмотреть список товаров в ней
![img.png](scrins/order_product_list.png)
![img.png](scrins/order_product_detail.png)

Вы можете ответить на эту заявку, если вы ранее уже отвечали, то программа предложит Вам обновить ответ на заявку.

![img.png](scrins/answer_order_product.png)
![img.png](scrins/update_order_product_answer.png)

Ответ на заявку:
![img.png](scrins/answer.png)
Если Поставщик не может дать предложение на какой-либо товар, необходимо оставить значение поля нулевым.

Обновление:
![img.png](scrins/update.png)

<h3>Для Сотрудников:</h3>

После регистрации и авторизации обратитесь к администратору.

Он проставит признак, что Пользователь является сотрудником и для Вас проявится дополнительный интерфейс
![img.png](scrins/admin.png)

Вы сможете создавать товары, при необходимости:

![img.png](scrins/add_product.png)

Создавать заявку.<br>
Так же реализовано API создания заявки из 1С, которая будет сразу же наполнена необходимыми товарами.

![img.png](scrins/add_order.png)

**Тестовые данные для создания заявки из 1С**
```angular2html

    {
    "products": [
        {"article": "12345", "name": "Product A", "measurement": "шт"},
        {"article": "67890", "name": "Product B", "measurement": "кг"}
    ],
    "amounts": [10, 20],
    "number_ERP": "ERP12345",
    "description": "Закупка товаров для проекта",
    "duration": "2024-12-31",
    }
```

Интерфейс Сотрудника:

![img.png](scrins/order_list.png)

При переходе в какую либо заявку, Сотрудник может добавить товары в заказ, при необходимости,<br>
Просмотреть анализ цен, и обновить данные по заявке, например увеличить срок ответа или сделать её НЕ актуальной.

![img.png](scrins/order_detail.png)

Обновление заявки:

![img.png](scrins/update_order.png)


Анализ цен, в котором выгружены все ответы поставщиков по каждому товару, наиболее низкая цена за конкретный товар выделена зеленым.
Группировка в таблице по товарам. Для удобства реализован фильтр по конкретному товару в этой заявке.

![img.png](scrins/price_analys.png)

Работа фильтра. Если значение товара от поставщика нулевое, значит он не ответил на этот товар(нет вналичии и т.п.)

![img.png](scrins/filter_price_analysis.png)
		