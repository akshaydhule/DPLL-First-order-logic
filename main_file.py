'''
	This program is to test the inference of First order logic with given test cases in Samples folder
'''
from __future__ import print_function
import sys

from copy import deepcopy
stack = []
count =1


class literal:
    def __init__(self, op, args):
        self.op = op
        self.args = args
        
class expr:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def expr_stand(self):
        d ={}
        for clause in self.lhs:
            ind = self.lhs.index(clause)
            self.lhs[ind] = stand_vars(clause, d)
        for clause in self.rhs:
            ind = self.rhs.index(clause)
            self.rhs[ind] = stand_vars(clause, d)
        
        
class Knowledge_Base:
    def __init__(self):
        self.base = {}
    def add(self,expr,key):
        if key not in self.base.keys():
            self.base[key] = []
        self.base[key].append(expr)
    def getexp(self,key):
        if key in self.base:
            return self.base[key]

def readfile(kb,query):
    #f = open (sys.argv[2],'r')
    #line = f.readline()
    f = open ("C:\Users\e\Desktop\AI\HW2\samples\sample06.txt",'r')
    express = f.readline().strip('\n') #query
    for expression in express.split(" && "):
        query.append(literal(expression.split('(')[0],expression.split('(')[1].strip(')').split(', '))) 

    no_of_lines = int(f.readline()) #no of lines in knowledge base
    while no_of_lines:
        expression = f.readline().strip("\n") 
        left_part = []
        right_part = []
## if no implication    
        if "=>" not in expression:
            lhs = expression.strip(" ")
            left = lhs
            clause = left.strip(" ")
            key = clause.split('(')[0]
            left_part.append(literal(clause.split('(')[0],clause.split('(')[1].strip(')').split(', ')))
            E = expr(left_part,right_part)
            kb.add(E,key)
## if two sides of kb
        else:
            lhs = (expression.split("=>")[0].strip(' '))
            rhs = (expression.split("=>")[1].strip(' '))
            left = lhs.split("&&")
            right = rhs
            for clause in left:
                clause = clause.strip(" ")
                left_part.append(literal(clause.split('(')[0],clause.split('(')[1].strip(')').split(', ')))
## for left part
            clause = right.strip(" ")
            key = clause.split('(')[0]
            right_part.append(literal(clause.split('(')[0],clause.split('(')[1].strip(')').split(', ')))
##for right part
            E = expr(left_part,right_part)
            kb.add(E,key)
        no_of_lines = no_of_lines- 1


def stand_vars(a, dict):
    global count
    if(dict==None):
        dict = {}
    if is_var(a) == False and not isinstance(a, literal):
        return a
    elif is_var(a) == True and not isinstance(a, literal): 
        if a in dict:
            return dict[a]
        else:
            val = "std_" + str(count)
            count  += 1
            dict[a] = val
            return val
    elif isinstance(a,literal):
        return literal(a.op, [stand_vars(b,dict) for b in a.args])
    else :
        return a

def is_var(a):
    if isinstance(a, str):
        return a[0].islower()
    return False

def extend(t,var,x): #add theta value 
    s = t.copy()
    s[var] = x
    if var in t.values():
        ind = t.values().index(var)
        s[t.keys()[ind]] = x
    t = s
    return s

def unify_var(var,a,t): #var unification
    if var in t:
        return unification(t[var],a,t)
    elif a in t:
        return unification(var,t[a],t)
    elif occur_check(var,a,t):
        return None
    else:
        return extend(t,var,a)

def occur_check(var,a, t): #occurrence check 
    if var == a:
        return True
    elif isinstance(a,str) and a in t:
        return occur_check(var, t[a], t)
    elif isinstance(a,literal) :
        return (occur_check(var, a.op, t) or occur_check(var, a.args, t))
    elif isinstance(a,list):
        for i in a:
            if occur_check(var, i, t) ==  True:
                return True
        return False
    else:
        return False

def unification(a,b,t): #unification of expression
    if t is None:
        return None
    elif a==b:
        return t
    elif is_var(a) and isinstance(a, str):
        return unify_var(a, b, t)
    elif is_var(b) and isinstance(b,str):
        return unify_var(b, a, t)
    elif isinstance(a, literal) and isinstance(b,literal):
        return unification(a.args, b.args, unification(a.op, b.op, t))
    elif isinstance(a,str) and isinstance(b,str):
        return None
    elif isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
        if len(a)==0:
            return t
        return unification(a[1:], b[1:], unification(a[0], b[0], t))
    else:
        return None

def substitute(t, a):# substitute from theta values    
    if t is None:
        return a
    if isinstance(a,list):
        return [substitute(t, ai) for ai in a]
    elif isinstance(a, str) and is_var(a):
        return t.get(a,a)
    elif isinstance(a,str):
        return a
    elif isinstance(a, literal):
        return literal(a.op,[substitute(t, ai) for ai in a.args])
    else:
        return a
    
previous_temp = " "
true_stack = []
def dpll_and(kb,query, t,model): 
    global true_stack
    global previous_temp
    if t is None:
        pass
    elif not query:
        yield t
    else :
        current, rest = query[0], query[1:]
        curr_sub = substitute(t, current)
        if curr_sub not in stack:
            stack.append(curr_sub)
        prnt = "Ask: " + curr_sub.op + "(" + ', '.join(str(p) if p.islower() == False else str("_") for p in curr_sub.args) + ")"
        if prnt != previous_temp:
            print( prnt)
        previous_temp = prnt
        for _t_1 in dpll_or(kb,curr_sub,t, model):
            if stack != []:
                stack.pop()
            curr_sub = substitute(_t_1, current)
            if curr_sub not in true_stack:
                true_stack.append(curr_sub)
            prnt = "True: " + curr_sub.op + "(" + ', '.join(str(p) if p.islower() == False else str("_") for p in curr_sub.args) + ")"
            if prnt != previous_temp:
                print( prnt)
            previous_temp = prnt
            for _t_2 in dpll_and(kb,rest,_t_1,model):
                yield _t_2
                
        if stack != []:
                stack.pop()
        if curr_sub not in true_stack:
            prnt = "False: " + curr_sub.op + "(" + ', '.join(str(p) if p.islower() == False else str("_") for p in curr_sub.args) + ")"
            if prnt != previous_temp:
                print( prnt)
            previous_temp = prnt
            
        if stack != []:
            new_val = stack.pop()
            prnt = "Ask: " + new_val.op + "(" + ', '.join(str(p) if p.islower() == False else str("_") for p in new_val.args) + ")"
            if prnt != previous_temp:
                print( prnt)
            previous_temp = prnt

def current_model(index,pos,val,model):
    hash_val = hash(str(index)+ str(pos) +''.join(str(arg) if arg.islower() == False else str("_") for arg in val.args))
    if hash_val in model:
        #if (index,pos) in model[hash_val]:
        return True
    return False

 
def updated_model(index,pos,val,model):
    new_model = deepcopy(model)
    hash_val = hash(str(index)+ str(pos) +''.join(str(arg) if arg.islower() == False else str("_") for arg in val.args))
    if hash_val not in new_model:
        new_model[hash_val] = []
    new_model[hash_val].extend((index,pos))
    return new_model

    
def dpll_or(kb,query,t, model):
    val_list = kb.getexp(query.op)
    index = query.op
    if val_list is None:
        return
    else:
        for pos,val in enumerate(val_list):
            if stack != []:
                stack.pop()
            exp = deepcopy(val)
            val = exp
            val.expr_stand()
            
            left_val = val.lhs 
            if len(val.rhs)>0:
                right_val = val.rhs[0]
            else:
                right_val = val.lhs[0]
                left_val =[] 
                
            theta = unification(right_val,query, t)
            new_model = {}
            if theta is not None:
                if pos>0:
                    prnt = "Ask: " + query.op + "(" + ', '.join(str(p) if p.islower() == False else str("_") for p in query.args) + ")"
                    if prnt != previous_temp:
                        print( prnt)
                        
                value = substitute(theta,right_val)
                if current_model(index,pos, value,model) == False:
                    new_model = updated_model(index,pos,value,model)
                if current_model(index,pos, value,model) == True:   
                    continue
            for _t_ in dpll_and(kb,left_val, theta,new_model):
                yield _t_


def dpll_satisfiable(kb, query,t,model):
    P = True
    
    for each in query:
        if each not in stack:
            stack.append(each)
        print( "Ask: " + each.op + "(" + ', '.join(str(p) if p.islower() == False else str("_") for p in each.args) + ")")
        
        try:
            theta = dpll_or(kb, each,t, model).next()
            curr_sub = substitute(theta, each)
            print( "True: " + curr_sub.op + "(" + ', '.join(str(p) for p in curr_sub.args) + ")")
            if stack != []:
                stack.pop()
            
        except:
            print( "False: " + each.op + "(" + ', '.join(str(p) for p in each.args) + ")")
            P = False
            break
    print( str(P),end="")


def main():
    #orig_stdout = sys.stdout
    f = file('C:\Users\e\Desktop\AI\HW2\output1.txt', 'w+')
    #sys.stdout = f
    global previous_temp
    kb = Knowledge_Base()
    query = []
    global stack
    global previous_temp
    
    readfile(kb,query)
    
    dpll_satisfiable(kb, query,{},{})
    
    #sys.stdout = orig_stdout
    f.close()
        
main()