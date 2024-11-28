import allure

from pages.app_page import app_page


@allure.severity('critical')
@allure.label('UI')
@allure.label("owner", "Zosimov")
@allure.feature('Mobile registration')
@allure.story('Mobile registration new user by email')
@allure.title('Mobile app open and choose registration by email')
def test_app_open_and_registration_by_email():
    app_page.open_start_page_and_click_continue()
    app_page.update_window_detect_and_close()
    app_page.welcome_window_and_email_input()
