from copy import deepcopy

#Setting up global environment
variables = {}
operators = {'+': lambda t, e: plus(t, e),
             '-': lambda t, e: sub(t, e),
             '*': lambda t, e: mul(t, e),
             '/': lambda t, e: div(t, e),
             'var': lambda t, e: assign(t, e),
             'if': lambda t, e: cond(t, e),
             '&&': lambda t, e: logical_and(t, e),
             '||': lambda t, e: logical_or(t, e),
             '!': lambda t, e: logical_not(t, e),
             '==': lambda t, e: equality(t, e),
             '<=': lambda t, e: less_eq(t, e),
             '>=': lambda t, e: great_eq(t, e),
             '<': lambda t, e: less(t, e),
             '>': lambda t, e: great(t, e),
             'alert': lambda t, e: alert(t, e),
             'for': lambda t, e: for_loop(t, e),
             'while': lambda t, e: while_loop(t, e),
             'function': lambda t, e: function(t, e),
             'execute': lambda t, e: execute(t, e),
             'true': lambda t, e: True,
             'false': lambda t, e: False
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
    print sing_eval(t[0], env)
    return env

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
    i = 0
    found = False

    while (i < (len(env)-1)) and not found:
        if env[i].has_key(t[0]):
            found = True
        i+=1
    
    env = [{}] + env
    evaluate(env[i][t[0]], env)
    return env


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
    result = sing_eval(t[0], env)
    for i in t[1:]:
        result = result/sing_eval(i, env)
    return result

#Evaluation functions
def sing_eval(expr, env):
    '''Evaluates a single expression in the context of a specified
       environment.'''
    
    if isinstance(expr, list):
        token = expr[0]
    else:
        token = expr
    
    i = -1
    found = False
    while i < (len(env)-1) and (not found):
        i+=1
        if env[i].has_key(token): 
            found = True
    
    if found:
        if len(env)-1 == i:
            return env[i][token](expr[1:], env)
        else:
            return env[i][token]
    else:
        return token


def evaluate(parser_tree, env=[{}, operators]):
    '''The core function. Takes in a "lispyjs" program (essentially 
        an abstract syntax tree) and then recursively traverses and 
        evaluates the program.'''
    
    if isinstance(parser_tree[0], list):
        for i in parser_tree:
            #env = evaluate(i, env)   ###EEEK! Here's our recursion problem.
            evaluate(i, env)
    else:
        i = -1
        while i < (len(env)-1):
            i+=1
            if env[i].has_key(parser_tree[0]):
                return env[i][parser_tree[0]](parser_tree[1:], env)
        
        sing_eval(parser_tree[0], env)
        
        """if token == 'true':
            return True
        elif token == 'false':
            return False"""

        """
        if parser_tree[0] == 'true':
            return True
        else:
            return False
        
        print "this is token"
        print token
        return operators[token](parser_tree, env)
        """

if __name__ == "__main__":
    #parser_tree = ["if", ["||", ["false"], ["!",["false"] ] ],["*", 4, 1], ["-", 8, 2] ]
    #parser_tree = ["if", ["==", 2, 2], ["*", 2, 3], ['/', 2, 3] ]
    #parser_tree = [["var", "x", "2"], "while", ["==", 2, 'x'], [["alert", "Hello world"], "var", 'x', ["+", 'x', 1] ] ]
    #parser_tree = ["for", ["var", "i", 1], ["<=", "i", 10], ["var", "i", ["+", "i", 1]], ["alert", ["+", "i", 5] ]]
    #parser_tree = [["function", "helloworld", ["alert", "HELLO WORLD!"]], ["execute", "helloworld"]]
    #parser_tree = [["function", "foo", [["function", "bar", ["alert", "HIYA!"] ], ["execute", "bar"] ]  ], ["execute", "foo"]]
    #parser_tree = [["function", "foo", [["var", "tmp1", 6], ["function", "bar", ["alert", "HIYA!"] ], ["execute", "bar"] ]  ], ["execute", "foo"]]
    #parser_tree = [["function", "foo", [["var", "temp", 3], ["alert", ['+', "temp", 2]]]], ["execute", "foo"]]
    #parser_tree = [["function", "foo", [["var", "tmp1", 6], ["function", "bar", [["var", "tmp1", 1], ["var", "tmp2", 2], ["+", "tmp1", "tmp2"], ["alert", "tmp1"], ["alert", "tmp2"], ["alert", "HIYA!"] ]], ["execute", "bar"], ["alert", "tmp1"] ]  ], ["execute", "foo"]]
    #parser_tree = [["function", "foo", [["var", "tmp1", 6], ["function", "bar", [ ["var", "tmp2", 2], ["+", "tmp1", "tmp2"], ["alert", "tmp1"] ]], ["execute", "bar"], ["alert", "tmp1"] ]  ], ["execute", "foo"]]
    #parser_tree = [["function", "foo", [["alert", ['+', 3, 2]]]], ["execute", "foo"]]
    parser_tree = [["function", "foo", [["var", "tmp1", 6], ["alert", "tmp1"], 
                   ["function", "bar", [["var", "tmp1", 1], ["var", "tmp2", 2], ["alert", "tmp1"]]],  
                   ["execute", "bar"], ["alert", "tmp1"]]], ["execute", "foo"]]  ##Should print 6, 1, 6

    evaluate(parser_tree)



##To do:
##remove deepcopy
##unittests
##this?
##iterables, such as an array or dictionary?
##or maybe just move on...