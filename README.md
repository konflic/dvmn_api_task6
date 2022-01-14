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
   1. VK_ACCESS_TOKEN - токен доступа. Как получить см. [здесь](https://dev.vk.com/api/access-token/implicit-flow-user). Для работы с приложением нужно будет выбрать [scope](https://dev.vk.com/reference/access-rights) wall, group и photos.
   2. VK_GROUP_ID - это идентификатор вашей созданной группы, его можно получить в адресной строке открытой страницы группы. 
   3. Как создать группу смотри, например, [здесь](https://vk.com/biz/article/sozdanie-vybor-tipa-i-tematiki).
2. Как правильно заполнить и для чего нужен файл .env написано [здесь](https://pypi.org/project/python-dotenv/0.9.1/#usages)
3. Создать [группу](https://vk.com/groups) и [приложение](https://vk.com/apps?act=manage).
4. В [настройках vk-приложения](https://vk.com/apps?act=manage), выбрать "Редактировать", перейти в настройки и выбрать состояние "Приложение включено и видно всем"

### Запуск

Для того чтобы разместить в группе случайный комикс нужно выполнить.

```
python app.py
```
