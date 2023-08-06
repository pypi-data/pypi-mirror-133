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

# External imports
import requests

# Internal imports
from .schema import QfParamsIn, QfParamsEngine

# Define base URL for API calls
base_url = 'https://api.quicfire.com'


class QfJob(QfParamsEngine):
    """
    Class returned by a the run method. Stores the job_id and handles post job run API calls.

    Args:
        QfParamsEngine (pydantic.BaseModel): Schema for QUIC-Fire engine parameters
    """

    def get_status(self) -> dict:
        """
        Fetches the status for the current job_id

        Returns:
            dict: Status endpoint response
        """

        resp = requests.get(f'{base_url}/jobs/{self.job_id}')
        return resp.json()

    def get_metrics(self) -> dict:
        """
        Fetches the metrics for the current job_id

        Returns:
            dict: Metrics endpoint response
        """

        resp = requests.get(f'{base_url}/jobs/{self.job_id}/metrics')
        return resp.json()


def run(**kwargs) -> QfJob:
    """
    Main userspace entry for the SDK. Kicks off a QF run job and return a QfJob object

    Returns:
        QfJob: Class object for calling additional API enpoints for the job
    """

    # Scheme validation
    qf_params_in = QfParamsIn(**kwargs)

    # Build payload and send post request to API
    payload = qf_params_in.dict()
    resp = requests.post(f'{base_url}/', json=payload)

    return QfJob(**resp.json())
