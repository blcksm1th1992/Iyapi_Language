##############################
# Iyapi Interpreter          #
# Coded by Miles Livermont   #
# Github user blcksm1th1992  #
#                            #
##############################

from sys import *
from math import *

##############################
#Global Vars                 #
##############################

tokens = []
num_stack = []
symbols = {}

##############################
#Open test.lang              #
##############################
def open_file(filename):
#    print(filename)
    data = open(filename, "r").read()
    data += "<EOF>"
#    print(data)
    return data #not related to the other data

##############################
#LEXER                       #
##############################
def lex(filecontents):
    tok = ""
    isexpr = 0
    state = 0
    varstarted = 0
    var = ""
    string = ""
    expr = ""
    n = ""
    filecontents = list(filecontents)
    for char in filecontents:
        tok += char
        if tok == " ":
            if state == 0:
                tok = ""
            else:
                tok = " "
        elif tok ==  "\n" or tok == "<EOF>":
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
                isexpr = 0
            elif expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            elif var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            tok = ""
        elif tok == "=" and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if var != "":
                tokens.append("VAR:" + var)
                var = ""
                varstarted = 0
            if tokens[-1] == "EQUALS":
                tokens[-1] = "EQEQ"
            else:    
                tokens.append("EQUALS")
            tok = ""
        elif tok == "$" and state == 0:
            varstarted = 1
            var += tok
            tok = ""
        elif varstarted == 1:
            if tok == "<" or tok == ">":
                if var != "":
                    tokens.appened("VAR:" + var)
                    var = ""
                    varstarted = 0
            var += tok
            tok = ""
        elif tok.lower() == "wowapi": # tok.lower() creates a fucntion that makes Wowapi case insensitive
            tokens.append("WOWAPI")
            tok = ""    
        elif tok.lower() == "ihanke": # tok.lower() creates a fucntion that makes ihanke case insensitive
            tokens.append("ihanke")
            tok = ""
        elif tok.lower() == "heci": # tok.lower() creates a fucntion that makes heci case insensitive
            tokens.append("heci")
            tok = ""
        elif tok.lower() == "ehan": # tok.lower() creates a fucntion that makes ehan case insensitive
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""            
            tokens.append("ehan")
            tok = ""
        elif tok.lower() == "kha": # tok.lower() creates a fucntion that makes kha case insensitive
            tokens.append("kha")
            tok = ""
        elif tok== "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":
            expr += tok
            tok = ""
        elif tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "(" or tok == ")":
            isexpr = 1
            expr += tok
            tok = ""
        elif tok == "\"" or tok == " \"":
            if state == 0:
                state = 1
            elif state == 1:
#                print("FOUND A STRING") #this is a debugging coommand to make sure it can location strings
                tokens.append("STRING:" + string + "\"")
                string = ""
                state = 0
                tok = ""
        elif state == 1:
            string += tok
            tok = ""
    #print(tokens) #debugging tool to make sure all the tokens are being recongnized
    #return ''
    return tokens

##############################
#Calculating Expr            #
##############################

def evalExpression(expr):

    return eval(expr) # is a slightly unstable function that will autommatically evaluate expressions
# it will also work with order of operations; 10+2*4=18 vs (10+2)*4=48

##############################
#Extra Stuff                 #
##############################

def doWOWAPI(toWOWAPI):
	if(toWOWAPI[0:6] == "STRING"):
		toWOWAPI = toWOWAPI[8:]
		toWOWAPI = toWOWAPI[:-1]
	elif(toWOWAPI[0:3] == "NUM"):
		toWOWAPI = toWOWAPI[4:]
	elif(toWOWAPI[0:4] == "EXPR"):
		toWOWAPI = evalExpression(toWOWAPI[5:])
	print(toWOWAPI)

def doASSIGN(varname, varvalue):
    symbols[varname[4:]] = varvalue
   
def getVARIABLE(varname):
    varname = varname[4:]
    if varname in symbols:
        #print("TRUE") # debugggig code that one uses to make sure all variables are being read as defined.
        return symbols[varname]
    else:
        return "Variable ERROR YAH IDIOT: Undfefined Variable" # message when a variable is not defined/

def getKHA(string, varname):
    i = input(string[1:-1] + " ")
    symbols[varname] = "STRING:\"" + i + "\""
    

##############################
#PARSER                      #
##############################
def parse(toks):
#    print(toks)
    i = 0
    while(i <  len(toks)):
#        print(i)
        if toks[i] == "ihanke":
            i+=1
        elif toks[i] + " " + toks[i+1][0:6] == "WOWAPI STRING" or toks[i] + " " + toks[i+1][0:3] == "WOWAPI NUM" or toks[i] + " " + toks[i+1][0:4] == "WOWAPI EXPR" or toks[i] + " " + toks[i+1][0:3] == "WOWAPI VAR":
            if toks[i+1][0:6] == "STRING":
                doWOWAPI(toks[i+1])
            elif toks[i+1][0:3] == "NUM":
                doWOWAPI(toks[i+1])
            elif toks[i+1][0:4] == "EXPR":
                doWOWAPI(toks[i+1])
            elif toks[i+1][0:3] == "VAR":
                doWOWAPI(getVARIABLE(toks[i+1]))
            i+=2
        elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
            if toks[i+2][0:6] == "STRING":
                doASSIGN(toks[i],toks[i+2])
            elif toks[i+2][0:3] == "NUM":
                doASSIGN(toks[i],toks[i+2])
            elif toks[i+2][0:4] == "EXPR":
                doASSIGN(toks[i], "NUM:" + str(evalExpression(toks[i+2][5:])))
            elif toks[i+2][0:3] == "VAR":
                doASSIGN(toks[i],getVARIABLE(toks[i+2]))
            i+=3
        elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "kha STRING VAR":
            getKHA(toks[i+1][7:], toks[i+2][4:])
            i+=3
        elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4] == "heci NUM EQEQ NUM ehan":
            #print("Foudn an IF Statement")
            if toks[i+1][4:] == toks[i+3][4:]:
                print("True")
            else: 
                print("False")
            i+=5      
    #print(symbols)

##############################
#MAIN RUN FUNCTION           #
##############################
def run():
    data = open_file(argv[1])
    toks = lex(data)
    parse(toks)
run()
input() #this is only needed for windows due to the fact when this is run in powershell or cmd the windows go away to quickly for proper use
