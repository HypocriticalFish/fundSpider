@echo ����һ������ǰ������˫��������ĿĿ¼�µ�'init.bat'��ʼ�������������޷���ȡ���ݣ���


echo.
@echo ����ȡģʽ˵������


@echo off
@echo off
@echo ��basic��������ȡͶ�˲�Ʒ�������ݣ��������ֲ���Ϣ��������Ϣ�Լ�ÿ���Ƿ���Ϣ��
@echo ��detial��������ȡͶ�˲�Ʒ�ֲ���Ϣ��������Ϣ�Լ�ÿ���Ƿ���Ϣ���������������ݣ�
@echo ��all������ȡͶ�˲�Ʒȫ����Ϣ��Ĭ��ģʽ


@echo off

@echo off

set /p mode=��������ȡģʽ:


call .\venv\Scripts\activate.bat
@echo �Ѽ������⻷������ʼ��������...

python fundSpider.py %mode%


@echo ��ȡ�����������ĿĿ¼�µ�fundData�ļ����£���־�ļ�������logĿ¼�¡�

pause