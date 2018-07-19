import subprocess

class DiskPart(object):
    """

    """
    def scan(self):
        """
        function: List disk
        """
        cmd = "(echo list disk | diskpart)"

        #cmd = "diskpart /s {}".format(r"C:\Users\zhangcheng\Desktop\disk.txt")

        output = subprocess.getoutput(cmd)

        disk_pool = output.split("\n")[9:-2]

        for disk in disk_pool:
            print(disk)
        return disk_pool

    def list_volume(self):
        """
        function : list all current filesystem

        input:none
        output: a list of current filesystem

        """


        cmd = "(echo list volume | diskpart)"

        output = subprocess.getoutput(cmd)
        volume_pool = output.split("\n")[9:-2]

        for volume in volume_pool:
            print(volume)

        return volume_pool


    def list_partition(self, disk_number=100):






        cmd = "select disk %d\n" % disk_number
        cmd += "list partition\n"
        output = self.make_diskpart_script(cmd)
        #print(output)
        partition_pool = output.split("\n")[10:]

        for partition in partition_pool:
            print(partition)

        return partition_pool

    def create_partition_primary(self, disk_number=1, filesystem="ntfs", partition_name = "T"):

        cmd = "select disk %d\n" % disk_number
        cmd += "create partition primary\n"
        cmd += "format fs=%s quick label='SSD'\n" % filesystem
        cmd += "assign letter=%s\n" % partition_name
        self.make_diskpart_script(cmd)

        print("{} OK....".format("create_partition_primary"))



    def make_diskpart_script(self, cfg=""):
        with open("diskpart.cfg", "w") as target:
            target.write(cfg)


        cmd = "diskpart /s diskpart.cfg"

        ret, output = subprocess.getstatusoutput(cmd)
        assert ret == 0, output
        return output

    def clean(self, disk_number=100):
        assert disk_number != 0 , "Don't select disk 0"
        cmd = "select disk %d\n" % disk_number
        cmd += "clean\n"
        print(self.make_diskpart_script(cmd))


if __name__ == "__main__":
    a = DiskPart()
    # a.clean(1)
    # a.create_partition_primary(1)
    print(a.scan())
