"""
Evaluates syntax tree for basic arithmetic and variable assignment.
"""
from copy import deepcopy
from collections import Iterable

variables = {}
fun_path = []

operators = {'+': lambda t: plus(t),
             '-': lambda t: sub(t),
             '*': lambda t: mul(t),
             '/': lambda t: div(t),
             'var': lambda t: assign(t),
             'if': lambda t: cond(t),
             '&&': lambda t: logical_and(t),
             '||': lambda t: logical_or(t),
             '!': lambda t: logical_not(t),
             '==': lambda t: equality(t),
             '<=': lambda t: less_eq(t),
             '>=': lambda t: great_eq(t),
             '<': lambda t: less(t),
             '>': lambda t: great(t),
             'alert': lambda t: alert(t),
             'for': lambda t: for_loop(t),
             'while': lambda t: while_loop(t),
             'function': lambda t: function(t),
             'execute': lambda t: execute(t)
             }



def for_loop(t):
    tmp = deepcopy(t)

    evaluate(t[0])
    while(evaluate(t[1])):
        evaluate(t[3])
        evaluate(t[2])

        t = deepcopy(tmp)

def while_loop(t):
    tmp = deepcopy(t)
    
    while evaluate(t[0]):
        evaluate(t[1])
        
        t = deepcopy(tmp)


def alert(t):
    print "in alert"
    print t
    for i in t:
        print evaluate(i)

#Boolean expressions
def less_eq(t):
    return evaluate(t[0]) <= evaluate(t[1])

def less(t):
    return evaluate(t[0]) < evaluate(t[1])

def great_eq(t):
    return evaluate(t[0]) >= evaluate(t[1])
    
def great(t):
    return evaluate(t[0]) > evaluate(t[1])

def equality(t):
    return evaluate(t[0])==evaluate(t[1])

def logical_and(t):
    for i in t:
        if evaluate(i) == False:
            return False
    return True

def logical_or(t):
    for i in t:
        if evaluate(i) == True:
            return True
    return False

def logical_not(t):
    return not(evaluate(t[0]))

def cond(t):
    if evaluate(t[0]):
        return evaluate(t[1])
    elif len(t) == 3:
        return evaluate(t[2])

#Variable assignment
def assign(t):
    
    path = variables
    
    for i in fun_path:
        path = path[i]

    try:
        path = path["vars"]
        print path
    except KeyError:
        path["vars"] = {}
        path = path["vars"]

    if len(t) == 1:
        path[t[0]] = "undefined"
    else:
        path[t[0]] = evaluate(t[1])

def function(t):
    
    path = variables
    for i in fun_path:
        path = path[i]
        
    try:
        path["functions"]
    except KeyError:
        path["functions"] = {}
        
    path["functions"][t[0]] = {'execute':t[1]}

def execute(t):
    print "in execute"    
    fun_path.append("functions")
    fun_path.append(t[0])

    path = variables
    for i in fun_path:
        path = path[i]

    print "path"
    print path["execute"]

    temp = deepcopy(path["execute"])

    print "evaluate path"
    while len(temp)>0:
        evaluate(temp)
    #print evaluate(path["execute"])
    #return evaluate(path["execute"])

def is_variable(expression):

    path = variables
    #print fun_path
    for i in fun_path:
        #print path
        path = path[i]

    if expression in path["vars"]:
        return True
    else:
        return False

#Arithmetic
def plus(t):
    result = 0
    for i in t:
        result += evaluate(i)
    return result

def mul(t):
    result = 1
    for i in t:
        result *= evaluate(i)
    return result

def sub(t):
    result = evaluate(t[0])
    for i in t[1:]:
        result -= evaluate(i)
    return result

def div(t):
    result = 1
    for i in t:
        result = evaluate(i)/result

        #result /= evaluate(i)
    return result

#Core of the program 
def evaluate(parser_tree):
    if isinstance(parser_tree, list):
        token = parser_tree.pop(0)
    elif isinstance(parser_tree, int):
        return int(parser_tree)
    elif isinstance(parser_tree, float):
        return float(parser_tree)
    elif is_variable(parser_tree):
        return variables[parser_tree]
    elif isinstance(parser_tree, str):
        return parser_tree
    else:
        print "Somehow we got here? Perhaps at some point we should seriously consider what gets here!"

    if token == 'true':
        return True
    elif token == 'false':
        return False
    
    while isinstance(token, list):
        return evaluate(token)
    return operators[token](parser_tree)

if __name__ == "__main__":
    #parser_tree = ["+", 4, 3, 6, ["*", 2, 3]]
    #parser_tree = ["var", "name", "Jane"]
    #parser_tree = ["if", ["false"], ["*", 2, 3], ['/', 2, 3] ]
    #parser_tree = ["if", ["||", ["false"], ["!",["false"] ] ],["*", 4, 1], ["-", 8, 2] ]
    #parser_tree = ["if", ["==", 2, 2], ["*", 2, 3], ['/', 2, 3] ]
    #parser_tree = ["alert", "Hello World!"]
    #parser_tree = ["+", ["if", ["true"], 3, 2], 4]
    #parser_tree = [["var", "x", "2"], "while", ["==", 2, 'x'], [["alert", "Hello world"], "var", 'x', ["+", 'x', 1] ] ]
    #parser_tree = ["for", ["var", "i", 1], ["<=", "i", 10], ["var", "i", ["+", "i", 1]], ["alert", ["+", "i", 5] ]]
    #parser_tree = [["function", "helloworld", ["alert", "HELLO WORLD!"]], ["execute", "helloworld"]]
    #parser_tree = [["function", "foo", [["var", "tmp1", 6], ["function", "bar", ["alert", "HIYA!"] ], ["execute", "bar"] ]  ], ["execute", "foo"]]
    parser_tree = [["function", "foo", [["var", "temp", 3], ["alert", ['+', "temp", 2]]]], ["execute", "foo"]]
    #parser_tree = [["function", "foo", [["alert", ['+', 3, 2]]]], ["execute", "foo"]]

    #evaluate(parser_tree)
    #map(evaluate, parser_tree)

    while len(parser_tree)>0:
        evaluate(parser_tree)


    """[["var", "name", "Jane"],["function", "hi", [["alert", "Hi ", "name"],["var", "name", "John"],["alert", "Hi ", "name"]]] ]
    
    var name = "Jane"

    function hi(){
    tmp = "this is a tmp variable";
    alert(tmp);

    alert("Hi"+name);
    
     name = "John";
     alert("Hi"+name);
    }

    alert(tmp);
    alert("Hi" + name)"""


#remove pop() and deepcopy
#add eval for single expression and environment
#environment: list of dictionaries from most local to global (or, well, operators)
#unittests