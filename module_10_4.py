'''
Задача "Потоки гостей в кафе":
Необходимо имитировать ситуацию с посещением гостями кафе.
Создайте 3 класса: Table, Guest и Cafe.
Класс Table:
Объекты этого класса должны создаваться следующим способом - Table(1)
Обладать атрибутами number - номер стола и guest - гость, который сидит за этим столом (по умолчанию None)
Класс Guest:
Должен наследоваться от класса Thread (быть потоком).
Объекты этого класса должны создаваться следующим способом - Guest('Vasya').
Обладать атрибутом name - имя гостя.
Обладать методом run, где происходит ожидание случайным образом от 3 до 10 секунд.
Класс Cafe:
Объекты этого класса должны создаваться следующим способом - Cafe(Table(1), Table(2),....)
Обладать атрибутами queue - очередь (объект класса Queue) и tables - столы в этом кафе (любая коллекция).
Обладать методами guest_arrival (прибытие гостей) и discuss_guests (обслужить гостей).
Метод guest_arrival(self, *guests):
Должен принимать неограниченное кол-во гостей (объектов класса Guest).
Далее, если есть свободный стол, то садить гостя за стол (назначать столу guest),
 запускать поток гостя и выводить на экран строку "<имя гостя> сел(-а) за стол номер <номер стола>".
Если же свободных столов для посадки не осталось,
 то помещать гостя в очередь queue и выводить сообщение "<имя гостя> в очереди".
Метод discuss_guests(self):
Этот метод имитирует процесс обслуживания гостей.
Обслуживание должно происходить пока очередь не пустая (метод empty) или хотя бы один стол занят.
Если за столом есть гость(поток) и гость(поток) закончил приём пищи(поток завершил работу - метод is_alive),
 то вывести строки "<имя гостя за текущим столом> покушал(-а) и ушёл(ушла)" и "Стол номер <номер стола> свободен".
  Так же текущий стол освобождается (table.guest = None).
Если очередь ещё не пуста (метод empty) и стол один из столов освободился (None),
 то текущему столу присваивается гость взятый из очереди (queue.get()).
 Далее выводится строка "<имя гостя из очереди> вышел(-ла) из очереди и сел(-а) за стол номер <номер стола>"
Далее запустить поток этого гостя (start)
Таким образом мы получаем 3 класса на основе которых имитируется работа кафе:
Table - стол, хранит информацию о находящемся за ним гостем (Guest).
Guest - гость, поток, при запуске которого происходит задержка от 3 до 10 секунд.
Cafe - кафе, в котором есть определённое кол-во столов и происходит имитация прибытия гостей (guest_arrival) и их обслуживания (discuss_guests).
'''


from threading import Thread
from queue import Queue
from random import randint, choice
from time import sleep


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))



class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)
        self.running_guests = []

    def guest_arrival(self, *guests):
        '''
        1. Прибытие гостей
        2. Рассадка гостей за столы
        3. Формирование очереди ожидания
        '''
        print('---------------------------')
        print('Прибытие гостей')
        print('Рассадка гостей за столы')
        print('Формирование очереди ожидания')
        print('---------------------------')
        print()
        for guest in guests:
            free_table = next((table for table in self.tables if table.guest is None), None)
            if free_table:
                free_table.guest = guest
                print(f'{guest.name} сел(-а) за стол номер {free_table.number}')
                guest.start()
                self.running_guests.append(guest)
            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')
        for guest in self.running_guests:
            guest.join()

    def discuss_guests(self):
        '''
        1. Обслуживание гостей
        2. Провод сытых гостей
        3. Обслуживание очереди
        '''
        print()
        print('---------------------------')
        print('Начало обслуживания')
        print('---------------------------')
        print()

        while any(table.guest for table in self.tables) or not self.queue.empty():
            for table in self.tables:
                if table.guest and not table.guest.is_alive():
                    guest = table.guest
                    table.guest = None
                    print(f'{guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')

                if not self.queue.empty():
                    table = next((table for table in self.tables if table.guest is None), None)
                    if table:
                        guest = self.queue.get()
                        table.guest = guest
                        print(f'{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                        guest.start()
                        guest.join()


# Создание столов
tables = [Table(number) for number in range(1, 4)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()

