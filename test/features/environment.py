from behave import use_fixture
from django.core.management import call_command

from test.features.behave_fixtures import django_test_runner, django_test_case


def before_all(context):
    use_fixture(django_test_runner, context)
    call_command('loaddata', "test/fixtures/holiday")


def before_scenario(context, scenario):
    use_fixture(django_test_case, context)

