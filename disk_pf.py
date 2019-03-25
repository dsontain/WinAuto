
import win32com.client as client
import wmi
import time
import copy
c = wmi.WMI()
com = client.Dispatch("WbemScripting.SWbemRefresher")
obj = client.GetObject("winmgmts:\\root\cimv2")
diskitems = com.AddEnum(obj, "Win32_PerfFormattedData_PerfDisk_LogicalDisk").objectSet
    #time.sleep(1)

#diskitems = com.AddEnum(obj, "Win32_PerfRawData_PerfDisk_PhysicalDisk").objectSet



com.Refresh()


for k in diskitems:
    print(k.name)



start = diskitems[0].DiskReadsPerSec




class DiskAttribuce(object):
    def __init__(self, disk):
        self.CurrentDiskQueueLength = disk.CurrentDiskQueueLength
        self.DiskBytesPerSec = disk.CurrentDiskQueueLength
        self.DiskReadBytesPerSec = disk.CurrentDiskQueueLength
        self.DiskReadsPerSec = disk.CurrentDiskQueueLength
        self.DiskTransfersPerSec = disk.CurrentDiskQueueLength
        self.DiskWriteBytesPerSec = disk.CurrentDiskQueueLength
        self.DiskWritesPerSec = disk.CurrentDiskQueueLength


class DiskItem(object):
    def __init__(self):

        self.com = client.Dispatch("WbemScripting.SWbemRefresher")
        obj = client.GetObject("winmgmts:\\root\cimv2")
#diskitems = com.AddEnum(obj, "Win32_PerfFormattedData_PerfDisk_LogicalDisk").objectSet
    #time.sleep(1)

        self.diskitems = self.com.AddEnum(obj, "Win32_PerfRawData_PerfDisk_PhysicalDisk").objectSet

        self.com.Refresh()

        # self.CurrentDiskQueueLength = 0
        # self.Description = 0
        # self.DiskBytesPerSec = 0
        # self.DiskReadBytesPerSec = 0
        # self.DiskReadsPerSec = 0
        # self.DiskTransfersPerSec =0
        # self.DiskWriteBytesPerSec = 0
        # self.DiskWritesPerSec = 0


    def get_attribute(self, disknum = 0):
        self.com.Refresh()
        #print(len(self.diskitems))
        assert len(self.diskitems) - 1 > disknum, "This disk does not exsit !"
        

        disk = self.diskitems[disknum]
        dict_attribute = {
        "CurrentDiskQueueLength" :disk.CurrentDiskQueueLength,
        #"Description" : disk.Description,
        "DiskBytesPerSec" : disk.DiskBytesPerSec,
        "DiskReadBytesPerSec" : disk.DiskReadBytesPerSec,
        "DiskReadsPerSec" : disk.DiskReadsPerSec,
        "DiskTransfersPerSec" : disk.DiskTransfersPerSec,
        "DiskWriteBytesPerSec" : disk.DiskWriteBytesPerSec,
        "DiskWritesPerSec" : disk.DiskWritesPerSec
        }
        return dict_attribute

    def per_sec_performance(self, disknum = 0):
      
        
        init = self.get_attribute(disknum)
        time.sleep(1)
        #print(init["DiskTransfersPerSec"])
        while True:
            start = time.time()
            current = self.get_attribute(disknum)
            dict_performance = {
            "CurrentDiskQueueLength" :current["CurrentDiskQueueLength"],
            #"Description" : disk.Description,
            "DiskBytesPerSec" : int(current["DiskBytesPerSec"]) - int(init["DiskBytesPerSec"]),
            "DiskReadBytesPerSec" : int(current["DiskReadBytesPerSec"]) - int(init["DiskReadBytesPerSec"]),
            "DiskReadsPerSec" : current["DiskReadsPerSec"] - init["DiskReadsPerSec"],
            "DiskTransfersPerSec" : current["DiskTransfersPerSec"] - init["DiskTransfersPerSec"],
            "DiskWriteBytesPerSec" : int(current["DiskWriteBytesPerSec"]) - int(init["DiskWriteBytesPerSec"]),
            "DiskWritesPerSec" : int(current["DiskWritesPerSec"]) - int(init["DiskWritesPerSec"])
            }
            #print(dict_performance)
            info = "%s   |   IOPS: %8d    ( R:%8d    W:%8d )    |      BW: %8.3f MB    ( R:%8.3f MB    W:%8.3f MB ) | IOdepth:%5d" \
            %(str(time.ctime()), dict_performance["DiskTransfersPerSec"],  dict_performance["DiskReadsPerSec"], dict_performance["DiskWritesPerSec"], \
            dict_performance["DiskBytesPerSec"] / 1024 /1024, dict_performance["DiskReadBytesPerSec"] / 1024 /1024, dict_performance["DiskWriteBytesPerSec"] / 1024 /1024, dict_performance["CurrentDiskQueueLength"])
            print(info)

            init = current
            while  time.time() - start < 1:
                time.sleep(0.000001)
                continue
            #print(time.time() - start)
a = DiskItem()



a.per_sec_performance(disknum=int(input("choose a disk:  ")))



