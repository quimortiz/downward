import sys
import re
import read_sas
import sas_tasks
import timers
import os
from typing import List
from copy import deepcopy


def help():
    print("usage SCRIPT  sas  plan")

def apply_action( state: sas_tasks.SASInit  , action: sas_tasks.SASOperator):
    print( "apply action")
    print( action.dump())
    print( "on state" )
    print( state.dump())
    new_state = deepcopy(state)
    for var, pre,post,cond in action.pre_post:
        print("info")
        print(var,pre,post,cond)
        effect = True
        for vvar,vval in cond:
            # example of cond [(9, 0), (10, 5)]
            if state.values[vvar] != vval:
                effect = False
                break
        if effect:
            if pre != -1:
                assert new_state.values[var] == pre
            new_state.values[var] =  post
            # no conditional effects
        print("after")
        print(new_state.dump())
    print("resulting state is")
    print(new_state.dump())
    return new_state


def check_action( state: sas_tasks.SASInit, action: sas_tasks.SASOperator):
    appli = action.get_applicability_conditions()
    applicable = True

    print( "CHECK apply action")
    print( action.dump())
    print( "CHECK on state" )
    print( state.dump())



    for var,val in appli:
        if ( state.values[var] != val ) :
            applicable = False
            break
    return applicable


def is_goal( state : sas_tasks.SASInit, goal: sas_tasks.SASGoal ):

    is_goal = True
    for var, val in goal.pairs:
        if state.values[var] != val:
            is_goal = False
            break;

    return is_goal




def apply_list_actions( state: sas_tasks.SASInit, actions_str : List[str] , 
        sas : sas_tasks.SASTask ):
    """
    """

    states=[]
    states.append(state)
    for a_str in actions_str:
        action = next((x for x in sas_task.operators if x.name.strip() == a_str ), None)
        if action is None: 
            raise ValueError("action {} not found".format(a_str))

        if not check_action( state , action):
            raise ValueError("action {} is not applicable".format(a_str))

        state = apply_action( state , action )
        states.append(state)

    return states








if __name__ == "__main__":
    # read
    arg1 = sys.argv[1] # plan
    arg2 = sys.argv[2] # sas file

    # read sas
    sas_task = read_sas.read_sas_task(arg1)

    lines = []

    # read plan
    with open(arg2,'r') as file_object:
        lines = file_object.readlines()

    tokens = []
    lines_clean = []
    
    # get text inisde parenthesis
    for line in lines:
        if not line.startswith(";"):
            out = line[line.find("(")+1:line.find(")")]
            lines_clean.append(out.strip())
            tokens.append(out.strip().split())
    print(tokens)
    print(lines_clean)

    init_state = sas_task.init;
    print(init_state.dump())

    # apply an action

    action_name = " pick object_green3 green3 l_gripper "
    # action_name = " pick object_green3 object_red_quim l_gripper "

    for x in sas_task.operators:
        print("*"+x.name+"*")
        print(x.dump())

    action = next((x for x in sas_task.operators if x.name == action_name ), None)
    if action is not None:
        print("found action")
        print( action.dump())
    else: 
        print("action not found")

    values = init_state.values
    

    # get the result

    # print( " applicable",  check_action(values,action))

    # [(5, -1, 0, []), (7, 1, 0, []), (10, 0, 1, [])]

    # new_state = apply_action( values, action)
    # print(new_state)

    # self.prevail = sorted(prevail)
    # self.pre_post = self._canonical_pre_post(pre_post)
    # self.cost = cost



    print("FIRST CHECK")
    out = apply_list_actions( sas_task.init , lines_clean , sas_task)
    for i,s in enumerate(out):
        print(i)
        print(s.dump())

    print( "checking if is goal")
    goal = is_goal( out[-1] , sas_task.goal)
    print(goal)










