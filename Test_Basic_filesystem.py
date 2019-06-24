import unittest
from winauto_benchmark import *
import logging
import win32api
import output_report
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')


TEMPLATE = os.path.abspath("template.docx")

print(win32api.GetLogicalDriveStrings().split(":\\\x00"))

TEST_TARGET = input("Partition( such as G ) :").upper()

class Benchmark(unittest.TestCase):

    # def tearDown(self):

    # def setUp(self):
    #     pass

    @classmethod
    def setUpClass(cls):

        tag = input("tag:")
        logging.info(f"Test partition : {TEST_TARGET}")
        run_path = os.path.join(os.getcwd(), time.strftime(f'winfs_{tag}_%Y%m%d-%H%M%S', time.localtime(time.time())))
        os.mkdir(run_path)
        logging.info(f"run_path: {run_path}")
        shutil.copy(TEMPLATE, run_path)
        shutil.copy("output_report.py", run_path)
        shutil.copy("report.ini", run_path)
        os.chdir(run_path)
        logging.info(f"Fomart finish!")

    # @unittest.skip("demonstrating skipping")
    def test_0_diskinfo(self):
        get_diskinfo(TEST_TARGET)

    def test_1_ASSD(self):
        run_assd(TEST_TARGET)

    def test_2_CDM(self):
        run_crystal__diskmark(TEST_TARGET)

    def test_3_ATTO(self):
        run_atto_disk_benchmark(TEST_TARGET)

    def test_4_TXbenck(self):
        run_txbench(TEST_TARGET)

    def test_5_Anvil(self):
        run_anvil(TEST_TARGET)

    def test_6_HDtune_fs(self):
        run_hdtune_fs(TEST_TARGET)

    def test_7_PCmark7(self):
        run_pc_mark7(TEST_TARGET)

    def test_8_PCmark8(self):
        run_pc_mark8(TEST_TARGET)

    @classmethod
    def tearDownClass(cls):
        output_report.get_report(template=TEMPLATE)
        logging.info("Test finish")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    test_cases = [
                    Benchmark("test_0_diskinfo"),
                    Benchmark("test_1_ASSD"),
                    Benchmark("test_2_CDM"),
                    Benchmark("test_3_ATTO"),
                    Benchmark("test_4_TXbenck"),
                    Benchmark("test_5_Anvil"),
                    Benchmark("test_6_HDtune_fs"),
                    Benchmark("test_7_PCmark7"),
                    Benchmark("test_8_PCmark8")
                  ]
    suite.addTests(test_cases)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
