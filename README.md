# 简介
## 项目名称：epcam_ui_test
## 项目作用：EP-CAM软件的UI自动化测试。

# 环境配置
## python环境：
### Python3.11.4，64位
* 安装python-3.11.4-amd64.exe。如已安装此版本，则略过。
  * 右击安装包，以管理员身份运行，打开安装程序。
  * 点击“Customize installation”。
  * 点击“Next”
  * 钩选“Install for all users”。
  * 安装路径改为“C:\Python3114”。然后点击“Install”。
  * 完成安装。
* 配置Python包安装源（为了提升下载包的速度） 
  * 在当前用户目录下新建“pip”名称的文件夹，在其中放入pip.ini文件。
  * 如果无些文件可以自行新建此文件，pip.ini中的内容为：
    * [global]
    * timeout = 6000
    * index-url = https://pypi.tuna.tsinghua.edu.cn/simple
    * trusted-host = pypi.tuna.tsinghua.edu.cn
* 创建虚拟环境
  * 管理员权限打开cmd。
  * 执行“pip install virtualenvwrapper-win”，安装好virtualenvwrapper-win。
  * 默认创建的虚拟环境位于C:\Users\username\envs,可以通过环境变量 WORKON_HOME 来定制。（一般无需设置）
  * 执行“mkvirtualenv -p python3.11.4 epcam_ui_test”，为当前项目创建虚拟环境。
  * 当前CMD界面会默认进入“epcam_test_client”虚拟环境下。
  * 常用命令如下（方便以后使用）：	
    * 创建虚拟环境：mkvirtualenv epcam_ui_test
    * 创建指定解释器的虚拟环境：mkvirtualenv -p python3.11.4 epcam_ui_test
    * 启动虚拟环境：workon epcam_ui_test
    * 退出虚拟环境：deactivate
    * 删除虚拟环境：rmvirtualenv epcam_ui_test
* Python包
  * 在当前项目的虚拟环境下，执行“pip install -r requirements.txt”
  * 参见requirements.txt
* 修改rarfile.py配置，设置支持最大200M文件。
  * 文件位置：C:\Users\用户名\Envs\虚拟环境名\Lib\site-packages\rarfile.py。
  * 代码修改：HACK_SIZE_LIMIT = 200 * 1024 * 1024
## WinRAR
  * 安装WinRAR
  * 配置环境变量：安装目录添加到系统环境变量Path里。
## Pycharm
## Git



# 架构说明
## Pytest + Pywinauto + POM
## Pytest
### config.py：基础配置
### conftest.py：fixture配置
### test_dir：测试用例路径，在config.py中指定
### run_tests.py：正式运行入口
### config_ep：悦谱CAM功能模块
### config_g：G软件功能模块
### cc：cc封装的方法
### data：测试用到的静态文件
## POM模式
### 操作层（基类Base）：config_ep/base/base.py，公用方法在此写
* 作用：对元素操作方法封装
* 命名举例：
  * 模块名：base.py
  * 类名：class Base:
  * 方法名：def get_file_compressed_job_name_by_job_id_from_dms():
* page页面一些公共的方法：
  * 下载测试料号
### 对象层（page）：
* 作用：对元素定位方法封装
* 命名规则：
  * 模块名：page+下划线+实际操作模块名称。
  * 函数名（类名）：使用大驼峰讲模块名称抄进来，有下划线去掉下划线。继承Base类。
  * 方法名：根据业务需求每个操作步骤单独封装一个方法（涉及元素，将每个元素操作单独封装一个操作方法）。
* 命名举例：
  * 模块名：page_input.py
  * 函数名（类名）：class PageInput(Base):
  * 方法名：def set_path(): 设置路径
* 注意：一个页面封装成一个对象，并继承 base
* 组合业务方法（组装）：根据需求组装以上操作步骤。如：page_input

### 业务层
* 作用：测试业务逻辑封装，将一个或多个操作组合起来完成一个业务功能。
* 命名规则：
  * 模块名：test+数字+下划线+实际操作模块名称；如果测试用例存在先后顺序，则可加上数字。
  * 测试业务名称：以大驼峰方法将模块名抄进来，有下划线去掉下划线。
  * 方法名：def test_engineering():
* 命名举例：
  * 模块名：test01_engineering.py
  * 测试业务名：class TestFile():
  * 方法名：def test_file_save_no_changed():


# 涉及技术
## 图像处理Opencv + 文字识别Tesseract




