# Задача.
Реализация генератора IP-пакетов в соответствии со стандартом RFC 791.

## Требования к реализации.

* Приложение должно выполнять функции генерации IP пакетов.
* Приложение должно позволять задавать адрес отправителя и получателя пакета
* Графический интерфейс.
* Отображать сообщения о возникающих ошибках и корректно их обрабатывать.

## Требования к надежности.

К приложению предъявляются следующие требования по надежности:
* Не допускается зависание приложения при любых действиях пользователя.
* Не допускается аварийное завершение приложения при любых действиях пользователя.
* Любая ошибочная ситуация должна корректно обрабатываться с выводом соответствующего сообщения.
* Не допускается утечка памяти/дескрипторов в процессе эксплуатации приложения.
* Не допускается полная загрузка процессора приложением в пассивном состоянии.

## Дополнительные требования.

Реализовать параллельную передачу/прием нескольких файлов.