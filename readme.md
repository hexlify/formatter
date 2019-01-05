# Описание


**Важно: пока что программа не позволяет задовать конфигурацию языка и поэтому
некоторые элементы захардкожены. Будет исправлено в дальнейшем**

Можно поменять настройки вот тут: `main.py::configure_lexer`


# Язык

```
program : function (function)*

function : DEF variable combound_statement

statement_list : statement
               | statement SEMI statement_list

statement : compound_statement
          | assignment_statement
          | empty

compound_statement : BEGIN statement_list END

assignment_statement : variable ASSIGN expr1

empty :

expr1 : expr2 ((PLUS | MINUS) expr2)*

expr2 : expr3 ((MUL | DIV) expr3)*

expr3 : factor (POW factor)*

factor : PLUS factor
       | MINUS factor
       | INTEGER
       | LPAREN expr RPAREN
       | variable

variable: ID
```

# Принцип работы

+ `frmty.lexing` - разбивает код на токены
+ `frmty.parsing` - принимает на вход поток токенов и генерирует синтаксической дерево (AST)
+ `frmty.visiting` - обходит AST дерево и формирует соответствующий файл с кодом

# Запуск

`python3.5+`

```
$ python main.py <lang_description_file> <source_file>
```

**! Пока что файл конфигурации языка не играет роли**