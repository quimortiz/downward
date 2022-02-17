import unittest
import sys
import subprocess as sp


def run_cmd(cmd):
    print("Running", cmd)
    out = sp.run(cmd.split())
    print("Running DONE", cmd)
    return out

def get_modify_cmd(conflict,sas_in,sas_out):
    return  "python3 modify_sas.py test_sas/data/{} test_sas/data/{} test_sas/tmp/{}".format(conflict , sas_in,sas_out)

def get_check_cmd(sas, plan):
    return  "python3 check_plan_quim.py test_sas/tmp/{} test_sas/data/{}".format(sas,plan)



class TestMove(unittest.TestCase):

    def test1(self):
        cmd = get_modify_cmd( "conflictC.txt" , "sas.1.sas", "sas.1C.sas")
        run_cmd(cmd)
        cmd = get_check_cmd( "sas.1C.sas" , "planCInfeas1.txt")
        out = run_cmd(cmd)
        assert out.returncode == 1

    def test2(self):
        cmd = get_modify_cmd( "conflictA.txt" , "sas.1.sas", "sas.1A.sas")
        run_cmd(cmd)
        cmd = get_check_cmd( "sas.1A.sas" , "planAfeas1.txt")
        out = run_cmd(cmd)
        assert out.returncode == 0


    def test3(self):
        # cmd = "python3 modify_sas.py conflictA.txt sas.1.sas sas.1A.sas"
        cmd = get_modify_cmd( "conflictA.txt" , "sas.1.sas", "sas.1A.sas")
        run_cmd(cmd)
        cmd = get_check_cmd( "sas.1A.sas" , "planAinfeas2.txt")
        out = run_cmd(cmd)
        assert out.returncode == 1

    def testBinfeas(self):
        # cmd = "python3 modify_sas.py conflictA.txt sas.1.sas sas.1A.sas"
        cmd = get_modify_cmd( "conflictB.txt" , "sas.1.sas", "sas.1B.sas")
        run_cmd(cmd)
        cmd = get_check_cmd( "sas.1B.sas" , "planBinfeas1.txt")
        out = run_cmd(cmd)
        assert out.returncode == 1

    def testBfeas(self):
        # cmd = "python3 modify_sas.py conflictA.txt sas.1.sas sas.1A.sas"
        cmd = get_modify_cmd( "conflictB.txt" , "sas.1.sas", "sas.1B.sas")
        run_cmd(cmd)
        cmd = get_check_cmd( "sas.1B.sas" , "planBfeas1.txt")
        out = run_cmd(cmd)
        assert out.returncode == 0

    def testDfeas(self):
        # cmd = "python3 modify_sas.py conflictA.txt sas.1.sas sas.1A.sas"
        cmd = get_modify_cmd( "conflictD.txt" , "sas.1.sas", "sas.1D.sas")
        run_cmd(cmd)
        cmd = get_check_cmd( "sas.1D.sas" , "planDFeas1.txt")
        out = run_cmd(cmd)
        assert out.returncode == 0

    def testDinfeas(self):
        # cmd = "python3 modify_sas.py conflictA.txt sas.1.sas sas.1A.sas"
        cmd = get_modify_cmd( "conflictD.txt" , "sas.1.sas", "sas.1D.sas")
        run_cmd(cmd)
        cmd = get_check_cmd( "sas.1D.sas" , "planDInfeas1.txt")
        out = run_cmd(cmd)
        assert out.returncode == 1




if __name__ == "__main__":
    unittest.main()


