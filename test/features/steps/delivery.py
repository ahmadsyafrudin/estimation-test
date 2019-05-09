from http import HTTPStatus

from dateutil.parser import parse
from behave import given, when, then
from django.test import Client


@given("client want to order on {date} at {hour}")
def step_impl(context, date, hour):
    """
    :param hour: str
    :param date: str
    :type context: behave.runner.Context
    """
    context.estimation_type = "delivery"
    context.date = parse(f"{date} {hour}").isoformat()


@when("estimate for delivery")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    factory = Client()
    context.response = factory.post("/api/estimate/", data={"dateTime": context.date,
                                                            "estimationType": context.estimation_type},
                                    content_type="application/json")


@then("client get receive estimation on {date} at {hour}")
def step_impl(context, date, hour):
    """
    :param hour: str
    :param date: str
    :type context: behave.runner.Context
    """
    assert context.response.status_code == HTTPStatus.OK
    assert context.response.json().get("receive") == parse(f"{date} {hour}").isoformat()


@given("client want to estimate order on {date} at {hour}")
def step_impl(context, date, hour):
    """
    :param date: str
    :param hour: str
    :type context: behave.runner.Context
    """
    context.estimation_type = "delivery"
    context.date = parse(f"{date} {hour}").isoformat()


@when("estimate for delivery and tomorrow is holiday")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    factory = Client()
    context.response = factory.post("/api/estimate/", data={"dateTime": context.date,
                                                            "estimationType": context.estimation_type},
                                    content_type="application/json")


@then("client get process estimation not tomorrow, but on {date} at {hour}")
def step_impl(context, date, hour):
    """
    :param date:
    :param hour:
    :type context: behave.runner.Context
    """
    assert context.response.status_code == HTTPStatus.OK
    assert context.response.json().get("processing") == parse(f"{date} {hour}").isoformat()


@given("client want to estimate holiday order on {date} at {hour}")
def step_impl(context, date, hour):
    """
    :param date: str
    :param hour: str
    :type context: behave.runner.Context
    """
    context.estimation_type = "delivery"
    context.date = parse(f"{date} {hour}").isoformat()


@when("estimate for delivery on holiday")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    factory = Client()
    context.response = factory.post("/api/estimate/", data={"dateTime": context.date,
                                                            "estimationType": context.estimation_type},
                                    content_type="application/json")


@then("client can't do order because {holiday_name}")
def step_impl(context, holiday_name):
    """
    :param holiday_name: str
    :type context: behave.runner.Context
    """
    assert context.response.status_code == HTTPStatus.BAD_REQUEST
    assert holiday_name in context.response.json().get("message")


@given("client want to estimate weekend order on {date} at {hour}")
def step_impl(context, date, hour):
    """
    :param hour: str
    :param date: str
    :type context: behave.runner.Context
    """
    context.estimation_type = "delivery"
    context.date = parse(f"{date} {hour}").isoformat()


@when("estimate for delivery on weekend")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    factory = Client()
    context.response = factory.post("/api/estimate/", data={"dateTime": context.date,
                                                            "estimationType": context.estimation_type},
                                    content_type="application/json")


@then("client can't do order on {weekend_day}")
def step_impl(context, weekend_day):
    """
    :param weekend_day: str
    :type context: behave.runner.Context
    """
    assert context.response.status_code == HTTPStatus.BAD_REQUEST
    assert weekend_day in context.response.json().get("message")
