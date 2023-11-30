from config_ep.page.page_engineering import PageEngineering

class Test_UI:
    def setup_method(self):
        self.engineering = PageEngineering()
        self.engineering.engineering_window.set_focus() # 激活窗口

    def test_ui_all(self, epcam_ui_start):
        print("加载ep-cam")