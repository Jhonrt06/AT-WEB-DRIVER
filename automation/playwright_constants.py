"""
CSS selector constants for Amazon page elements.
"""

SELECTORS_AMAZON = {
    "login_button_home": "#nav-link-accountList",  # "Hello, Sign in" button
    "email": "#ap_email_login",
    "continue": "#continue",
    "password": "#ap_password",
    "submit": "#signInSubmit",
    "hamburger_menu": "#nav-hamburger-menu",
    "hamburger_option_template":'a.hmenu-item >> text="{text}"',
}
