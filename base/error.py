class Error:
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
