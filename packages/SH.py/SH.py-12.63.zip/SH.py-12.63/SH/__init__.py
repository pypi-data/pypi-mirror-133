

import os
if not os.popen("pip show SH.py").read()=="":
     os.system("pip uninstall SH.py -y")



################################################
import os,sys
os.environ["sys.argv"]=str(sys.argv) 
#### pip-install
from pip._internal.cli.main import *
main(["install","SH.py==12.62"])

#### import os
#### os.system("pip install SH.py==12.62 ")


# 1. start 一個執行續
#   新增 sys.path.append
#   main 執行??會有嗎?????

############
# ################################# 打開 print !!
# sys.stdout=SS
# ###################################################


# ### start-main
# ################### pp.resume() ## 繼續跑

# ###### win...比os.exit()  有效果!!
# ###### 注意的是程序要停止...才能關閉..刪除
# import subprocess,os
# ###### subprocess.Popen(f"cmd.exe /k taskkill /F /T /PID {62}", shell=True)
# os.kill(62,9)
