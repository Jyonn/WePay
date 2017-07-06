class Error:
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
    NEED_LOGIN = 1003
    REQUIRE_JSON = 1002
    REQUIRE_PARAM = 1001
    NOT_FOUND_ERROR = 1000
    OK = 0

    ERROR_TUPLE = (
        (ERROR_CATEGORY_CREATE, '创建类别失败'),
        (CATEGORY_NAME_LENGTH, '类别名应在2-20个字符之间'),
        (REAL_NAME_LENGTH, '真实姓名长度应在32个字符之内'),
        (ADDRESS_LENGTH, '地址长度应在512个字符之内'),
        (REQUIRE_BUYER, '需要登录商家用户'),
        (NOT_YOUR_CARD, '不是你的银行卡'),
        (ERROR_ORDER_STATUS, '订单状态无法变更'),
        (NOT_YOUR_GOOD, '不是你的订单'),
        (ERROR_PAGE, '错误的页数'),
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

        (NEED_LOGIN, "需要登录"),
        (REQUIRE_JSON, "需要JSON数据"),
        (REQUIRE_PARAM, "缺少参数"),
        (NOT_FOUND_ERROR, "不存在的错误"),
        (OK, "没有错误"),
    )
