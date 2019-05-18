import subprocess
import time
import platform
import re


class InteractiveCommand(object):

    def __init__(self, process, prompt):
 
        self.process = subprocess.Popen(process, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        self.prompt = prompt.encode()
        self.coding = "gbk"
        self.output = ""
        if platform.system() == 'Windows':
            self.linebreak = "\r\n"
        else :
            self.linebreak = "\n"

    def find_prompt(self, prompt=None):
        
        buff = b""
        if not prompt:
            prompt = self.prompt
        # else：
        #     prompt = prompt.encode()
        want = re.compile(prompt)
        while True:
            buff += self.process.stdout.read(1)

            if want.search(buff) or self.process.poll():
                break
        return buff
    
    def send(self, cmd):
        if not self.process.poll():
            cmd = ("{}{}".format(cmd, self.linebreak)).encode()
            self.process.stdin.write(cmd)
            self.process.stdin.flush()
            return 1
        else:
            return 0

    def send_for_get(self, send , get=None):
        if self.send(send):
            return self.find_prompt(get)
        else:
            pass


class Diskpart(object):

    def __init__(self):
        self.op = InteractiveCommand("diskpart", "DISKPART> ")
        self.op.find_prompt().decode("gbk")

    def list_disk(self):
        cmd = "list disk"
        output = self.op.send_for_get(cmd)

        diskpool = re.findall(b"\xb4\xc5\xc5\xcc [0-9]+ +\xc1\xaa\xbb\xfa +[0-9]+ [MGTKP]B", output)
        disks = []
        for k in diskpool:
            disks.append(k.split(b" ")[1])
        return disks

    def select_disk(self, disk=200):
        assert self.check_disk_being(disk) == True, "No disk {} ".format(disk)

        cmd = "select disk {}".format(disk)
        output = self.op.send_for_get(cmd)

        if b'\xc4\xe3\xd6\xb8\xb6\xa8\xb5\xc4\xb4\xc5\xc5\xcc\xce\xde\xd0\xa7\xa1\xa3' in output:
            return False
        else:
            return output

    def detail(self, disk=2, info="disk"):
        cmd = "detail {}".format(info)
        if self.select_disk(disk):
            output = self.op.send_for_get(cmd)
            return output
        else:
            return b" "

    def system_disk_check(self, disk=20):
        
        if re.search(b"\xc6\xf4\xb6\xaf\xb4\xc5\xc5\xcc: \xca\xc7", self.detail(disk, "disk")):
            return True #系统盘
        else:
            return False

    def check_disk_being(self, disk=100):
        if str(disk).encode() in self.list_disk():
            return True
        else:
            return False
            
    def clean(self, disk=100):

        assert self.system_disk_check(disk) == False, "\n>>>>>>>>>>ERR：Can't clean system disk"

        cmd = "clean"

        if b'DiskPart \xb3\xc9\xb9\xa6\xb5\xd8\xc7\xe5\xb3\xfd\xc1\xcb\xb4\xc5\xc5\xcc\xa1\xa3' in self.op.send_for_get(cmd):
            return True
        else:
            return False

    def create_partition_primary(self, disk=100, target="G"):
        self.select_disk(disk)
        cmd = "create partition primary"

        if b'DiskPart \xb3\xc9\xb9\xa6\xb5\xd8\xb4\xb4\xbd\xa8\xc1\xcb\xd6\xb8\xb6\xa8\xb7\xd6\xc7\xf8\xa1\xa3' in self.op.send_for_get(cmd):
            cmd = "format fs=ntfs quick"
            self.op.send_for_get(cmd)
            cmd = "assign letter={}".format(target)
            self.op.send_for_get(cmd)
            return True
        else:
            return False

    def quit_diskpart(self):
        self.op.process.communicate(b"exit")

   
if __name__ == "__main__":

    pass
    
