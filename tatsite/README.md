Устанавливаем монгу:
sudo apt-get install mongodb-clients
sudo apt-get install mongodb-server
sudo apt-get install g++
sudo pip install pymongo

Ставим библиотеки для парсера:
sudo pip install html5lib
sudo pip install requests
sudo apt-get install libxml2-dev
sudo apt-get install libxslt1-dev
sudo apt-get install python-dev
sudo pip install lxml

Запускаем парсер: python server/clients/fetch.py

Ставим зависимости для nodejs
cd server
npm i

Запускаем node app.js
http://localhost:8007/client/

Так как база обновляется слишком долго, то можно посмотреть результат отсюда:
http://tat.people.yandex.net/client/