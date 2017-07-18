# -*- coding: utf-8 -*-
import time
from tornado.ioloop import IOLoop
from tornado import gen
 
def my_function(callback):
  print('do some work')
  # Эта строчка блокирует выполнение
  time.sleep(1)
  callback(123)
 
@gen.engine
def f():
  print('start')
  # Вызов my_function и возврат результата, как только вызовется "callback"
  # Результат - это аргумент, передаваемый в функцию обратного вызова(callback)
  result = yield gen.Task(my_function)
  print('result is', result)
  IOLoop.instance().stop()
 
if __name__ == "__main__":
  f()
  IOLoop.instance().start()
