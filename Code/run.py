import os

date = "06032022"
numbers = [0, 1, 2, 3]
for n in numbers:
    analysis_folder = r"C:\Users\liuzy\Documents\{0}\Analysis\{1:02d}".format(date, n)
    img_folder = r"D:\DE\{0}\{1:02d}\8-bit".format(date, n)
    print("{0} | {1:02d}".format(date, n))
    os.system("python correction.py {} {}".format(analysis_folder, img_folder))
