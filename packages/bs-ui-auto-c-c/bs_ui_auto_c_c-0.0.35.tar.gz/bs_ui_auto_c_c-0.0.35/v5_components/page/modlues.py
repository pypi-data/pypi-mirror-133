
import json
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command

from b_c_components.Intercept_requests.selenium_network import info, get_network_data
from b_c_components.custom_module.custom_exception import Configuration_file_error
from b_c_components.get_environment import get_environment_data, get_host
from b_c_components.pytest_model import *


def login(username, password, driver):
    """
    登陆，返回cookie
    """
    session = requests.session()
    login_data = {
        "UserName": f"{username}",
        "Password": f"{password}",
        "LoginType": "0",
        "Remember": "true",
        "IsShowValCode": "false",
        "ValCodeKey": ""}
    try:
        italent_url = get_environment_data(os.environ.get('environment')).get('italent_url')
        r = session.post(
            url=italent_url + '/Account/Account/LogInITalent',
            data=login_data)
        if r.status_code == 200:
            if json.loads(r.text).get('Code') == 1:
                driver.get(italent_url)
                driver.add_cookie({'domain': get_host().get('account'),
                                   'name': 'ssn_Tita_PC',
                                   'value': r.cookies.get('Tita_PC')})
                driver.add_cookie(
                    {'name': 'Tita_PC', 'value': r.cookies.get('Tita_PC')})
                driver.add_cookie(
                    {'name': 'Tita_PC', 'value': r.cookies.get('Tita_PC')})
                driver.get(italent_url)
            else:
                raise
        else:
            raise
    except Exception as e:
        raise e


def login_interface(username, password):
    """

    :param username:
    :param password:
    """

    session = requests.session()
    login_data = {
        "UserName": f"{username}",
        "Password": f"{password}",
        "LoginType": "0",
        "Remember": "true",
        "IsShowValCode": "false",
        "ValCodeKey": ""}
    italent_url = get_environment_data(os.environ.get('environment')).get('italent_url')
    r = session.post(url=italent_url + '/Account/Account/LogInITalent', data=login_data)
    if r.status_code == 200:
        return session
    else:
        return Configuration_file_error(msg=r.text)


def unfinished_transactions(driver, transaction_type, transaction_name):
    """
    cloud待办的处理
    transaction_type 待办所属产品
    transaction_name 以绩效为例，transaction_name代表活动
    """
    cookie = ''
    cookie_list = driver.get_cookies()
    driver.global_cases_instance.update(BSGlobal={})
    time.sleep(0.5)
    driver.global_cases_instance.get('BSGlobal').update(
        tenantInfo=driver.execute_script('return BSGlobal.tenantInfo'))
    driver.global_cases_instance.get('BSGlobal').update(
        userInfo=driver.execute_script('return BSGlobal.userInfo'))
    ssn_Tita_PC = ''
    for i in cookie_list:
        if i.get('name') == 'Tita_PC':
            cookie = f'{i.get("name")}={i.get("value")}' + \
                     f'; {"ssn_Tita_PC"}={i.get("value")}'
            ssn_Tita_PC = i.get("value")
            break
    headers = {
        'Cookie': cookie
    }
    tenantId = str(driver.global_cases_instance.get(
        'BSGlobal').get('tenantInfo').get('Id'))
    userId = str(driver.global_cases_instance.get(
        'BSGlobal').get('userInfo').get('userId'))

    session = requests.session()
    italent_url = get_environment_data(os.environ.get('environment')).get('italent_url')
    url = f'{italent_url}/api/v3/{tenantId}/{userId}/todo/Get?app_id=-1&deadline=&blackTodoIds=&page_size=10&status=1&__t={round(time.time() * 1000)}'
    all_transactions = json.loads(
        session.get(
            url=url,
            headers=headers).text).get('data').get('todos')
    cloud_url = get_environment_data(os.environ.get('environment')).get('cloud_url').split('://')[1]
    driver.add_cookie(
        {'domain': cloud_url, 'name': 'ssn_Tita_PC', 'value': ssn_Tita_PC})
    for i in all_transactions:
        if transaction_type == i.get('appName'):
            if transaction_name != "" and transaction_name in i.get('content'):
                driver.get(url='https:' + i.get('objUrl'))
                break


def go_to_menu(driver, menu_name):
    """
    进入菜单
    menu_name: 菜单名称，默认菜单传应用名称，非默认菜单传应用名称_菜单名称
    """
    cloud_host = get_host().get('cloud')
    driver.add_cookie({'domain': cloud_host,
                       'name': 'ssn_Tita_PC',
                       'value': driver.get_cookie('Tita_PC').get('value')})
    driver.add_cookie({'domain': cloud_host,
                       'name': 'Tita_PC',
                       'value': driver.get_cookie('Tita_PC').get('value')})
    menu_mapping = requests.get('http://8.141.50.128:80/static/json_data/menu_mapping.json').json()
    host_url = get_environment_data().get('cloud_url')
    driver.get(host_url + menu_mapping.get(menu_name))


def get_form_view(driver):
    """
    获取表单信息
    """
    fields_to_operate_on_list = []
    network_data = info(driver)
    network_data.reverse()
    datasource_data = []
    for data in network_data:
        url = data.get('request').get('url')
        if '/api/v2/data/datasource' in url:
            # 获取字段对应数据源
            datasource_data = json.loads(data.get('response_data').get('body'))
            break
    for data in network_data:
        # 解析formView接口，获取所有表单字段
        url = data.get('request').get('url')
        if '/api/v2/UI/FormView' in url:
            # 在这里获取所有需要操作的字段
            for sub in json.loads(
                    data.get('response_data').get('body')).get('sub_cmps'):
                for field in sub.get('sub_cmps'):
                    if field.get('cmp_data').get('showdisplaystate') == 'readonly' and field.get(
                            'cmp_data').get('required') is True:
                        dict_data = {}
                        for data_source in datasource_data:
                            if field.get('cmp_data').get(
                                    'datasourcename') == data_source.get('key'):
                                dict_data['dataSourceResults'] = data_source.get(
                                    'dataSourceResults')
                                break
                        dict_data.update({
                            'cmp_id': field.get('cmp_id'),
                            'cmp_label': field.get('cmp_label'),
                            'cmp_name': field.get('cmp_name'),
                            'cmp_type': field.get('cmp_type'),
                            'cmp_data': field.get('cmp_data')
                        })
                        fields_to_operate_on_list.append(dict_data)
    return fields_to_operate_on_list


def option_form(driver, fields_to_operate_on_list, **kwargs):
    """
    操作表单
    """
    if kwargs.keys() is not None:
        pass
    enter_iframe(driver, '//*[@class="modal-pop"]')
    for field in fields_to_operate_on_list:
        """
        表单填充
        """
        if field.get('cmp_type') == 'BC_TextBox':
            """
            文本输入框类型
            """
            title_xpath = f"(//div[@class='form-item__title ']/a[@class='form-item__required'])[{fields_to_operate_on_list.index(field) + 1}]/../..//input"
            element = driver.find_element_by_xpath(title_xpath)
            element.clear()
            key_value = field.get('cmp_label')
            if key_value in kwargs.keys():
                pass
            if kwargs.__contains__(key_value):
                input_text = kwargs.get(key_value)
                element.send_keys(input_text)
            else:
                element.send_keys(
                    '自动化数据' + str(int(time.time())))
            driver.execute_script("arguments[0].blur();", element)

        elif field.get('cmp_type') == 'BC_TextArea':
            """
            富文本类型
            """
            title_xpath = f"(//div[@class='form-item__title ']/a[@class='form-item__required'])[{fields_to_operate_on_list.index(field) + 1}]/../..//textarea"
            element = driver.find_element_by_xpath(title_xpath)
            element.clear()
            key_value = field.get('cmp_label')
            if kwargs.__contains__(key_value):
                input_text = kwargs.get(key_value)
                element.send_keys(input_text)
            else:
                element.send_keys(
                    '自动化数据富文本类型' + str(int(time.time())))
            driver.execute_script("arguments[0].onblur;", element)
        elif field.get('cmp_type') == 'BC_DropDownList':
            """
            下拉类型
            """
            title_xpath = f"(//div[@class='form-item__title ']/a[@class='form-item__required'])[{fields_to_operate_on_list.index(field) + 1}]/../..//div[@class='input_']"
            driver.find_element_by_xpath(title_xpath).click()
            key_value = field.get('cmp_label')

            if kwargs.__contains__(key_value):
                select_name = kwargs.get(key_value)
                li_xpath = f"//ul[@class='dropdown__list a-height-spread']/li/span[text()='{select_name}']"
            else:
                li_xpath = "//ul[@class='dropdown__list a-height-spread']/li"
            driver.find_element_by_xpath(li_xpath).click()
        elif field.get('cmp_type') == 'BC_UserSelect':
            """人员选择"""
            title_xpath = f"(//div[@class='form-item__title ']/a[@class='form-item__required'])[{fields_to_operate_on_list.index(field) + 1}]/../..//input/.."
            driver.find_element_by_xpath(title_xpath).click()
            key_value = field.get('cmp_label')
            if kwargs.__contains__(key_value):
                usernames = kwargs.get(key_value)
                for username in usernames:
                    username_input_xpath = "//div[@id='BS_mountComponent_userselect']//input"
                    driver.find_element_by_xpath(username_input_xpath).clear()
                    driver.find_element_by_xpath(username_input_xpath).send_keys(username)
                    select_name_xpath = f"//ul[@class='us-item-top']/li//em[text()='{username}']"
                    driver.find_element_by_xpath(select_name_xpath).click()
            else:
                select_name_xpath = f"//ul[@class='us-item-top']/li/"
                driver.find_element_by_xpath(select_name_xpath).click()
            driver.find_element_by_xpath(
                '//div[@class="us-container"]//span[@class="base-bg-ripple  base-btns-bgc-small  "]').click()
        elif field.get('cmp_type') == 'BC_DigitText':
            """
            数值输入框
            """
            title_xpath = f"(//div[@class='form-item__title ']/a[@class='form-item__required'])[{fields_to_operate_on_list.index(field) + 1}]/../..//input"
            driver.find_element_by_xpath(title_xpath).clear()
            key_value = field.get('cmp_label')
            if kwargs.__contains__(key_value):
                input_num = kwargs.get(key_value)
                driver.find_element_by_xpath(title_xpath).send_keys(input_num)
            else:
                input_num = random.randint(1, 100)
                driver.find_element_by_xpath(title_xpath).send_keys(input_num)
            driver.execute_script("arguments[0].blur();", driver.find_element_by_xpath(title_xpath))
        elif field.get('cmp_type') == 'BC_DateTime':
            """时间选择"""
            title_xpath = f"(//div[@class='form-item__title ']/a[@class='form-item__required'])[{fields_to_operate_on_list.index(field) + 1}]/../..//input/.."
            driver.find_element_by_xpath(title_xpath).click()
            driver.find_element_by_xpath("//input[@class='ant-calendar-input  head-input ']").clear()
            key_value = field.get('cmp_label')
            if kwargs.__contains__(key_value):
                input_date = kwargs.get(key_value)
                driver.find_element_by_xpath("//input[@class='ant-calendar-input  head-input ']").send_keys(input_date)
            else:
                driver.find_element_by_xpath("//a[@class='ant-calendar-today-btn ' and text()='今天']").click()
        elif field.get('cmp_type') == 'BC_FileUploader':
            title_xpath = f"(//div[@class='form-item__title ']/a[@class='form-item__required'])[{fields_to_operate_on_list.index(field) + 1}]/../..//input"
            key_value = field.get('cmp_label')
            if kwargs.__contains__(key_value):
                input_file = kwargs.get(key_value)
            else:
                input_file = os.environ.get('application_path') + driver.global_instance.get('config').get_setting('upload_file', 'file_path')
            driver.find_element_by_xpath(title_xpath).send_keys(input_file)
    driver.switch_to_default_content()


def click_check_index(driver, list_index):
    """
    点击列表上的复选框，支持int和list，int单选，list多选
    """
    check_str_path = '//*[@name="checkboxPro"]'
    if isinstance(list_index, int):
        element = driver.find_elements_by_xpath(check_str_path)[list_index-1]
        element.click()
    elif isinstance(list_index, list):
        for i in list_index:
            element = driver.find_elements_by_xpath(check_str_path)[i-1]
            element.click()


def go_to_data_details(driver, details_page_name, details_page_id):
    """
    进入列表数据详情

    :param driver: driver: 实例
    :param details_page_name: 哪个产品的详情页
    :param details_page_id: 详情页的id('新增接口有返回')
    """
    host_url = get_environment_data(os.environ.get('environment')).get('cloud_url')
    details_page_mapping = requests.get(
        'http://8.141.50.128:80/static/json_data/details_page_mapping.json').json()
    if details_page_mapping.get(details_page_name):
        interface_url = details_page_mapping.get(details_page_name)
        headers = {
            'Pragma': 'no-cache'
        }
        driver.get(host_url + interface_url + details_page_id)
    else:
        raise Configuration_file_error(msg='mappings文件中没有对应的详情页地址')


def check_list_data(driver):
    """
    校验列表数据当前分页中的指定数据或所有的所有字段是否有值
    """
    list_elements = list()
    for list_element in driver.find_elements_by_xpath('//*[@class="z-table"]/div/div'):
        col_element_data = dict()
        for col_element in list_element.find_elements_by_xpath('./div'):
            if col_element.get_attribute('name') == 'CreatedBy':
                col_element_data[col_element.get_attribute('name')] = \
                    col_element.find_element_by_xpath('./div/div/span[2]').text
                continue
            col_element_data[col_element.get_attribute('name')] = col_element.text
        list_elements.append(col_element_data)
    network_data = info(driver)
    tab_list_data = None
    for data in network_data:
        if '/api/v2/UI/TableList' in data.get('request').get('url'):
            tab_list_data = json.loads(data.get('response_data').get('body'))
            break
    if tab_list_data is not None:
        for biz_data in tab_list_data.get('biz_data'):
            col_list = list_elements.pop(0)
            failure_data = [c for c in list(col_list.keys()) if c not in list(biz_data.keys())]
            if failure_data:
                for data in failure_data:
                    pytest_assume(driver, col_list.get(data), list(biz_data.keys()), '列表中的字段在接口中不存在即没有数据')
            else:
                pytest_assume(driver, True, True, '对比当前页面的所有字段，数据正确')
                failure_data = [d for d in list(col_list.keys()) if col_list.get(d) not in biz_data.get(d).get('value')]
                if 'CreatedBy' in failure_data:
                    failure_data.pop(failure_data.index('CreatedBy'))
                    CreatedBy = biz_data.get('CreatedBy').get('text').split('(')[0]
                    pytest_assume(driver, col_list.get('CreatedBy'), CreatedBy, '创建人字段值正确')
                if failure_data:
                    for data in failure_data:
                        pytest_assume(driver, col_list.get(data), biz_data.get(data).get('value'),
                                      '列表中的字段对应值在接口中不存在即没有数据')

                else:
                    pytest_assume(driver, True, True, '对比当前页面的所有字段的值，数据存在')
                continue


def filter_item(driver, filter_name, *args, **kargs):
    """
    对筛选条件进行操作
    :param driver: driver: 实例
    :param filter_name: 筛选条件的名称
    """
    filter_xpath = f"//div[@class='searchform clearfix']//span[@class='lable' and text()='{filter_name}']"
    filter_cmp_type = get_filter_info(driver, filter_name)
    driver.find_element_by_xpath(filter_xpath).click()
    if filter_cmp_type == 'BC_TextBox':
        driver.find_element_by_xpath('//*[@id="inputText"]').send_keys(args)
        driver.find_element_by_xpath('//div[@class="TextBoxShow"]//span[@class="base-btn-title"]/..').click()
    elif filter_cmp_type == 'BC_UserSelect':
        for arg in args:
            driver.find_element_by_xpath("//div[@class='base-search-component']//input").clear()
            driver.find_element_by_xpath("//div[@class='base-search-component']//input").send_keys(arg)
            time.sleep(1)
            driver.find_element_by_xpath("//div[@class='us-user-info']").click()
        driver.find_element_by_xpath(
            '//div[@class="us-container"]//span[@class="base-bg-ripple  base-btns-bgc-small  "]').click()
    elif filter_cmp_type == 'BC_DropDownList':
        for arg in args:
            driver.find_element_by_xpath(f"//span[@class='form-item__label' and text()='{arg}']").click()
        driver.find_element_by_xpath('//div[@id="DropdownList_ul"]//button[@class="btn btn_default btn_sm"]').click()
    elif filter_cmp_type == 'BC_DateTimeRange':

        driver.find_element_by_xpath(
            "//input[@class='ant-calendar-range-picker ant-input input-create-picker ' and @placeholder='开始时间']/..").click()
        input_element = driver.find_element_by_xpath("//input[@class='ant-calendar-input ']")
        input_element.send_keys(Keys.CONTROL + 'a')
        input_element.send_keys(Keys.DELETE)
        input_element.clear()
        driver.find_element_by_xpath("//input[@class='ant-calendar-input ']").send_keys(kargs.get("开始时间"))
        driver.find_element_by_xpath("//a[@class='ant-calendar-ok-btn' and @role='button']").click()

        driver.find_element_by_xpath(
            "//input[@class='ant-calendar-range-picker ant-input input-create-picker ' and @placeholder='截止时间']/..").click()
        input_element = driver.find_element_by_xpath("//input[@class='ant-calendar-input ']")
        input_element.send_keys(Keys.CONTROL + 'a')
        input_element.send_keys(Keys.DELETE)
        input_element.clear()
        driver.find_element_by_xpath("//input[@class='ant-calendar-input ']").send_keys(kargs.get("截止时间"))
        driver.find_element_by_xpath("//a[@class='ant-calendar-ok-btn' and @role='button']").click()
        driver.find_element_by_xpath(
            '//div[@class="dateTime-range-container-show"]//span[@class="base-btn-title"]/..').click()


def advanced_filter_item(driver, filter_name, *args, **kargs):
    advanced_filter_title = "//div[@class='searchform clearfix']//p[@class='AdvancedFilterTitle']"
    filter_cmp_type = get_filter_info(driver, filter_name)
    driver.find_element_by_xpath(advanced_filter_title).click()
    filter_name_xpath = f"//div[@class='AdvancedFilterInfo clearfix']//label[text()='{filter_name}']"
    if filter_cmp_type == "BC_TextBox":
        driver.find_element_by_xpath(f"{filter_name_xpath}/../..//input").clear()
        driver.find_element_by_xpath(f"{filter_name_xpath}/../..//input").send_keys(args)
    elif filter_cmp_type == 'BC_UserSelect':
        driver.find_element_by_xpath(f"{filter_name_xpath}/../..//ul").click()
        for arg in args:
            driver.find_element_by_xpath("//div[@class='base-search-component']//input").clear()
            driver.find_element_by_xpath("//div[@class='base-search-component']//input").send_keys(arg)
            time.sleep(1)
            driver.find_element_by_xpath("//div[@class='us-user-info']").click()
        driver.find_element_by_xpath(
            '//div[@class="us-container"]//span[@class="base-bg-ripple  base-btns-bgc-small  "]').click()
    elif filter_cmp_type == 'BC_DropDownList':
        driver.find_element_by_xpath(f"{filter_name_xpath}/../..//ul").click()
        for arg in args:
            driver.find_element_by_xpath(f"//span[@class='form-item__label' and text()='{arg}']").click()
        driver.find_element_by_xpath('//div[@id="DropdownList_ul"]//button[@class="btn btn_default btn_sm"]').click()
    elif filter_cmp_type == 'BC_DateTimeRange':
        driver.find_element_by_xpath(
            f"{filter_name_xpath}/../../..//input[@placeholder='开始时间']/..").click()
        input_element = driver.find_element_by_xpath("//input[@class='ant-calendar-input ']")
        input_element.send_keys(Keys.CONTROL + 'a')
        input_element.send_keys(Keys.DELETE)
        input_element.clear()
        driver.find_element_by_xpath("//input[@class='ant-calendar-input ']").send_keys(kargs.get("开始时间"))
        driver.find_element_by_xpath("//a[@class='ant-calendar-ok-btn' and @role='button']").click()
        driver.find_element_by_xpath(
            f"{filter_name_xpath}/../../..//input[@placeholder='截止时间']/..").click()
        input_element = driver.find_element_by_xpath("//input[@class='ant-calendar-input ']")
        input_element.send_keys(Keys.CONTROL + 'a')
        input_element.send_keys(Keys.DELETE)
        input_element.clear()
        driver.find_element_by_xpath("//input[@class='ant-calendar-input ']").send_keys(kargs.get("截止时间"))
        driver.find_element_by_xpath("//a[@class='ant-calendar-ok-btn' and @role='button']").click()
    driver.find_element_by_xpath("//div[@class='btnAllBorder']//span[@class='base-btn-title']/..").click()


def get_filter_info(driver, filter_name):
    driver.refresh()  # 重新获取index_page接口
    network_data = info(driver)
    network_data.reverse()
    for data in network_data:
        url = data.get('request').get('url')
        if '/api/v2/UI/IndexPage' in url:
            # 获取字段对应数据源
            response_data = json.loads(data.get('response_data').get('body'))
            filter_sub_cmps_list = response_data.get('sub_cmps').get('active_view').get('sub_cmps').get(
                'search_form').get('sub_cmps')
            for filter_sub_cmp in filter_sub_cmps_list:
                cmp_label = filter_sub_cmp.get('cmp_label')
                if cmp_label == filter_name:
                    cmp_type = filter_sub_cmp.get('cmp_type')
                    return cmp_type


def index_button_click(driver, btn_name):
    button_xpath = f"//span[@class='base-btn-title' and text()='{btn_name}']/.."
    driver.find_element_by_xpath(button_xpath).click()


def form_view_button_click(driver, btn_name):
    button_xpath = f"//div[@class='isFocusableButton']/span[text()='{btn_name}']"
    driver.find_element_by_xpath(button_xpath).click()


def enter_iframe(driver, element_str):
    """
    处理iframe跳转
    :param element_str
    :param driver
    """
    for i in driver.find_elements_by_xpath('//iframe'):
        driver.switch_to_frame(i)
        if isElementExist(driver, element_str):
            return
        else:
            driver.switch_to_default_content()
            continue


def form_button_click(driver, button_name):
    """
    :param driver
    :param button_name
    专用于表单区域的按钮点击
    """
    form_element_str = requests.get('http://8.141.50.128:5000/static/json_data/button_xpath_str.json'
                                    ).json().get('form_button_click')

    button_click(driver, form_element_str, button_name)


def list_button_click(driver, button_name):
    """
    :param driver
    :param button_name
    专用于表单区域的按钮点击
    """
    form_element_str = requests.get('http://8.141.50.128:5000/static/json_data/button_xpath_str.json'
                                    ).json().get('list_button_click')

    button_click(driver, form_element_str, button_name)


def view_tab_button_click(driver, button_name):
    """
    :param driver
    :param button_name
    专用于视图切换的按钮点击
    """
    form_element_str = requests.get('http://8.141.50.128:5000/static/json_data/button_xpath_str.json'
                                    ).json().get('view_tab_button_click')

    button_click(driver, form_element_str, button_name)


def view_button_click(driver, button_name):
    """
    专用于视图功能的按钮点击
    """
    form_element_str = requests.get('http://8.141.50.128:5000/static/json_data/button_xpath_str.json'
                                    ).json().get('view_button_click')
    button_click(driver, form_element_str, button_name)


def details_page_button_click(driver, button_name):
    """
    专用于详情页功能的按钮点击
    """
    form_element_str = requests.get('http://8.141.50.128:5000/static/json_data/button_xpath_str.json'
                                    ).json().get('details_page_button_click')

    button_click(driver, form_element_str, button_name)


def button_click(driver, form_element_str, button_name):
    """
    :param driver driver实例
    :param form_element_str 对应区域的str
    :param button_name 按钮名称
    """
    explicit_waiting(driver, '//iframe')
    time.sleep(0.5)
    if not isElementExist(driver, form_element_str):
        enter_iframe(driver, form_element_str)
    form_element = driver.find_element_by_xpath(form_element_str)

    for i in form_element.find_elements_by_xpath(f'//*[text()="{button_name}"]'):
        try:
            driver.execute_script("arguments[0].click();", i)
            time.sleep(0.5)
            break
        except ElementClickInterceptedException:
            continue
    driver.switch_to_default_content()
