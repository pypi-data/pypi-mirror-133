#  Copyright (c) 2019-2022 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Supercube Typ B module.
"""

import logging
from hvl_ccb.configuration import configdataclass
from . import constants
from .base import (
    SupercubeBase,
    SupercubeOpcUaCommunication,
    SupercubeOpcUaCommunicationConfig,
)

logger = logging.getLogger(__name__)


@configdataclass
class SupercubeBOpcUaConfiguration(SupercubeOpcUaCommunicationConfig):
    endpoint_name: str = constants.SupercubeOpcEndpoint.B.value  # type: ignore


class SupercubeBOpcUaCommunication(SupercubeOpcUaCommunication):
    @staticmethod
    def config_cls():
        return SupercubeBOpcUaConfiguration


class SupercubeB(SupercubeBase):
    """
    Variant B of the Supercube without frequency converter but external safety switches.
    """

    @staticmethod
    def default_com_cls():
        return SupercubeBOpcUaCommunication
