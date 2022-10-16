@echo 【初始化前请确认已经安装python并配置好环境变量，否则无法初始化环境！】

python -m pip install --upgrade pip

@echo 【正在安装依赖包...】

pip install -r requirements.txt

@echo 【所有依赖包安装完成！】

timeout /t 5 /nobreak > NUL

