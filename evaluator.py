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



def for_loop(t, env):
    tmp = deepcopy(t)

    env = evaluate(t[0], env)
    while(sing_eval(t[1], env)):
        env = evaluate(t[3], env)
        env = evaluate(t[2], env)

        t = deepcopy(tmp)

    return env


def while_loop(t, env):
    tmp = deepcopy(t)
    
    while evaluate(t[0], env):
        evn = evaluate(t[1], env)
        
        t = deepcopy(tmp)

    return env

def alert(t, env):
    print evaluate(t, env)

#Boolean expressions
def less_eq(t, env):
    return sing_eval(t[0], env) <= sing_eval(t[1], env)

def less(t, env):
    return sing_eval(t[0], env) < sing_eval(t[1], env)

def great_eq(t, env):
    return sing_eval(t[0], env) >= sing_eval(t[1], env)
    
def great(t, env):
    return sing_eval(t[0], env) > sing_eval(t[1], env)

def equality(t, env):
    return sing_eval(t[0], env)==sing_eval(t[1], env)

def logical_and(t, env):
    for i in t:
        if sing_eval(i, env) == False:
            return False
    return True

def logical_or(t, env):
    for i in t:
        if sing_eval(i, env) == True:
            return True
    return False

def logical_not(t, env):
    return not(sing_eval(t[0], env))

def cond(t, env):
    if sing_eval(t[0], env):
        return sing_eval(t[1], env)
    elif len(t) == 3:
        return sing_eval(t[2], env)

#Variable assignment
def assign(t, env):
    
    env[0][t[0]] = t[1]
    return env

def function(t, env):
    
    env[0][t[0]] = t[1]
    return env

def execute(t, env):

    i = -1
    found = False
    while i < (len(env)-1) and (not found):
        i+=1
        try env[i][t[0]]:
            found = True
            eval_this = env[i][t[0]]

    env = [{}] + env
    evaluate(eval_this, env)



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
def plus(t, env):
    result = 0
    for i in t:
        result += sing_eval(i, env)
    return result

def mul(t, env):
    result = 1
    for i in t:
        result *= sing_eval(i, env)
    return result

def sub(t, env):
    result = sing_eval(t[0], env)
    for i in t[1:]:
        result -= sing_eval(i, env)
    return result

def div(t, env):
    result = 1
    for i in t:
        result = sing_eval(i, env)/result

        #result /= evaluate(i)
    return result

def sing_eval(expr, env):

    token = expr[0]
    
    i = -1
    found = False
    while i < (len(env)-1) and (not found):
        i+=1
        try env[i][token]:
            found = True
    
    return env[i][token](expr[1:])



#Core of the program 
def evaluate(parser_tree, env):

    if isinstance(parser_tree[0], list):
        for i in parser_tree:
            env = evaluate(i, env)

    if isinstance(parser_tree, int):
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

    envir = [{}, operators]

    while len(parser_tree)>0:
        envir = evaluate(parser_tree, envir)


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