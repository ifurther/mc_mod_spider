@echo off
echo 扫描所安装的mod并记录mod名和文件名，放在【mod_info.txt】中
python 0.getinstances.py
set /p a=请输入任意键结束：
