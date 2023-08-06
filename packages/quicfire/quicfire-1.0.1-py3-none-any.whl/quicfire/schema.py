# **************************************************
# Copyright (C) 2021 Holtz Forestry LLC DBA HOLTZ
#
# This file is part of QUIC-Fire API
#
# QUIC-Fire API can not be copied and/or distributed
# without the express permission of HOLTZ
# **************************************************

__author__ = "Lucas Wells"
__email__ = "lucas@holtztds.com"

from pydantic import BaseModel


class QfParamsIn(BaseModel):
    ff_export_id: str
    wind_speed: float = 0
    wind_direction: str = 'W'
    fmc_surface: float = 0.3
    fmc_canopy: float = 1.0
    sim_time: float = 100
    output_time: int = 30


class QfParamsEngine(QfParamsIn):
    job_id: str
