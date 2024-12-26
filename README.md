# ПЕРЕПИСАТЬ РИДМИ !!! MLITA_colloq

[![Coverage Status](https://coveralls.io/repos/github/Fel1-of/MLITA_colloq/badge.svg?branch=main)](https://coveralls.io/github/Fel1-of/MLITA_colloq?branch=main)

## Задание 1.

Была разработана система классов для работы с логичискими выражениями и автоматического вывода системы тавтологий из аксиом

```mermaid
classDiagram

class Term {
  <<Interface>>
  +__str__() str*
  +__copy__() Term*
  +__deepcopy__(memo) Term*
  +humanize() str*
  +to_implication_view() Term*
  +substitute(**kwargs) Term*
  +get_substitution_map(other) dict*
  +unify(alphabet) Term*
  +vars() OrderedSet[str]*
}

class Operator {
  <<Abstract>>
  +__copy__() Term*
  +__deepcopy__(memo) Term*
  +__eq__(other) bool
  +substitute(**kwargs) Term
  +get_substitution_map(other) dict*
  +unify(alphabet) Term*
  +vars() OrderedSet[str]*
}

class NullaryOperator {
  <<Abstract>>
  +constructor()
}

class UnaryOperator {
  <<Abstract>>
  +arg : Term
}

class BinaryOperator {
  <<Abstract>>
  +arg1 : Term
  +arg2 : Term
}

class Var {
  +name : str
  +__str__() str
  +substitute(**kwargs) Term
  +humanize() str
  +vars() OrderedSet[str]
  +unify(alphabet) Term
}

class Not {
  +to_implication_view() Not
  +humanize() str
}

class And {
  +to_implication_view() Not
  +humanize() str
}

class Or {
  +to_implication_view() Arrow
  +humanize() str
}

class Xor {
  +to_implication_view() Not
  +humanize() str
}

class Arrow {
  +to_implication_view() Arrow
  +humanize() str
}

class Equal {
  +to_implication_view() Not
  +humanize() str
}

Term <|.. Operator
Operator <|.. NullaryOperator
Operator <|.. UnaryOperator
Operator <|.. BinaryOperator
Term <|.. Var
UnaryOperator <|.. Not
BinaryOperator <|.. And
BinaryOperator <|.. Or
BinaryOperator <|.. Xor
BinaryOperator <|.. Arrow
BinaryOperator <|.. Equal
```
### Идея реализованного алгоритма
Для автоматического вывода тавтологий из аксиом был взять за основу алгоритм BFS.

Всё начинается с двух ассоциативных массивов, один из которых хранит старые выведенные тавтологии (выведенные на предпредыдущих шагах), второй хранит тавтологии, выведенные на последнем шаге. При запуске поиска оба ассоциативных массива заполнены аксиомами.

Ассоциативный массив, то есть словарь, хранит тавтологию и соотвествующий ей силлогизм (метод, благодаря которому она была получена).
Для всех аксиоматичных тавтологий вводится "тривиальный" силлогизм "axiom", чисто из технических соображений. 

Далее для каждой пары, состоящей из элемента первого и второго массива, производится попытка применения Modus Ponens.
Важно отметить, что:
- правило вывода применяется как с прямым, так и с обратным порядком аргументов
- производятся все необходимые подстановки выражений в тавтологии (замены переменных на выражения)

Последняя указанная функция является одной из ключевых в решении
Она реализована методом `get_substuitution_map()`, которая для пары тавтологий подбирает значения переменных так, чтобы первое совпадало со вторым.
Например:
```python
# Пример работы метода get_substuitution_map()
inp1 = parse(input('Первая тавтология: '))
inp2 = parse(input('Вторая тавтология: '))
print('Словарь подстановок для приведения первого выражения во второе:')
print('\t', inp1.get_substitution_map(inp2))
print('Словарь подстановок для приведения второго выражения в первое:')
print('\t', inp2.get_substitution_map(inp1))
```
Вывод такой простенькой программы
```
Первая тавтология: a > a
Вторая тавтология: (!x > y) > (!x > y)
Словарь подстановок для приведения первого выражения во второе:
         {'a': Arrow(Not(Var('x')), Var('y'))}
Словарь подстановок для приведения второго выражения в первое:
         None
```
И действительно, если в первую тавтологию подставить вместо `a` следующее `Arrow(Not(Var('x')), Var('y'))` (то есть `(!x > y)`), то получится ровным счётом второе выражение.
Вывод None означает, что какие значения в `x` и `y` не подставляй, выражение вида `a > a` из него не получается.

Эта функция используется в силлогизмах и при проверке ответа.
В выводе отображается дополнительной строкой к силлогизму, например:
```
4. modus ponens:
        получено a > a
        из 1=[a > (b > a)], 2=[(a > b) > (a > a)]
        подстановкой во 2 a: (a), b: (b > a) 
        1=[a > (b > a)], 2=[(a > b) > (a > a)]
```
Строка `подстановкой во 2 a: (a), b: (b > a)` отражает действие метода

После перебора всех пар тавтологий, результат их применения сохраняется в новый ассоциативный массив, при этом производится исключение дубликатов (засчёт хешируемости тавтологии) и проверка на достижение конеченой цели.

При возможности получить искомое выражение подстановкой в одну из уже полученных тавтологий добавляется "тривиальный" силлогизм "substetute", который показывает какую именно подставку нужно выполнить.

Если выражение не найдено, поиск продолжается, при этом входные ассоциативные массивы обновляются.

После этого, по полученному ассоциативному массиву и последнему силлогизму собирается вывод искомого выражения.

### Полученные результаты
Произведена попытка реализовать программу, выводящую все выражения из исходных. К сожалению удалось вывести лишь А11: A∨¬A(преобразовано к !A->!A).

Запуск программы для аксимомы 11:
```
MLITA_colloq$ python main.py 
Введите выражение: a | !a
```

Протокол вывода для аксимомы 11:
```
0. axiom:       (a > (b > c)) > ((a > b) > (a > c))
1. axiom:       a > (b > a)
2. modus ponens:
        получено (a > b) > (a > a)
        из 1=[a > (b > a)], 2=[(a > (b > c)) > ((a > b) > (a > c))]
        подстановкой во 2 a: (a), b: (b), c: (a)
        1=[a > (b > a)], 2=[(a > (b > c)) > ((a > b) > (a > c))]
3. axiom:       a > (b > a)
4. modus ponens:
        получено a > a
        из 1=[a > (b > a)], 2=[(a > b) > (a > a)]
        подстановкой во 2 a: (a), b: (b > a)
        1=[a > (b > a)], 2=[(a > b) > (a > a)]
5. substitute:
        получено !a > !a
        из 1=[a > a]
        подстановкой во 1 a: (!a)
        1=[!a > !a]
Нетривиальных силлогизмов: 2
```

Запуск программы A -> A:
```
MLITA_colloq$ python main.py 
Введите выражение: a>a
```

Протокол вывода А -> A:
```
0. axiom:       (a > (b > c)) > ((a > b) > (a > c))
1. axiom:       a > (b > a)
2. modus ponens:
        получено (a > b) > (a > a)
        из 1=[a > (b > a)], 2=[(a > (b > c)) > ((a > b) > (a > c))]
        подстановкой во 2 a: (a), b: (b), c: (a)
        1=[a > (b > a)], 2=[(a > (b > c)) > ((a > b) > (a > c))]
3. axiom:       a > (b > a)
4. modus ponens:
        получено a > a
        из 1=[a > (b > a)], 2=[(a > b) > (a > a)]
        подстановкой во 2 a: (a), b: (b > a)
        1=[a > (b > a)], 2=[(a > b) > (a > a)]
Нетривиальных силлогизмов: 2
```


## Задание 2.
В процессе выполнения.
Были реализованы часть правил вывода, представленных ниже (отмечены галочками), однако они не интегрированы в поиск (это требует доработки кода)

- [x] Modus ponens:            P, P→Q ⊢ Q
- [x] Modus tollens:           P→Q, ⅂Q ⊢ ⅂P
- [ ] Дизъюнктивный силлогизм  ⅂P, P∨Q ⊢ Q
- [x] Гипотетический силлогизм    P→Q, Q→R ⊢ P→R
- [ ] Разделительный силлогизм   P, P xor Q ⊢ ⅂Q
- [ ] Простая конструктивная дилемма P→R, Q→R, P∨Q ⊢ R
- [ ] Сложная конструктивная дилемма P→R, Q→T, P∨Q ⊢ R∨T
- [ ] Простая деструктивная дилемма P→R, P→Q, ⅂R∨⅂Q ⊢ ⅂P
- [ ] Сложная деструктивная дилемма P→R, Q→T, ⅂R∨⅂T ⊢ ⅂P∨⅂Q 

## Задание 4.

Выражение, предложенное командой №2, успешно выводится разработанной программой за время всего около 0.02 c!

Запуск программы
```
python3 main.py
Введите выражение: (a>b)>(a>((!(b>((a>(b>c))>((a>b)>(a>c))))>!a)>((!(b>((a>(b>c))>((a>b)>(a>c))))>a)>(b>((a>(b>c))>((a>b)>(a>c)))))))
```

Вывод программы (время исполнения + протокол вывода)
```
Время выполнения: 0.020108 секунд
0. axiom:       A > (B > A)
1. axiom:       (!B > !A) > ((!B > A) > B)
2. axiom:       A > (B > A)
3. modus ponens:
        получено A > ((!B > !C) > ((!B > C) > B))
        из 1=[(!B > !A) > ((!B > A) > B)], 2=[A > (B > A)]
        подстановкой во 2 a: ((!A > !B) > ((!A > B) > A))
        1=[(!B > !A) > ((!B > A) > B)], 2=[A > (B > A)]
4. modus ponens:
        получено A > (B > ((!C > !D) > ((!C > D) > C)))
        из 1=[A > ((!B > !C) > ((!B > C) > B))], 2=[A > (B > A)]
        подстановкой во 2 a: (A > ((!B > !C) > ((!B > C) > B)))
        1=[A > ((!B > !C) > ((!B > C) > B))], 2=[A > (B > A)]
5. substitute:
        получено (a > b) > (a > ((!(b > ((a > (b > c)) > ((a > b) > (a > c)))) > !a) > ((!(b > ((a > (b > c)) > ((a > b) > (a > c)))) > a) > (b > ((a > (b > c)) > ((a > b) > (a > c)))))))
        из 1=[A > (B > ((!C > !D) > ((!C > D) > C)))]
        подстановкой во 1 A: (a > b), B: (a), C: (b > ((a > (b > c)) > ((a > b) > (a > c)))), D: (a)
        1=[(a > b) > (a > ((!(b > ((a > (b > c)) > ((a > b) > (a > c)))) > !a) > ((!(b > ((a > (b > c)) > ((a > b) > (a > c)))) > a) > (b > ((a > (b > c)) > ((a > b) > (a > c)))))))]
Нетривиальных силлогизмов: 2
```
