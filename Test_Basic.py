import unittest
import time
from winauto_benchmark import *
import sys
#import diskpart_tool
import diskpart_new
import logging
import win32api
import output_report
import shutil


logging.basicConfig(level = logging.INFO,format = '%(asctime)s - [%(levelname)s] - %(message)s')

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
        # with open("run.json",'r',encoding='utf-8') as json_file:
        #         #json.dump(tool_dic,json_file,ensure_ascii=False,indent=4)
        #         run_dic = json.load(json_file)
        # self.target = run_dic["Partition"]
        # self.disk = run_dic["Target"]
        a = diskpart_new.Diskpart()
        for k in a.list_disk():
            print(f"disk : {k}")
        while True:
            self.disk = int(input("Select test disk："))
            if a.system_disk_check(self.disk):
                print("Do not select system disk!")
            else:
                logging.info(f"Test disk : {self.disk}")
                break

        print(win32api.GetLogicalDriveStrings().split(":\\\x00"))


        while True:
            self.target = input("Partition( such as G ) :").upper()
            if self.target in win32api.GetLogicalDriveStrings().split(":\\\x00"):
                print(f"{self.target} already exists, please input a new partition")
            else:
                logging.info(f"Test partition : {self.target}")
                break
        tag = input("tag:")
        run_path = os.path.join(os.getcwd(), time.strftime(f'win_bench_{tag}_%Y%m%d-%H%M%S',time.localtime(time.time())))
        os.mkdir(run_path)
        self.template = os.path.abspath("template-1.docx")


        os.chdir(run_path)
        a.select_disk(self.disk)
        a.create_partition_primary(self.disk, self.target)
        a.quit_diskpart()

        get_DiskInfo(self.disk)
    
    @classmethod
    def tearDownClass(self):
        output_report.get_report(template=self.template)
        #output_report.modify_report(start=1,  output="report", template=self.template)

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

        a = diskpart_new.Diskpart()
        a.clean(self.disk)
        a.quit_diskpart()

        run_HDtune(self.disk)

        a = diskpart_new.Diskpart()
        a.select_disk(self.disk)
        a.create_partition_primary(self.disk, self.target)
        a.quit_diskpart()

    def test_7_PCmark7(self):
        run_PCmark7(self.disk)

    def test_7_PCmark8(self):
        run_PCmark8(self.disk)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        fire.Fire({
          'assd': run_assd,
          'cdm' : run_CrystalDiskMark5,
          'atto': run_ATTO_Disk_Benchmark,
          'txb' : run_TxBENCH,
          'avl' : run_Anvil,
          'HDtune': run_HDtune
      }
      )
        
    else:
        unittest.main()#运行所有的测试用例`
        

