import unittest
import time
from winauto_benchmark import *

import diskpart_tool

class Benchmark(unittest.TestCase):

    # def tearDown(self):
    #     # 每个测试用例执行之后做操作
    #     pass

    # def setUp(self):
    #     # 每个测试用例执行之前做操作
    #     pass
    #     #print('22222')

    @classmethod
    def setUpClass(self):
        with open("run.json",'r',encoding='utf-8') as json_file:
                #json.dump(tool_dic,json_file,ensure_ascii=False,indent=4)
                run_dic = json.load(json_file)
        
        
        self.target = run_dic["Partition"]
        self.disk = run_dic["Target"]
        self.reboot = run_dic["Reboot"]
        self.cycle = run_dic["Total_Cycle"]
        
        Current_Cycle = run_dic["Current_Cycle"]
        get_DiskInfo(self.disk, "start")
    
    @classmethod
    def tearDownClass(self):
        pass
        #get_DiskInfo(self.disk, "end")

    #@unittest.skip("demonstrating skipping")
    def test_1_ASSD(self):
        run_assd(self.target)
    #@unittest.skip("demonstrating skipping")
    def test_2_CDM(self):
        run_CrystalDiskMark5(self.target)
    #@unittest.skip("demonstrating skipping")
    def test_3_ATTO(self):
        run_ATTO_Disk_Benchmark(self.target)
    #@unittest.skip("demonstrating skipping")
    def test_4_TXbenck(self):
        run_TxBENCH(self.target)
    #@unittest.skip("demonstrating skipping")
    def test_5_Anvil(self):
        run_Anvil(self.target)
    #@unittest.skip("demonstrating skipping")
    def test_6_HDtune(self):
        diskpart_tool.DiskPart.clean(self.disk)
        run_HDtune(self.disk)



if __name__ == '__main__':
    unittest.main()#运行所有的测试用例`