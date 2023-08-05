#!/usr/bin/python3

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

"""
Triggers module entities cache
"""

# Python base dependencies
import datetime
import uuid
from abc import ABC
from typing import Dict, List, Optional, Union

# Library dependencies
from fastnumbers import fast_float
from modules_metadata.triggers_module import (
    TriggerActionType,
    TriggerConditionOperator,
    TriggerConditionType,
    TriggerType,
)
from modules_metadata.types import ButtonPayload, SwitchPayload


class TriggerItem(ABC):
    """
    Trigger entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __trigger_id: uuid.UUID
    __name: str
    __comment: Optional[str]
    __enabled: bool

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        trigger_id: uuid.UUID,
        name: str,
        comment: Optional[str],
        enabled: bool,
    ) -> None:
        self.__trigger_id = trigger_id
        self.__name = name
        self.__comment = comment
        self.__enabled = enabled

    # -----------------------------------------------------------------------------

    @property
    def trigger_id(self) -> uuid.UUID:
        """Trigger identifier"""
        return self.__trigger_id

    # -----------------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Trigger user name"""
        return self.__name

    # -----------------------------------------------------------------------------

    @property
    def comment(self) -> Optional[str]:
        """Trigger user description"""
        return self.__comment

    # -----------------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """Flag informing if trigger is enabled"""
        return self.__enabled

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, int, bool, None]]:
        """Convert condition item to dictionary"""
        return {
            "id": self.trigger_id.__str__(),
            "name": self.name,
            "comment": self.comment,
            "enabled": self.enabled,
        }


class AutomaticTriggerItem(TriggerItem):
    """
    Automatic trigger entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    def to_dict(self) -> Dict[str, Union[str, int, bool, None]]:
        return {
            **{
                "type": TriggerType.AUTOMATIC.value,
            },
            **super().to_dict(),
        }


class ManualTriggerItem(TriggerItem):
    """
    Manual trigger entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    def to_dict(self) -> Dict[str, Union[str, int, bool, None]]:
        return {
            **{
                "type": TriggerType.MANUAL.value,
            },
            **super().to_dict(),
        }


class TriggerControlItem:
    """
    Trigger control entity base item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __id: uuid.UUID
    __name: str

    __trigger_id: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        trigger_id: uuid.UUID,
        control_id: uuid.UUID,
        control_name: str,
    ) -> None:
        self.__trigger_id = trigger_id

        self.__id = control_id
        self.__name = control_name

    # -----------------------------------------------------------------------------

    @property
    def trigger_id(self) -> uuid.UUID:
        """Control trigger identifier"""
        return self.__trigger_id

    # -----------------------------------------------------------------------------

    @property
    def control_id(self) -> uuid.UUID:
        """Control identifier"""
        return self.__id

    # -----------------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Control name"""
        return self.__name

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, str]:
        """Convert control item to dictionary"""
        return {
            "id": self.control_id.__str__(),
            "name": self.name,
            "trigger": self.trigger_id.__str__(),
        }


class ConditionItem(ABC):
    """
    Base condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __condition_id: uuid.UUID
    __trigger_id: uuid.UUID
    __enabled: bool

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
    ) -> None:
        self.__condition_id = condition_id
        self.__trigger_id = trigger_id
        self.__enabled = enabled

    # -----------------------------------------------------------------------------

    @property
    def condition_id(self) -> uuid.UUID:
        """Condition identifier"""
        return self.__condition_id

    # -----------------------------------------------------------------------------

    @property
    def trigger_id(self) -> uuid.UUID:
        """Condition identifier"""
        return self.__trigger_id

    # -----------------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """Flag informing if condition is enabled"""
        return self.__enabled

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, int, bool, List[int], None]]:
        """Convert condition item to dictionary"""
        return {
            "id": self.condition_id.__str__(),
            "trigger": self.trigger_id.__str__(),
            "enabled": self.enabled,
        }


class PropertyConditionItem(ConditionItem):
    """
    Base property condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __operator: TriggerConditionOperator
    __operand: Union[str, ButtonPayload, SwitchPayload]

    __device: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        operator: TriggerConditionOperator,
        operand: Union[str, ButtonPayload, SwitchPayload],
        device: uuid.UUID,
    ) -> None:
        super().__init__(condition_id, trigger_id, enabled)

        self.__operator = operator
        self.__operand = operand

        self.__device = device

    # -----------------------------------------------------------------------------

    @property
    def device(self) -> uuid.UUID:
        """Device identifier"""
        return self.__device

    # -----------------------------------------------------------------------------

    @property
    def operator(self) -> TriggerConditionOperator:
        """Property condition operator"""
        return self.__operator

    # -----------------------------------------------------------------------------

    @property
    def operand(self) -> Union[str, ButtonPayload, SwitchPayload]:
        """Property condition operand"""
        return self.__operand

    # -----------------------------------------------------------------------------

    def validate(self, property_value: Union[str, int, float, bool, SwitchPayload, ButtonPayload]) -> bool:
        """Property value validation"""
        if self.__operator == TriggerConditionOperator.EQUAL:
            return str(self.operand) == str(property_value)

        if self.__operator == TriggerConditionOperator.ABOVE:
            return fast_float(str(self.operand), 0) < fast_float(str(property_value), 0)

        if self.__operator == TriggerConditionOperator.BELOW:
            return fast_float(str(self.operand), 0) > fast_float(str(property_value), 0)

        return False

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, int, bool, List[int], None]]:
        return {
            **{
                "device": self.device.__str__(),
                "operator": self.operator.value,
                "operand": str(self.operand),
            },
            **super().to_dict(),
        }


class DevicePropertyConditionItem(PropertyConditionItem):
    """
    Device property condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __device_property: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        operator: TriggerConditionOperator,
        operand: Union[str, ButtonPayload, SwitchPayload],
        device_property: uuid.UUID,
        device: uuid.UUID,
    ) -> None:
        super().__init__(condition_id, trigger_id, enabled, operator, operand, device)

        self.__device_property = device_property

    # -----------------------------------------------------------------------------

    @property
    def device_property(self) -> uuid.UUID:
        """Device property identifier"""
        return self.__device_property

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, int, bool, List[int], None]]:
        return {
            **{
                "type": TriggerConditionType.DEVICE_PROPERTY.value,
                "property": self.device_property.__str__(),
            },
            **super().to_dict(),
        }


class ChannelPropertyConditionItem(PropertyConditionItem):
    """
    Channel property condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __channel_property: uuid.UUID
    __channel: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        operator: TriggerConditionOperator,
        operand: Union[str, ButtonPayload, SwitchPayload],
        channel_property: uuid.UUID,
        channel: uuid.UUID,
        device: uuid.UUID,
    ) -> None:
        super().__init__(condition_id, trigger_id, enabled, operator, operand, device)

        self.__channel_property = channel_property
        self.__channel = channel

    # -----------------------------------------------------------------------------

    @property
    def channel(self) -> uuid.UUID:
        """Channel identifier"""
        return self.__channel

    # -----------------------------------------------------------------------------

    @property
    def channel_property(self) -> uuid.UUID:
        """Channel property identifier"""
        return self.__channel_property

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, int, bool, List[int], None]]:
        return {
            **{
                "type": TriggerConditionType.CHANNEL_PROPERTY.value,
                "channel": self.channel.__str__(),
                "property": self.channel_property.__str__(),
            },
            **super().to_dict(),
        }


class TimeConditionItem(ConditionItem):
    """
    Time condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __time: datetime.timedelta
    __days: List[int]

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        time: datetime.timedelta,
        days: str,
    ) -> None:
        super().__init__(condition_id, trigger_id, enabled)

        self.__time = time
        self.__days = [int(x) for x in days.split(",")]

    # -----------------------------------------------------------------------------

    @property
    def time(self) -> datetime.timedelta:
        """Condition time"""
        return self.__time

    # -----------------------------------------------------------------------------

    @property
    def days(self) -> List[int]:
        """Condition days array"""
        return self.__days

    # -----------------------------------------------------------------------------

    def validate(
        self,
        date: datetime.datetime,
    ) -> bool:
        """Condition validation"""
        if date.isoweekday() not in self.days:
            return False

        return date.strftime("%H:%M:%S") == self.__format_time()

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, int, bool, List[int], None]]:
        return {
            **{
                "type": TriggerConditionType.TIME.value,
                "time": f"1970-01-01\\T{self.__format_time()}+00:00",
                "days": self.days,
            },
            **super().to_dict(),
        }

    # -----------------------------------------------------------------------------

    def __format_time(self) -> str:
        minutes, seconds = divmod(self.time.seconds, 60)
        hours, minutes = divmod(minutes, 60)

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


class DateConditionItem(ConditionItem):
    """
    Date condition entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __date: datetime.datetime

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        condition_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        date: datetime.datetime,
    ) -> None:
        super().__init__(condition_id, trigger_id, enabled)

        self.__date = date

    # -----------------------------------------------------------------------------

    @property
    def date(self) -> datetime.datetime:
        """Condition date"""
        return self.__date

    # -----------------------------------------------------------------------------

    def validate(
        self,
        date: datetime.datetime,
    ) -> bool:
        """Condition validation"""
        return date == self.date

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, int, bool, List[int], None]]:
        return {
            **{
                "type": TriggerConditionType.DATE.value,
                "date": self.date.strftime(r"%Y-%m-%d\T%H:%M:%S+00:00"),
            },
            **super().to_dict(),
        }


class ActionItem(ABC):
    """
    Base action entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __action_id: uuid.UUID
    __trigger_id: uuid.UUID
    __enabled: bool

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        action_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
    ) -> None:
        self.__action_id = action_id
        self.__trigger_id = trigger_id
        self.__enabled = enabled

    # -----------------------------------------------------------------------------

    @property
    def action_id(self) -> uuid.UUID:
        """Action identifier"""
        return self.__action_id

    # -----------------------------------------------------------------------------

    @property
    def trigger_id(self) -> uuid.UUID:
        """Action trigger identifier"""
        return self.__trigger_id

    # -----------------------------------------------------------------------------

    @property
    def enabled(self) -> bool:
        """Flag informing if action is enabled"""
        return self.__enabled

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, int, bool, None]]:
        """Convert condition item to dictionary"""
        return {
            "id": self.action_id.__str__(),
            "trigger": self.trigger_id.__str__(),
            "enabled": self.enabled,
        }


class PropertyActionItem(ActionItem):
    """
    Base property action entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __value: Union[str, ButtonPayload, SwitchPayload]

    __device: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        action_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        value: Union[str, ButtonPayload, SwitchPayload],
        device: uuid.UUID,
    ) -> None:
        super().__init__(action_id, trigger_id, enabled)

        self.__value = value

        self.__device = device

    # -----------------------------------------------------------------------------

    @property
    def device(self) -> uuid.UUID:
        """Device identifier"""
        return self.__device

    # -----------------------------------------------------------------------------

    @property
    def value(self) -> Union[str, ButtonPayload, SwitchPayload]:
        """Action property value to be set"""
        return self.__value

    # -----------------------------------------------------------------------------

    def validate(self, property_value: Union[str, int, float, bool, SwitchPayload, ButtonPayload]) -> bool:
        """Property value validation"""
        if isinstance(self.value, SwitchPayload) and self.value == SwitchPayload.TOGGLE:
            return False

        return str(self.value) == str(property_value)

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, int, bool, None]]:
        return {
            **{
                "device": self.device.__str__(),
                "value": str(self.value),
            },
            **super().to_dict(),
        }


class DevicePropertyActionItem(PropertyActionItem):
    """
    Device property action entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __device_property: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        action_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        value: Union[str, ButtonPayload, SwitchPayload],
        device_property: uuid.UUID,
        device: uuid.UUID,
    ) -> None:
        super().__init__(action_id, trigger_id, enabled, value, device)

        self.__device_property = device_property

    # -----------------------------------------------------------------------------

    @property
    def device_property(self) -> uuid.UUID:
        """Device property identifier"""
        return self.__device_property

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, int, bool, None]]:
        return {
            **{
                "type": TriggerActionType.DEVICE_PROPERTY.value,
                "property": self.device_property.__str__(),
            },
            **super().to_dict(),
        }


class ChannelPropertyActionItem(PropertyActionItem):
    """
    Channel property action entity item

    @package        FastyBird:TriggersModule!
    @module         items

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __channel_property: uuid.UUID
    __channel: uuid.UUID

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        action_id: uuid.UUID,
        trigger_id: uuid.UUID,
        enabled: bool,
        value: Union[str, ButtonPayload, SwitchPayload],
        channel_property: uuid.UUID,
        channel: uuid.UUID,
        device: uuid.UUID,
    ) -> None:
        super().__init__(action_id, trigger_id, enabled, value, device)

        self.__channel_property = channel_property
        self.__channel = channel

    # -----------------------------------------------------------------------------

    @property
    def channel(self) -> uuid.UUID:
        """Channel identifier"""
        return self.__channel

    # -----------------------------------------------------------------------------

    @property
    def channel_property(self) -> uuid.UUID:
        """Channel property identifier"""
        return self.__channel_property

    # -----------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Union[str, int, bool, None]]:
        return {
            **{
                "type": TriggerActionType.CHANNEL_PROPERTY.value,
                "channel": self.channel.__str__(),
                "property": self.channel_property.__str__(),
            },
            **super().to_dict(),
        }
