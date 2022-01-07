# Публикуйте комиксы во Вконтакте

Программа для публикации комиксов с сайта [https://xkcd.com/](https://xkcd.com/) в группу социальной сети [ВКонтакте](https://vk.com).

### Как установить

Python3 должен быть уже установлен.

Затем используйте [виртуальное окружение](https://docs.python.org/3/library/venv.html) и `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Для запуска приложения

1. Прописать значения для всех необходимых переменных в файле .env, названия переменных уже добавлены.
   1. ACCESS_TOKEN - токен доступа. Как получить см. [здесь](https://dev.vk.com/api/access-token/implicit-flow-user).
   2. CLIENT_ID - это идентификатор вашего приложения. Создать приложение можно [здесь](https://vk.com/apps?act=manage).
   3. GROUP_ID - это идентификатор вашей созданной группы, его можно получить в адресной строке открытой страницы группы. Как создать группу смотри [здесь](https://vk.com/biz/article/sozdanie-vybor-tipa-i-tematiki).
2. Как правильно заполнить и для чего нужен файл .env написано [здесь](https://pypi.org/project/python-dotenv/0.9.1/#usages)
3. Подготовить [группу](https://vk.com/groups) и [приложение](https://vk.com/apps?act=manage) по [документации](https://vk.com/dev)

### Запуск приложения

Для того чтобы разместить в группе случайный комикс нужно выполнить.

```
python app.py
```
