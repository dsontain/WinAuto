import unittest
from winauto_benchmark import *
import diskpart_new
import logging
import win32api
import output_report
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')


TEMPLATE = os.path.abspath("template.docx")
REPORT_INI = os.path.abspath("report.ini")
dp = diskpart_new.Diskpart()
for k in dp.list_disk():
    print(f"disk : {k}")
while True:
    TEST_DISK = int(input("Select test disk："))
    if dp.system_disk_check(TEST_DISK):
        print("Do not select system disk!")
    else:
        break
dp.quit_diskpart()


print(win32api.GetLogicalDriveStrings().split(":\\\x00"))
while True:
    TEST_TARGET = input("Partition( such as G ) :").upper()
    if TEST_TARGET in win32api.GetLogicalDriveStrings().split(":\\\x00"):
        print(f"{TEST_TARGET} already exists, please input a new partition")
    else:

        break


class Benchmark(unittest.TestCase):

    # def tearDown(self):

    # def setUp(self):
    #     pass

    @classmethod
    def setUpClass(cls):

        tag = input("tag:")
        logging.info(f"Test disk : {TEST_DISK}")
        logging.info(f"Test partition : {TEST_TARGET}")
        run_path = os.path.join(os.getcwd(),
                                time.strftime(f'winbench_{tag}_%Y%m%d-%H%M%S', time.localtime(time.time())))
        os.mkdir(run_path)
        logging.info(f"run_path: {run_path}")
        shutil.copy(TEMPLATE, run_path)
        shutil.copy("output_report.py", run_path)
        shutil.copy("report.ini", run_path)
        os.chdir(run_path)
        logging.info(f"Fomart disk {TEST_DISK} to partition {TEST_TARGET}")
        a = diskpart_new.Diskpart()
        a.select_disk(TEST_DISK)
        a.create_partition_primary(TEST_DISK, TEST_TARGET)
        a.quit_diskpart()
        logging.info(f"Fomart finish!")


    # @unittest.skip("demonstrating skipping")
    def test_0_diskinfo(self):
        get_diskinfo(TEST_DISK)

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

    def test_6_HDtune(self):

        a = diskpart_new.Diskpart()
        a.clean(TEST_DISK)
        a.quit_diskpart()

        run_hdtune(TEST_DISK)

        a = diskpart_new.Diskpart()
        a.select_disk(TEST_DISK)
        a.create_partition_primary(TEST_DISK, TEST_TARGET)
        a.quit_diskpart()

    def test_7_PCmark7(self):
        run_pc_mark7(TEST_TARGET)

    def test_8_PCmark8(self):
        run_pc_mark8(TEST_TARGET)

    @classmethod
    def tearDownClass(cls):
        output_report.get_report(template=TEMPLATE)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    test_cases = [
                    Benchmark("test_0_diskinfo"),
                    Benchmark("test_1_ASSD"),
                    Benchmark("test_2_CDM"),
                    Benchmark("test_3_ATTO"),
                    Benchmark("test_4_TXbenck"),
                    Benchmark("test_5_Anvil"),
                    Benchmark("test_6_HDtune"),
                    Benchmark("test_7_PCmark7"),
                    Benchmark("test_8_PCmark8")
                  ]
    suite.addTests(test_cases)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
