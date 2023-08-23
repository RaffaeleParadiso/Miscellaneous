import shutil

path = "C:"
BytesPerGB = 1024 * 1024 * 1024
BytesPerMB = 1024 * 1024

(total, used, free) = shutil.disk_usage(path)
# print("Total: %.2fGB" % (float(total) / BytesPerGB))
# print("Used:  %.2fGB" % (float(used) / BytesPerGB))
# print("Used:  %.2fGB" % (float(free) / BytesPerGB))
with open("Data_disk_usage.txt", "a") as f:
        f.write(str("{:.1f}".format((float(used)/BytesPerMB))))
        f.write("\n")