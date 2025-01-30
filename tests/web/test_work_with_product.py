import allure
import pytest

from pages.main_page import main_page
from pages.product_page import product_page
from tests import conftest
from tests.marks import microservice, layer, owner, tm4j, jira_issues

pytestmark = [
    layer("web"),
    owner("zosimov"),
    allure.feature("Registration")
]

OWNER = "allure-framework"
REPO = "allure2"


class DATA:
    address = 'Mainski put'
    cafe_name = 'Garden Caffe'
    meal_type = 'Burgeri'
    meal_first = 'Garden burger 200 gr'
    meal_second = 'Double cheeseburger 200 gr'
    extra_first = 'Pomfrit 200 gr'
    extra_second = 'Fanta 0.33 l'


@tm4j("ZM-T14")
@jira_issues("ZM-4")
@microservice("cart-service")
@allure.severity('critical')
@allure.feature('Products')
@allure.story('Add, edit and delete products in cart')
@allure.title('Test adding, editing and deleting products in cart')
@conftest.web
@pytest.mark.web
def test_add_edit_delete_products_in_cart():
    main_page.open()

    product_page.address_input_and_check(DATA.address)
    product_page.cafe_name_input_and_check(DATA.cafe_name)

    product_page.meal_type(DATA.meal_type)
    product_page.meal_name(DATA.meal_first)
    product_page.add_meal_to_cart_and_check(DATA.meal_first)
    product_page.meal_name(DATA.meal_second)
    product_page.add_meal_to_cart_and_check(DATA.meal_second)

    product_page.edit_extra_for_meal(DATA.meal_second, DATA.extra_first)
    product_page.edit_extra_for_meal(DATA.meal_first, DATA.extra_second)
    product_page.edit_extra_for_meal(DATA.meal_second, DATA.extra_first)

    product_page.increase_qty_for_meal(DATA.meal_second)
    product_page.reduce_qty_for_meal(DATA.meal_first)
    product_page.reduce_qty_for_meal(DATA.meal_second)
    product_page.reduce_qty_for_meal(DATA.meal_second)
