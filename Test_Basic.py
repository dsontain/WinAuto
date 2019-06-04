import unittest
from winauto_benchmark import *
import diskpart_new
import logging
import win32api
import output_report
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')


TEMPLATE = os.path.abspath("template-1.docx")
dp = diskpart_new.Diskpart()
for k in dp.list_disk():
    print(f"disk : {k}")
while True:
    TEST_DISK = int(input("Select test disk："))
    if dp.system_disk_check(TEST_DISK):
        print("Do not select system disk!")
    else:
        logging.info(f"Test disk : {TEST_DISK}")
        break
dp.quit_diskpart()


print(win32api.GetLogicalDriveStrings().split(":\\\x00"))
while True:
    TEST_TARGET = input("Partition( such as G ) :").upper()
    if TEST_TARGET in win32api.GetLogicalDriveStrings().split(":\\\x00"):
        print(f"{TEST_TARGET} already exists, please input a new partition")
    else:
        logging.info(f"Test partition : {TEST_TARGET}")
        break


class Benchmark(unittest.TestCase):

    # def tearDown(self):

    # def setUp(self):
    #     pass

    @classmethod
    def setUpClass(cls):

        tag = input("tag:")
        run_path = os.path.join(os.getcwd(),
                                time.strftime(f'winbench_{tag}_%Y%m%d-%H%M%S', time.localtime(time.time())))
        os.mkdir(run_path)
        shutil.copy(TEMPLATE, run_path)
        shutil.copy("output_report.py", run_path)
        os.chdir(run_path)

        a = diskpart_new.Diskpart()
        a.select_disk(TEST_DISK)
        a.create_partition_primary(TEST_DISK, TEST_TARGET)
        a.quit_diskpart()
        get_DiskInfo(TEST_DISK)

    # @unittest.skip("demonstrating skipping")
    def test_1_ASSD(self):
        run_assd(TEST_TARGET)

    def test_2_CDM(self):
        run_CrystalDiskMark5(TEST_TARGET)

    def test_3_ATTO(self):
        run_ATTO_Disk_Benchmark(TEST_TARGET)

    def test_4_TXbenck(self):
        run_TxBENCH(TEST_TARGET)

    def test_5_Anvil(self):
        run_Anvil(TEST_TARGET)

    def test_6_HDtune(self):

        a = diskpart_new.Diskpart()
        a.clean(TEST_DISK)
        a.quit_diskpart()

        run_HDtune(TEST_DISK)

        a = diskpart_new.Diskpart()
        a.select_disk(TEST_DISK)
        a.create_partition_primary(TEST_DISK, TEST_TARGET)
        a.quit_diskpart()

    def test_7_PCmark7(self):
        run_PCmark7(TEST_TARGET)

    def test_8_PCmark8(self):
        run_PCmark8(TEST_TARGET)

    @classmethod
    def tearDownClass(cls):
        output_report.get_report(template=TEMPLATE)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    test_cases = [Benchmark("test_1_ASSD"), Benchmark("test_2_CDM"), Benchmark("test_3_ATTO"),
                  Benchmark("test_4_TXbenck"), Benchmark("test_5_Anvil"), Benchmark("test_6_HDtune"),
                  Benchmark("test_7_PCmark7"),
                  Benchmark("test_8_PCmark8")]
    suite.addTests(test_cases)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
