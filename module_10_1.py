'''
Задача "Потоковая запись в файлы":
Необходимо создать функцию write_words(word_count, file_name),
где word_count - количество записываемых слов,
file_name - название файла, куда будут записываться слова.

Функция должна вести запись слов "Какое-то слово № <номер слова по порядку>" в соответствующий файл
с прерыванием после записи каждого на 0.1 секунду.

Сделать паузу можно при помощи функции sleep из модуля time, предварительно импортировав её: from time import sleep.
В конце работы функции вывести строку "Завершилась запись в файл <название файла>".

После создания файла вызовите 4 раза функцию wite_words, передав в неё следующие значения:
10, example1.txt
30, example2.txt
200, example3.txt
100, example4.txt
После вызовов функций создайте 4 потока для вызова этой функции со следующими аргументами для функции:
10, example5.txt
30, example6.txt
200, example7.txt
100, example8.txt
Запустите эти потоки методом start не забыв, сделать остановку основного потока при помощи join.
Также измерьте время затраченное на выполнение функций и потоков. Как это сделать рассказано в лекции к домашнему заданию.
'''


from time import sleep
from threading import Thread
import time


def write_words(word_count, file_name):
    with open(file_name, 'w', encoding='UTF-8') as file:
        for i in range(1, word_count + 1):
            file.write(f'Какое-то слово № {i}\n')
            sleep(0.1)
    print(f'Завершилась запись в файл {file_name}')

#  Пример использования функции write_words
write_words(10, 'example1.txt')
write_words(30, 'example2.txt')
write_words(200, 'example3.txt')
write_words(100, 'example4.txt')

print('----------------------------------')
#  время начала выполнения программы
start = time.time()
threads = []

# текущее время с начала суток в часах
print('Запуск потоков', time.strftime('%H:%M:%S', time.localtime(start)))

#  Пример использования потоков
for i in [(10, 'example5.txt'),
          (30, 'example6.txt'),
          (200, 'example7.txt'),
          (100, 'example8.txt')
          ]:
    thread = Thread(target=write_words, args=i)
    threads.append(thread)
    thread.start()
    thread.join()
    end = time.time()
    print(f'Время выполнения: {end - start}')

#   время завершения выполнения потоков
end = time.time()

print('----------------------------------')
# текущее время с начала суток в часах
print('Завершение потоков', time.strftime('%H:%M:%S', time.localtime(start)))
print(f'Общее время выполнения: {end - start}')