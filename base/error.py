class Error:
    """
    错误代码类
    """
    ERROR_COUNT = 2048
    PASSWORD_LENGTH = 2047
    NOT_FOUND_ORDER = 2046
    ERROR_STATUS = 2045
    NOT_FOUND_USER = 2044
    NOT_YOUR_BUTTON = 2043
    NOT_BELONG_CATEGORY = 2042
    NOT_FOUND_BUTTON = 2041
    EXIST_BUTTON = 2040
    FAILED_UPLOAD = 2039
    ILLEGAL_PIC = 2038
    PIC_SIZE = 2037
    NOT_FOUND_CATEGORY = 2036
    NOT_FOUND_CARD = 2035
    ERROR_SEND_PHONE_CAPTCHA = 2034
    STORE = 2033
    PRICE = 2032
    DESCRIPTION_LENGTH = 2031
    GOOD_NAME_LENGTH = 2030
    ERROR_CATEGORY_CREATE = 2029
    CATEGORY_NAME_LENGTH = 2028
    REAL_NAME_LENGTH = 2027
    ADDRESS_LENGTH = 2026
    REQUIRE_SELLER = 2025
    NOT_YOUR_CARD = 2024
    ERROR_ORDER_STATUS = 2023
    NOT_YOUR_GOOD = 2022
    ERROR_PAGE = 2021
    ERROR_ORDER_CREATE = 2020
    REQUIRE_ADD_DEFAULT_CARD = 2019
    REQUIRE_COMPLETE_BUYER_INFO = 2018
    LACK_STORE = 2017
    REQUIRE_SET_BUTTON = 2016
    BUY_NUM = 2015
    ERROR_BUTTON_CREATE = 2014
    REQUIRE_BUYER = 2013
    DELETED_GOOD = 2012
    NOT_FOUND_GOOD = 2011
    ERROR_CARD_CREATE = 2010
    ERROR_GOOD_CREATE = 2009
    ERROR_USER_CREATE = 2008
    PHONE_FORMAT = 2007
    USERNAME_LENGTH = 2006
    BRAND_LENGTH = 2005

    ERROR_PHONE_CAPTCHA = 2004
    EXIST_USERNAME = 2003
    NOT_FOUND_USERNAME = 2001
    ERROR_PASSWORD = 2000

    ERROR_METHOD = 1004
    REQUIRE_LOGIN = 1003
    REQUIRE_JSON = 1002
    REQUIRE_PARAM = 1001
    NOT_FOUND_ERROR = 1000
    OK = 0

    # 错误说明
    ERROR_TUPLE = (
        (ERROR_COUNT, '错误的每页条数'),
        (PASSWORD_LENGTH, '密码应长于6个字符'),
        (NOT_FOUND_ORDER, '不存在的订单'),
        (ERROR_STATUS, '错误的订单状态'),
        (NOT_FOUND_USER, '不存在的用户'),
        (NOT_YOUR_BUTTON, '不是你的按钮'),
        (NOT_BELONG_CATEGORY, '当前商品不属于此类别'),
        (NOT_FOUND_BUTTON, '不存在的按钮设置'),
        (EXIST_BUTTON, '已存在的按钮设置'),
        (FAILED_UPLOAD, '图片上传失败'),
        (ILLEGAL_PIC, '图片解析错误'),
        (PIC_SIZE, '图片过大'),
        (NOT_FOUND_CATEGORY, '不存在的类别'),
        (NOT_FOUND_CARD, '不存在的银行卡'),
        (ERROR_SEND_PHONE_CAPTCHA, '手机验证码发送失败'),
        (STORE, '错误的商品库存'),
        (PRICE, '错误的商品价格'),
        (DESCRIPTION_LENGTH, '商品描述长度应在512个字符之内'),
        (GOOD_NAME_LENGTH, '商品名应在1-20个字符之间'),
        (ERROR_CATEGORY_CREATE, '创建类别失败'),
        (CATEGORY_NAME_LENGTH, '类别名应在2-20个字符之间'),
        (REAL_NAME_LENGTH, '真实姓名长度应在32个字符之内'),
        (ADDRESS_LENGTH, '地址长度应在512个字符之内'),
        (REQUIRE_BUYER, '需要登录商家用户'),
        (NOT_YOUR_CARD, '不是你的银行卡'),
        (ERROR_ORDER_STATUS, '订单状态无法变更'),
        (NOT_YOUR_GOOD, '不是你的订单'),
        (ERROR_PAGE, '错误的订单页数'),
        (ERROR_ORDER_CREATE, '创建订单失败'),
        (REQUIRE_ADD_DEFAULT_CARD, '需要设置默认银行卡'),
        (REQUIRE_COMPLETE_BUYER_INFO, '需要完善用户收货信息'),
        (LACK_STORE, '库存不足'),
        (REQUIRE_SET_BUTTON, '需要设置购买商品'),
        (BUY_NUM, '购买数量必须是正整数'),
        (ERROR_BUTTON_CREATE, '创建按钮设置错误'),
        (REQUIRE_BUYER, '需要登录买家用户'),
        (DELETED_GOOD, '商品被删除'),
        (NOT_FOUND_GOOD, '不存在的商品'),
        (ERROR_CARD_CREATE, '创建银行卡失败'),
        (ERROR_GOOD_CREATE, '创建商品失败'),
        (ERROR_USER_CREATE, '创建用户失败'),
        (PHONE_FORMAT, '手机号输入不准确'),
        (USERNAME_LENGTH, '用户名应在4-20个字符之间'),
        (BRAND_LENGTH, '品牌名称应在2-32个字符之间'),
        (ERROR_PHONE_CAPTCHA, "手机验证码错误"),
        (EXIST_USERNAME, "已存在的用户名"),
        (NOT_FOUND_USERNAME, "不存在的用户名"),
        (ERROR_PASSWORD, "错误的用户名或密码"),

        (ERROR_METHOD, '错误的HTTP请求方法'),
        (REQUIRE_LOGIN, "需要登录"),
        (REQUIRE_JSON, "需要JSON数据"),
        (REQUIRE_PARAM, "缺少参数"),
        (NOT_FOUND_ERROR, "不存在的错误"),
        (OK, "没有错误"),
    )
