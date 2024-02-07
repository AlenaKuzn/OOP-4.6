#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import date
import sys
from typing import List
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class re:
   pynkt: str
   numb: int
   samolet: str


@dataclass
class Staff:
   reys: List[re] = field(default_factory=lambda: [])
   def add(self, pynkt, numb, samolet):
       self.reys.append(
           re(
               pynkt=pynkt,
               numb=numb,
               samolet=samolet
          )
      )
       self.reys.sort(key=lambda re: re.pynkt)


   def __str__(self):
       # Заголовок таблицы.
       table = []
       line = '+-{}-+-{}-+-{}-+-{}-+'.format(
           '-' * 4,
           '-' * 30,
           '-' * 20,
           '-' * 8
       )
       table.append(line)
       table.append(
           '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
               "№",
               "Пункт",
               "Номер рейса",
               "Самолет"
           )
       )
       table.append(line)

       # Вывести данные о всех сотрудниках.
       for idx, re in enumerate(self.reys, 1):
           table.append(
               '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                   idx,
                   re.pynkt,
                   re.numb,
                   re.samolet
               )
           )

       table.append(line)
       return '\n'.join(table)


   def select(self, period):
       result = []
       for employee in self.reys:
            if employee.get('pynkt') == pynkt_pr:
                result.append(employee)

       return result


   def load(self, filename):
       with open(filename, 'r', encoding='utf8') as fin:
           xml = fin.read()
       parser = ET.XMLParser(encoding="utf8")
       tree = ET.fromstring(xml, parser=parser)

       self.reys = []
       for re_element in tree:
           pynkt, numb, samolet = None, None, None
           for element in re_element:
               if element.tag == 'pynkt':
                   pynkt = element.text
               elif element.tag == 'numb':
                   numb = element.text
               elif element.tag == 'samolet':
                   samolet = int(element.text)


   def save(self, filename):
       root = ET.Element('reys')
       for re in self.reys:
           reys_element = ET.Element('reys')

           pynkt_element = ET.SubElement(reys_element, 'pynkt')
           pynkt_element.text = re.pynkt

           numb_element = ET.SubElement(reys_element, 'numb')
           numb_element.text = str(re.numb)

           samolet_element = ET.SubElement(reys_element, 'samolet')
           samolet_element.text = re.samolet

           root.append(reys_element)

       tree = ET.ElementTree(root)

       with open(filename, 'wb') as fout:
           tree.write(fout, encoding='utf8', xml_declaration=True)


if __name__ == '__main__':
   # Список работников.
   staff = Staff()

   # Организовать бесконечный цикл запроса команд.
   while True:
           # Запросить команду из терминала.
           command = input(">>> ").lower()
           # Выполнить действие в соответствие с командой.
           if command == 'exit':
               break

           elif command == 'add':
               # Запросить данные о работнике.
               pynkt = input("Пункт назвачения: ")
               numb = int(input("Номер рейса: "))
               samolet = input("Тип самолета ")
               # Добавить работника.

               staff.add(pynkt, numb, samolet)

           elif command == 'list':
               # Вывести список.
               print(staff)

           elif command.startswith('select '):
               # Разбить команду на части для выделения номера года.
               parts = command.split(maxsplit=1)
               # Запросить работников.
               selected = staff.select(parts[1])

               # Вывести результаты запроса.
               if selected:
                   for idx, re in enumerate(selected, 1):
                       print(
                           '{:>4}: {}'.format(idx, re.pynkt)
                       )
               else:
                   print("Работники с заданным стажем не найдены.")

           elif command.startswith('load '):
                # Разбить команду на части для имени файла.
                parts = command.split(maxsplit=1)
                # Загрузить данные из файла.
                staff.load(parts[1])

           elif command.startswith('save '):
                # Разбить команду на части для имени файла.
                parts = command.split(maxsplit=1)
                # Сохранить данные в файл.
                staff.save(parts[1])

           elif command == 'help':
                # Вывести справку о работе с программой.
                print("Список команд:\n")
                print("add - добавить данные о рейсе;")
                print("list - вывести список рейсов;")
                print("select <стаж> - запросить работников со стажем;")
                print("load <имя_файла> - загрузить данные из файла;")
                print("save <имя_файла> - сохранить данные в файл;")
                print("help - отобразить справку;")
                print("exit - завершить работу с программой.")

           else:
                print(f"Неизвестная команда {command}", file=sys.stderr)
