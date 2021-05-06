Перед использованием проекта выполнить обновление пакетов из requirements.txt

#Консольные команды:
1. python manage.py fill_db - 
   1.1 наполнение данными бд на основе json файлов в
   папке json корня проекта.
   1.2 Создание суперюзера Username: intergalactic Password: intergalactic
   1.3 Создание юзера Username: user2 Password: user2
   1.4 Создание юзера Username: user3 Password: user3
2. python manage.py fill_db_win - для Windows, 
   2.1 автоматизация удаления бд, 
   2.2 создания и выполнения миграций, 
   2.3 наполнение бд на основе созданного ранее fill_db

