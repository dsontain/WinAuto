import unittest
import time
from winauto_benchmark import *
#from WinAuto.winauto_benchmark import *
import sys
import diskpart_tool
from screenPrt import image_joint

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
        self.images = []
        
        Current_Cycle = run_dic["Current_Cycle"]
        self.outname = "cycle_{}.png".format(Current_Cycle)
        if Current_Cycle < self.cycle:
            print("The {} cycle test begin".format(Current_Cycle))
            run_dic["Current_Cycle"] += 1

            with open("run.json",'w',encoding='utf-8') as json_file:
                    json.dump(run_dic,json_file,ensure_ascii=False,indent=4)
                    #run_dic = json.load(json_file)
        else:
            print("The {} cycle test END!!!".format(self.cycle))
            while 1:
                time.sleep(100)

    @classmethod
    def tearDownClass(self):
        image_joint(self.outname, *self.images)
        if self.reboot :
            os.system("shutdown -r -t 5")
        #get_DiskInfo(self.disk, "end")

    #@unittest.skip("demonstrating skipping")
    def test_1_ASSD(self):
        im = run_assd(self.target)
        self.images.append(im)
    #@unittest.skip("demonstrating skipping")
    def test_2_CDM(self):
        im = run_crystal__diskmark(self.target)
        self.images.append(im)
    #@unittest.skip("demonstrating skipping")
    def test_3_ATTO(self):
        im = run_atto_disk_benchmark(self.target)
        self.images.append(im)
    @unittest.skip("demonstrating skipping")
    def test_4_TXbenck(self):
        run_txbench(self.target)
    @unittest.skip("demonstrating skipping")
    def test_5_Anvil(self):
        run_anvil(self.target)
    @unittest.skip("demonstrating skipping")
    def test_6_HDtune(self):
        diskpart_tool.DiskPart.clean(self.disk)
        run_hdtune(self.disk)


if __name__ == '__main__':
    unittest.main()#运行所有的测试用例



