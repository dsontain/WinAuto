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
        self.target = "G"
        self.disk = 2
        get_DiskInfo(self.disk, "start")
    
        #a = diskpart_tool.DiskPart()
        #a.clean(self.target)
        #a.create_partition_primary(self.disk, self.target)
    
    @classmethod
    def tearDownClass(self):
        pass
        #get_DiskInfo(self.disk, "end")

    @unittest.skip("demonstrating skipping")
    def test_1_ASSD(self):
        run_assd(self.target)
    @unittest.skip("demonstrating skipping")
    def test_2_CDM(self):
        run_CrystalDiskMark5(self.target)
    #@unittest.skip("demonstrating skipping")
    def test_3_ATTO(self):
        run_ATTO_Disk_Benchmark(self.target)
    
    def test_4_TXbenck(self):
        run_TxBENCH(self.target)
    def test_5_Anvil(self):
        run_Anvil(self.target)
    def test_6_HDtune(self):
        a = diskpart_tool.DiskPart()
        a.clean(self.disk)
        run_HDtune(self.disk)
if __name__ == '__main__':
    unittest.main()#运行所有的测试用例