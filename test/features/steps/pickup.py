from http import HTTPStatus

from dateutil.parser import parse
from behave import given, when, then
from django.test import Client


@given("client want to return on {date} at {hour}")
def step_impl(context, date, hour):
    """
    :param hour: str
    :param date: str
    :type context: behave.runner.Context
    """
    context.estimation_type = "return"
    context.date = parse(f"{date} {hour}").isoformat()


@when("estimate for return")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    factory = Client()
    context.response = factory.post("/estimate/", data={"date": context.date,
                                                        "estimation_type": context.estimation_type},
                                    content_type="application/json")


@then("client get pickup estimation on {date} at {hour}")
def step_impl(context, date, hour):
    """
    :param hour: str
    :param date: str
    :type context: behave.runner.Context
    """
    assert context.response.status_code == HTTPStatus.OK
    assert context.response.json().get("pick_up") == parse(f"{date} {hour}").isoformat()


@given("client estimate return on {date} at {hour}")
def step_impl(context, date, hour):
    """
    :param hour: str
    :param date: str
    :type context: behave.runner.Context
    """
    context.estimation_type = "return"
    context.date = parse(f"{date} {hour}").isoformat()


@when("estimate for pickup on Saturday")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    factory = Client()
    context.response = factory.post("/estimate/", data={"date": context.date,
                                                        "estimation_type": context.estimation_type},
                                    content_type="application/json")


@then("client get pickup and unbooked estimation on {date} at {hour}")
def step_impl(context, date, hour):
    """
    :param hour: str
    :param date: str
    :type context: behave.runner.Context
    """
    assert context.response.status_code == HTTPStatus.OK
    assert context.response.json().get("processedAndUnbooked") == parse(f"{date} {hour}").isoformat()


@given("client estimate two days before Election day on {date} at {hour}")
def step_impl(context, date, hour):
    """
    :param hour: str
    :param date: str
    :type context: behave.runner.Context
    """
    context.estimation_type = "return"
    context.date = parse(f"{date} {hour}").isoformat()


@when("estimate for return on Monday and pickup on Tuesday")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    factory = Client()
    context.response = factory.post("/estimate/", data={"date": context.date,
                                                        "estimation_type": context.estimation_type},
                                    content_type="application/json")


@then("client get estimation for pickup and unbooked on {date} at {hour}")
def step_impl(context, date, hour):
    """
    :param hour: str
    :param date: str
    :type context: behave.runner.Context
    """
    assert context.response.status_code == HTTPStatus.OK
    assert context.response.json().get("processedAndUnbooked") == parse(f"{date} {hour}").isoformat()


@given("client estimate on Election day on {day} at {hour}")
def step_impl(context, day, hour):
    """
    :param hour: str
    :param day: str
    :type context: behave.runner.Context
    """
    context.estimation_type = "return"
    context.date = parse(f"{day} {hour}").isoformat()


@when("estimate for return on Wednesday")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    factory = Client()
    context.response = factory.post("/estimate/", data={"date": context.date,
                                                        "estimation_type": context.estimation_type},
                                    content_type="application/json")


@then("client  cant get estimation for pickup and unbooked Because its {holiday_name}")
def step_impl(context, holiday_name):
    """
    :param holiday_name: str
    :type context: behave.runner.Context
    """
    assert context.response.status_code == HTTPStatus.BAD_REQUEST
    assert holiday_name in context.response.json().get("message")
