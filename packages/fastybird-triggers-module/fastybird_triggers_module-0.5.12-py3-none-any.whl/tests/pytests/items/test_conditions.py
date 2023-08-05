#     Copyright 2021. FastyBird s.r.o.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

# Test dependencies
import datetime
import uuid
from kink import inject

# Library libs
from triggers_module.items import PropertyConditionItem, ChannelPropertyConditionItem, TimeConditionItem
from triggers_module.repositories import ConditionsRepository

# Tests libs
from tests.pytests.tests import DbTestCase


class TestConditionItem(DbTestCase):
    @inject
    def test_transform_to_dict(self, condition_repository: ConditionsRepository) -> None:
        condition_repository.initialize()

        condition_item = condition_repository.get_by_id(
            uuid.UUID("2726f19c-7759-440e-b6f5-8c3306692fa2", version=4)
        )

        self.assertIsInstance(condition_item, PropertyConditionItem)
        self.assertIsInstance(condition_item, ChannelPropertyConditionItem)

        self.assertEqual({
            "id": "2726f19c-7759-440e-b6f5-8c3306692fa2",
            "type": "channel-property",
            "enabled": False,
            "trigger": "2cea2c1b-4790-4d82-8a9f-902c7155ab36",
            "device": "28989c89-e7d7-4664-9d18-a73647a844fb",
            "channel": "5421c268-8f5d-4972-a7b5-6b4295c3e4b1",
            "property": "ff7b36d7-a0b0-4336-9efb-a608c93b0974",
            "operand": "3",
            "operator": "eq",
        }, condition_item.to_dict())

        condition_item = condition_repository.get_by_id(
            uuid.UUID("09c453b3-c55f-4050-8f1c-b50f8d5728c2", version=4)
        )

        self.assertIsInstance(condition_item, TimeConditionItem)

        self.assertEqual({
            "id": "09c453b3-c55f-4050-8f1c-b50f8d5728c2",
            "type": "time",
            "enabled": False,
            "trigger": "1b17bcaa-a19e-45f0-98b4-56211cc648ae",
            "time": r"1970-01-01\T07:30:00+00:00",
            "days": [1, 2, 3, 4, 5, 6, 7],
        }, condition_item.to_dict())

    # -----------------------------------------------------------------------------

    @inject
    def test_validate(self, condition_repository: ConditionsRepository) -> None:
        condition_repository.initialize()

        condition_item = condition_repository.get_by_id(
            uuid.UUID("2726f19c-7759-440e-b6f5-8c3306692fa2", version=4)
        )

        self.assertIsInstance(condition_item, PropertyConditionItem)
        self.assertIsInstance(condition_item, ChannelPropertyConditionItem)

        self.assertTrue(condition_item.validate("3"))

        self.assertFalse(condition_item.validate("1"))

        condition_item = condition_repository.get_by_id(
            uuid.UUID("09c453b3-c55f-4050-8f1c-b50f8d5728c2", version=4)
        )

        self.assertIsInstance(condition_item, TimeConditionItem)

        self.assertTrue(condition_item.validate(datetime.datetime(1970, 1, 1, 7, 30)))
        self.assertTrue(condition_item.validate(datetime.datetime(2021, 9, 14, 7, 30)))

        self.assertFalse(condition_item.validate(datetime.datetime(1970, 1, 1, 7, 31)))
        self.assertFalse(condition_item.validate(datetime.datetime(2021, 9, 14, 7, 31)))
