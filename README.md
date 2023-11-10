# 概要说明
## 项目名称：epcam_ui_test
## 项目作用：EP-CAM软件的UI自动化测试。

# 环境配置
## python：
* 版本：python3.11.4
* 修改rarfile.py配置：C:\Users\Administrator\Envs\epcam_test_client\Lib\site-packages\rarfile.py。
HACK_SIZE_LIMIT = 200 * 1024 * 1024



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




