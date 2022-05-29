begin_version
3
end_version
begin_metric
0
end_metric
10
begin_variable
var0
-1
3
Atom on(base_ref, base)
Atom on(floor, base)
Atom on(free, base)
end_variable
begin_variable
var1
-1
2
Atom is_moving(base)
NegatedAtom is_moving(base)
end_variable
begin_variable
var2
-1
6
Atom on(block1, block2)
Atom on(block2, block2)
Atom on(block2_ref, block2)
Atom on(f_gripper, block2)
Atom on(m_gripper, block2)
Atom on(table, block2)
end_variable
begin_variable
var3
-1
2
Atom busy(f_gripper)
NegatedAtom busy(f_gripper)
end_variable
begin_variable
var4
-1
2
Atom busy(m_gripper)
NegatedAtom busy(m_gripper)
end_variable
begin_variable
var5
-1
6
Atom on(block1, block1)
Atom on(block1_ref, block1)
Atom on(block2, block1)
Atom on(f_gripper, block1)
Atom on(m_gripper, block1)
Atom on(table, block1)
end_variable
begin_variable
var6
-1
2
Atom infeas1-4(0)conflict0
Atom infeas1-4(1)conflict0
end_variable
begin_variable
var7
-1
2
Atom infeas2-4(0)conflict0
Atom infeas2-4(1)conflict0
end_variable
begin_variable
var8
-1
2
Atom infeas3-4(0)conflict0
Atom infeas3-4(1)conflict0
end_variable
begin_variable
var9
-1
2
Atom infeas4-4(0)conflict0
Atom infeas4-4(1)conflict0
end_variable
0
begin_state
0
1
2
1
1
1
1
0
0
0
end_state
begin_goal
2
5 2
9 0
end_goal
40
begin_operator
pick block1 block1 f_gripper f_base
0
5
0 3 1 0
0 5 0 3
0 6 -1 0
0 7 -1 0
0 8 -1 0
1
end_operator
begin_operator
pick block1 block1 m_gripper base
1
1 1
5
0 4 1 0
0 5 0 4
0 6 -1 0
1 6 1 7 0 1
1 7 1 8 0 1
1
end_operator
begin_operator
pick block1 block1_ref f_gripper f_base
0
5
0 3 1 0
0 5 1 3
0 6 -1 0
0 7 -1 0
0 8 -1 0
1
end_operator
begin_operator
pick block1 block1_ref m_gripper base
1
1 1
5
0 4 1 0
0 5 1 4
0 6 -1 0
1 6 1 7 0 1
1 7 1 8 0 1
1
end_operator
begin_operator
pick block1 block2 f_gripper f_base
0
5
0 3 1 0
0 5 2 3
0 6 -1 0
0 7 -1 0
0 8 -1 0
1
end_operator
begin_operator
pick block1 block2 m_gripper base
1
1 1
5
0 4 1 0
0 5 2 4
0 6 -1 0
1 6 1 7 0 1
1 7 1 8 0 1
1
end_operator
begin_operator
pick block1 f_gripper f_gripper f_base
1
5 3
4
0 3 1 0
0 6 -1 0
0 7 -1 0
0 8 -1 0
1
end_operator
begin_operator
pick block1 f_gripper m_gripper base
1
1 1
5
0 4 1 0
0 5 3 4
0 6 -1 0
1 6 1 7 0 1
1 7 1 8 0 1
1
end_operator
begin_operator
pick block1 m_gripper f_gripper f_base
0
5
0 3 1 0
0 5 4 3
0 6 -1 0
0 7 -1 0
0 8 -1 0
1
end_operator
begin_operator
pick block1 m_gripper m_gripper base
2
1 1
5 4
4
0 4 1 0
0 6 -1 0
1 6 1 7 0 1
1 7 1 8 0 1
1
end_operator
begin_operator
pick block1 table f_gripper f_base
0
5
0 3 1 0
0 5 5 3
0 6 -1 0
0 7 -1 0
0 8 -1 0
1
end_operator
begin_operator
pick block1 table m_gripper base
1
1 1
5
0 4 1 0
0 5 5 4
0 6 -1 0
1 6 1 7 0 1
1 7 1 8 0 1
1
end_operator
begin_operator
pick block2 block1 f_gripper f_base
0
4
0 2 0 3
0 3 1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
pick block2 block1 m_gripper base
1
1 1
4
0 2 0 4
0 4 1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
pick block2 block2 f_gripper f_base
0
4
0 2 1 3
0 3 1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
pick block2 block2 m_gripper base
1
1 1
4
0 2 1 4
0 4 1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
pick block2 block2_ref f_gripper f_base
0
4
0 2 2 3
0 3 1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
pick block2 block2_ref m_gripper base
1
1 1
4
0 2 2 4
0 4 1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
pick block2 f_gripper f_gripper f_base
1
2 3
3
0 3 1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
pick block2 f_gripper m_gripper base
1
1 1
4
0 2 3 4
0 4 1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
pick block2 m_gripper f_gripper f_base
0
4
0 2 4 3
0 3 1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
pick block2 m_gripper m_gripper base
2
1 1
2 4
3
0 4 1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
pick block2 table f_gripper f_base
0
4
0 2 5 3
0 3 1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
pick block2 table m_gripper base
1
1 1
4
0 2 5 4
0 4 1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
place block1 f_gripper block1 f_base
0
5
0 3 -1 1
0 5 3 0
0 6 -1 0
0 7 -1 0
0 8 -1 0
1
end_operator
begin_operator
place block1 f_gripper block2 f_base
0
6
0 3 -1 1
0 5 3 2
0 6 -1 0
0 7 -1 0
0 8 -1 0
1 8 1 9 0 1
1
end_operator
begin_operator
place block1 f_gripper table f_base
0
5
0 3 -1 1
0 5 3 5
0 6 -1 0
0 7 -1 0
0 8 -1 0
1
end_operator
begin_operator
place block1 m_gripper block1 base
1
1 1
5
0 4 -1 1
0 5 4 0
0 6 -1 0
0 7 -1 0
0 8 -1 0
1
end_operator
begin_operator
place block1 m_gripper block2 base
1
1 1
6
0 4 -1 1
0 5 4 2
0 6 -1 0
0 7 -1 0
0 8 -1 0
1 8 1 9 0 1
1
end_operator
begin_operator
place block1 m_gripper table base
1
1 1
5
0 4 -1 1
0 5 4 5
0 6 -1 0
0 7 -1 0
0 8 -1 0
1
end_operator
begin_operator
place block2 f_gripper block1 f_base
0
4
0 2 3 0
0 3 -1 1
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
place block2 f_gripper block2 f_base
0
4
0 2 3 1
0 3 -1 1
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
place block2 f_gripper table f_base
0
4
0 2 3 5
0 3 -1 1
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
place block2 m_gripper block1 base
1
1 1
4
0 2 4 0
0 4 -1 1
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
place block2 m_gripper block2 base
1
1 1
4
0 2 4 1
0 4 -1 1
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
place block2 m_gripper table base
1
1 1
4
0 2 4 5
0 4 -1 1
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
start_move base base_ref free
0
4
0 0 0 2
0 1 -1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
start_move base floor free
0
4
0 0 1 2
0 1 -1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
start_move base free free
1
0 2
3
0 1 -1 0
0 7 -1 0
1 7 1 8 0 1
1
end_operator
begin_operator
stop_move base free floor
0
4
0 0 2 1
0 1 0 1
0 7 -1 0
1 7 1 8 0 1
1
end_operator
0
