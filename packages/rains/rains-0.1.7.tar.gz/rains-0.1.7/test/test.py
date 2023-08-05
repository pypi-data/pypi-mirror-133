
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from rains.kit.web import *
from rains.common.run_pool import RunPool


class TaskTest(WebTask):
    """
    测试任务
    """
    user_input: WebElement
    password_input: WebElement
    login_button: WebElement
    create_button: WebElement

    def set_class_starting(self):
        self.user_input = self.plant.element(
            page='超管后台',
            name='邮箱输入框',
            by_key=BY.XPATH,
            by_value='/html/body/div/div/div/div/div[2]/form/div[1]/div/input'
        )

        self.password_input = self.plant.element(
            page='超管后台',
            name='密码输入框',
            by_key=BY.XPATH,
            by_value='/html/body/div/div/div/div/div[2]/form/div[2]/div/input'
        )

        self.login_button = self.plant.element(
            page='超管后台',
            name='Login按钮',
            by_key=BY.XPATH,
            by_value='/html/body/div/div/div/div/div[2]/form/div[4]/div/button'
        )

        self.create_button = self.plant.element(
            page='超管后台',
            name='Login按钮',
            by_key=BY.XPATH,
            by_value='/html/body/div/div/div/div/div/div[1]/a'
        )

    def set_function_starting(self):
        self.plant.view.to_url('http://manage.dev-tea.cblink.net/')

    def case_01(self):
        """
        登录成功
        """
        self.user_input.input.send('admin@baocai.us')
        self.password_input.input.send('123456')
        self.login_button.mouse.tap()
        return self.create_button.get.in_page() is True


if __name__ == '__main__':
    from rains.common.rains_server import RainsServer
    rains_server = RainsServer()
    rains_server.running()
