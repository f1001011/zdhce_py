
@echo off
REM 声明采用UTF-8编码
chcp 65001
echo %date% %time% ：start
python run.py
echo %time% ：执行完毕,按任意键退出!
pause
