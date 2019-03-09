"""Factories for all models in the project."""
from datetime import timedelta, datetime

import factory
import random

from timeless.db import DB
from timeless.employees import models as employee_models
from timeless.restaurants import models as restaurants_models
from timeless.roles import models as role_models
from timeless.companies import models as company_models
from timeless.restaurants import models as restaurant_models
from timeless.items import models as item_models
from timeless.schemetypes import models as schemetypes_models


class DictMixin:

    @classmethod
    def get_dict(cls):
        instance = cls.build()
        # convert instance to dict
        return {
            column.name: str(getattr(instance, column.name))
            for column in instance.__table__.columns
        }


class TableShapeFactory(factory.alchemy.SQLAlchemyModelFactory):
    """ Factory for creating TableShape instance. """
    description = factory.Faker("text")
    picture = factory.Faker("text")

    class Meta:
        model = restaurants_models.TableShape
        sqlalchemy_session = DB.session
        sqlalchemy_session_persistence = "commit"


class EmployeeFactory(factory.alchemy.SQLAlchemyModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttribute(
        lambda emp: f'{emp.first_name}{emp.last_name}'[:15])
    phone_number = factory.Faker("phone_number")
    birth_date = factory.Faker("date")
    registration_date = factory.Faker("date")
    account_status = factory.Faker("text")
    user_status = factory.Faker("text")
    email = factory.Faker("email")
    password = factory.Faker("text")
    pin_code = factory.LazyAttribute(lambda _: random.randint(1, 9999))
    comment = "Test comment"

    class Meta:
        model = employee_models.Employee
        sqlalchemy_session = DB.session
        sqlalchemy_session_persistence = "commit"


class CompanyFactory(factory.alchemy.SQLAlchemyModelFactory):
    name = factory.Faker("text")
    code = factory.Faker("text")
    address = factory.Faker("text")

    class Meta:
        model = company_models.Company
        sqlalchemy_session = DB.session
        sqlalchemy_session_persistence = "commit"


class ItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    name = factory.Faker("text")
    stock_date = factory.Faker("date")
    comment = factory.Faker("text")
    created_on = factory.Faker("date")
    updated_on = factory.Faker("date")

    class Meta:
        model = item_models.Item
        sqlalchemy_session = DB.session
        sqlalchemy_session_persistence = "commit"


class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):
    works_on_shifts = True

    class Meta:
        model = role_models.Role
        sqlalchemy_session = DB.session
        sqlalchemy_session_persistence = "commit"


class TableFactory(factory.alchemy.SQLAlchemyModelFactory):
    name = factory.Faker("text")
    x = factory.Faker("pyint")
    y = factory.Faker("pyint")
    width = factory.Faker("pyint")
    height = factory.Faker("pyint")
    status = factory.Iterator([0, 1])
    max_capacity = factory.Faker("pyint")
    multiple = factory.Faker("boolean", chance_of_getting_true=50)
    playstation = factory.Faker("boolean", chance_of_getting_true=50)

    class Meta:
        model = restaurants_models.Table
        sqlalchemy_session = DB.session
        sqlalchemy_session_persistence = "commit"


class FloorFactory(factory.alchemy.SQLAlchemyModelFactory):
    description = factory.Faker("text")

    class Meta:
        model = restaurant_models.Floor
        sqlalchemy_session = DB.session
        sqlalchemy_session_persistence = "commit"


class ReservationFactory(factory.alchemy.SQLAlchemyModelFactory):
    num_of_persons = factory.Faker("pyint")
    comment = factory.Faker("text")
    start_time = datetime.now().replace(microsecond=0)
    status = restaurant_models.RESERVATION_STATUS[2][0]

    class Meta:
        model = restaurant_models.Reservation
        sqlalchemy_session = DB.session
        sqlalchemy_session_persistence = "commit"

    @factory.lazy_attribute
    def end_time(self):
        return self.start_time + timedelta(days=3)


class SchemeTypeFactory(factory.alchemy.SQLAlchemyModelFactory):
    description = factory.Faker("text")
    default_value = factory.Faker("text")
    value_type = factory.Faker("text")

    class Meta:
        model = schemetypes_models.SchemeType
        sqlalchemy_session = DB.session
        sqlalchemy_session_persistence = "commit"


class LocationFactory(DictMixin, factory.alchemy.SQLAlchemyModelFactory):
    name = factory.Faker("text")
    code = factory.Faker("text")
    country = factory.Faker("text")
    region = factory.Faker("text")
    city = factory.Faker("text")
    address = factory.Faker("text")
    longitude = factory.Faker("text")
    latitude = factory.Faker("text")
    type = factory.Faker("text")
    status = factory.Faker("text")
    comment = factory.Faker("text")

    class Meta:
        model = restaurant_models.Location
        sqlalchemy_session = DB.session
        sqlalchemy_session_persistence = "commit"

    @classmethod
    def get_edit_fields_dict(cls):
        location = cls.get_dict()
        excluded_fields = [
            'poster_id', 'closed_days', 'id',
            'working_hours', 'company_id', 'synchronized_on'
        ]
        for field in excluded_fields:
            location.pop(field, None)

        return location
