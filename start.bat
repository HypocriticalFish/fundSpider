@echo ����һ������ǰ������˫��������ĿĿ¼�µ�'init.bat'��ʼ�������������޷���ȡ���ݣ���


echo.
@echo �����������ݿ�������Ϣ��Ĭ��ΪipΪlocalhost(127.0.0.1)��Ĭ�϶˿�Ϊ3306��Ĭ���ַ���Ϊ'utf8'��
@echo ������ # ����ʹ��Default_DB_Config.ini�е�Ĭ�����á�


@echo off
@echo off


set /p host=���������ݿ�ip:
set /p port=������˿ں�:
set /p user=�������û���:
set /p password=����������:


call .\venv\Scripts\activate.bat
@echo �Ѽ������⻷������ʼ��������...

python fundSpider.py %host% %port% %user% %password%


@echo ��ȡ�����ݱ�����tt_fund���ݿ��У���ṹ�Լ��ֶκ�����鿴ReadMe�ĵ�����־��鿴log�ļ��С�

pause