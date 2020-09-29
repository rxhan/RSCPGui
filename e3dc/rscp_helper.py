# -*- coding: latin-1 -*-

import datetime
import hashlib
import time
import json
import traceback

from e3dc._rscp_dto import RSCPDTO
from e3dc.e3dc import E3DC
from e3dc.rscp_tag import RSCPTag
from e3dc.rscp_type import RSCPType


class rscp_helper():
    def __init__(self, username, password, host, rscp_pass):
        self.e3dc = E3DC(username, password, host, rscp_pass)

    def get_all(self, requests=None, raw=False):
        if not requests:
            requests = []
        requests += self.getBatData(bat_index=0, dcb_indexes=[0, 1])
        requests += self.getDCDCData(dcdc_indexes=[0, 1])
        requests += self.getEMSData()
        requests += self.getPMData(pm_indexes=[0, 1])
        requests += self.getPVIData()
        # requests += self.getEmergencyStatus()
        # requests += self.getSysSpecs()
        # requests += self.getInfo()

        return self.get_data(requests, raw)

    def getUserLevel(self):
        requests = []
        requests.append(RSCPTag.RSCP_REQ_USER_LEVEL)
        return requests


    def getCheckForUpdates(self):
        requests = []
        requests.append(RSCPTag.UM_REQ_CHECK_FOR_UPDATES)

        return requests

    def getUpdateStatus(self):
        requests = []
        requests.append(RSCPTag.UM_REQ_UPDATE_STATUS)

        return requests

    def getWB(self):
        # TODO: Werte auslesen und in der Oberfläche darstellen
        r = RSCPDTO(RSCPTag.WB_REQ_CONNECTED_DEVICES, rscp_type=RSCPType.Container)
        r += RSCPDTO(RSCPTag.WB_INDEX, rscp_type=RSCPType.UChar8, data = 0)
        r += RSCPTag.WB_REQ_STATUS
        return r

    def getInfo(self):
        requests = []
        requests.append(RSCPTag.INFO_REQ_PRODUCTION_DATE)
        requests.append(RSCPTag.INFO_REQ_SERIAL_NUMBER)
        requests.append(RSCPTag.INFO_REQ_SW_RELEASE)
        requests.append(RSCPTag.INFO_REQ_A35_SERIAL_NUMBER)
        requests.append(RSCPTag.INFO_REQ_TIME)
        requests.append(RSCPTag.INFO_REQ_TIME_ZONE)
        requests.append(RSCPTag.INFO_REQ_UTC_TIME)
        requests.append(RSCPTag.INFO_REQ_IP_ADDRESS)
        requests.append(RSCPTag.INFO_REQ_SUBNET_MASK)
        requests.append(RSCPTag.INFO_REQ_MAC_ADDRESS)
        requests.append(RSCPTag.INFO_REQ_GATEWAY)
        requests.append(RSCPTag.INFO_REQ_DNS)
        requests.append(RSCPTag.INFO_REQ_DHCP_STATUS)
        requests.append(RSCPTag.SRV_REQ_IS_ONLINE)
        requests.append(RSCPTag.SYS_REQ_IS_SYSTEM_REBOOTING)
        requests.append(RSCPTag.RSCP_REQ_USER_LEVEL)

        return requests

    def setChargePower(self, value=None):
        requests = []
        containerData = []
        if value:
            containerData.append(RSCPDTO(tag=RSCPTag.EMS_POWER_LIMITS_USED, data=True))
            containerData.append(RSCPDTO(tag=RSCPTag.EMS_MAX_CHARGE_POWER, data=value))
        else:
            containerData.append(RSCPDTO(tag=RSCPTag.EMS_POWER_LIMITS_USED, data=False))

        requests.append(RSCPDTO(tag=RSCPTag.EMS_REQ_SET_POWER_SETTINGS, data=containerData))

        return requests

    def getBatDcbData(self, bat_index=0, bat_indexes=None):
        if not bat_indexes:
            bat_indexes = [bat_index]

        requests = []

        for bat_index in bat_indexes:
            r = RSCPDTO(tag=RSCPTag.BAT_REQ_DATA)
            r += RSCPDTO(tag=RSCPTag.BAT_INDEX, data=bat_index)
            r += RSCPTag.BAT_REQ_DCB_COUNT

            data = self.get_data([r], True)

            requests += self.getBatData(bat_index = bat_index, dcb_indexes = range(0, data['BAT_DCB_COUNT'].data))

        return requests

    def getBatData(self, bat_index=0, bat_indexes=None, dcb_index=0, dcb_indexes=None):
        requests = []

        if not bat_indexes:
            bat_indexes = [bat_index]
        if not dcb_indexes and dcb_index:
            dcb_indexes = [dcb_index]

        for bat_index in bat_indexes:
            r = RSCPDTO(tag=RSCPTag.BAT_REQ_DATA)
            r += RSCPDTO(tag=RSCPTag.BAT_INDEX, data=bat_index)
            r += RSCPTag.BAT_REQ_USABLE_CAPACITY
            r += RSCPTag.BAT_REQ_USABLE_REMAINING_CAPACITY
            r += RSCPTag.BAT_REQ_ASOC
            r += RSCPTag.BAT_REQ_RSOC_REAL
            r += RSCPTag.BAT_REQ_MAX_BAT_VOLTAGE
            r += RSCPTag.BAT_REQ_MAX_CHARGE_CURRENT
            r += RSCPTag.BAT_REQ_EOD_VOLTAGE
            r += RSCPTag.BAT_REQ_MAX_DISCHARGE_CURRENT
            r += RSCPTag.BAT_REQ_CHARGE_CYCLES
            r += RSCPTag.BAT_REQ_TERMINAL_VOLTAGE
            r += RSCPTag.BAT_REQ_MAX_DCB_CELL_TEMPERATURE
            r += RSCPTag.BAT_REQ_MIN_DCB_CELL_TEMPERATURE
            r += RSCPTag.BAT_REQ_READY_FOR_SHUTDOWN
            r += RSCPTag.BAT_REQ_TRAINING_MODE
            r += RSCPTag.BAT_REQ_FCC
            r += RSCPTag.BAT_REQ_RC
            r += RSCPTag.BAT_REQ_INFO
            r += RSCPTag.BAT_REQ_DCB_COUNT
            r += RSCPTag.BAT_REQ_DEVICE_NAME
            r += RSCPTag.BAT_REQ_DEVICE_STATE
            r += RSCPTag.BAT_REQ_SPECIFICATION
            r += RSCPTag.BAT_REQ_INTERNALS

            if dcb_indexes:
                for dcb_index in dcb_indexes:
                    r += RSCPDTO(tag=RSCPTag.BAT_REQ_DCB_ALL_CELL_TEMPERATURES, data=dcb_index)
                    r += RSCPDTO(tag=RSCPTag.BAT_REQ_DCB_ALL_CELL_VOLTAGES, data=dcb_index)
                    r += RSCPDTO(tag=RSCPTag.BAT_REQ_DCB_INFO, data=dcb_index)

            requests.append(r)

        return requests

    def getDCDCData(self, dcdc_index=0, dcdc_indexes=None):
        requests = []

        if not dcdc_indexes:
            dcdc_indexes = [dcdc_index]

        for dcdc_index in dcdc_indexes:
            r = RSCPDTO(tag=RSCPTag.DCDC_REQ_DATA)
            r += RSCPDTO(tag=RSCPTag.DCDC_INDEX, data=dcdc_index)
            r += RSCPTag.DCDC_REQ_P_BAT
            r += RSCPTag.DCDC_REQ_P_DCL
            r += RSCPTag.DCDC_REQ_U_BAT
            r += RSCPTag.DCDC_REQ_U_DCL
            r += RSCPTag.DCDC_REQ_I_BAT
            r += RSCPTag.DCDC_REQ_I_DCL
            r += RSCPTag.DCDC_REQ_STATUS_AS_STRING
            r += RSCPTag.DCDC_REQ_FPGA_FIRMWARE
            r += RSCPTag.DCDC_REQ_FIRMWARE_VERSION
            r += RSCPTag.DCDC_REQ_SERIAL_NUMBER
            r += RSCPTag.DCDC_BOARD_VERSION
            requests.append(r)

        return requests

    def getEMSData(self):
        requests = []

        requests.append(RSCPTag.EMS_REQ_POWER_PV)
        requests.append(RSCPTag.EMS_REQ_POWER_BAT)
        requests.append(RSCPTag.EMS_REQ_POWER_HOME)
        requests.append(RSCPTag.EMS_REQ_POWER_GRID)
        requests.append(RSCPTag.EMS_REQ_POWER_ADD)
        requests.append(RSCPTag.EMS_REQ_BAT_SOC)
        requests.append(RSCPTag.EMS_REQ_AUTARKY)
        requests.append(RSCPTag.EMS_REQ_SELF_CONSUMPTION)
        requests.append(RSCPTag.EMS_REQ_COUPLING_MODE)

        requests.append(RSCPTag.EMS_REQ_BALANCED_PHASES)
        requests.append(RSCPTag.EMS_REQ_INSTALLED_PEAK_POWER)
        requests.append(RSCPTag.EMS_REQ_DERATE_AT_PERCENT_VALUE)
        requests.append(RSCPTag.EMS_REQ_DERATE_AT_POWER_VALUE)
        requests.append(RSCPTag.EMS_REQ_USED_CHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_USER_CHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_BAT_CHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_DCDC_CHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_USED_DISCHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_USER_DISCHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_BAT_DISCHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_DCDC_DISCHARGE_LIMIT)
        requests.append(RSCPTag.EMS_REQ_REMAINING_BAT_CHARGE_POWER)
        requests.append(RSCPTag.EMS_REQ_REMAINING_BAT_DISCHARGE_POWER)
        requests.append(RSCPTag.EMS_REQ_GET_IDLE_PERIODS)
        requests.append(RSCPTag.EMS_REQ_GET_POWER_SETTINGS)
        requests.append(RSCPTag.EMS_REQ_EMERGENCY_POWER_STATUS)

        requests.append(RSCPTag.EMS_REQ_MODE)
        requests.append(RSCPTag.EMS_REQ_EXT_SRC_AVAILABLE)
        requests.append(RSCPTag.EMS_REQ_BATTERY_BEFORE_CAR_MODE)
        requests.append(RSCPTag.EMS_REQ_BATTERY_TO_CAR_MODE)
        #requests.append(RSCPTag.EMS_REQ_GET_GENERATOR_STATE)
        requests.append(RSCPTag.EMS_REQ_EMERGENCYPOWER_TEST_STATUS)
        requests.append(RSCPTag.EMS_REQ_GET_SYS_SPECS)
        requests.append(RSCPTag.EMS_REQ_STORED_ERRORS)
        #requests.append(RSCPTag.EMS_REQ_ERROR_BUZZER_ENABLED)

        requests.append(RSCPTag.EMS_REQ_POWER_WB_ALL)
        requests.append(RSCPTag.EMS_REQ_POWER_WB_SOLAR)
        requests.append(RSCPTag.EMS_REQ_ALIVE)

        requests.append(RSCPTag.EMS_REQ_GET_MANUAL_CHARGE)

        requests.append(RSCPTag.EP_REQ_IS_READY_FOR_SWITCH)
        requests.append(RSCPTag.EP_REQ_IS_GRID_CONNECTED)
        requests.append(RSCPTag.EP_REQ_IS_ISLAND_GRID)
        requests.append(RSCPTag.EP_REQ_IS_POSSIBLE)
        requests.append(RSCPTag.EP_REQ_IS_INVALID_STATE)

        requests.append(RSCPTag.EMS_REQ_STATUS)

        return requests

    def getEmergencyStatus(self):
        requests = []

        requests.append(RSCPTag.EMS_REQ_EMERGENCY_POWER_STATUS)

        return requests

    def getSysSpecs(self):
        requests = []
        requests.append(RSCPTag.EMS_REQ_GET_SYS_SPECS)

        return requests

    def getPMData(self, pm_index=0, pm_indexes=None):
        requests = []
        if not pm_indexes:
            pm_indexes = [pm_index]

        for pm_index in pm_indexes:
            r = RSCPDTO(tag=RSCPTag.PM_REQ_DATA)
            r += RSCPDTO(tag=RSCPTag.PM_INDEX, data=pm_index)  # PM INDEX 0 = Leistungsmesser Netzbezug
            r += RSCPTag.PM_REQ_POWER_L1
            r += RSCPTag.PM_REQ_POWER_L2
            r += RSCPTag.PM_REQ_POWER_L3
            r += RSCPTag.PM_REQ_VOLTAGE_L1
            r += RSCPTag.PM_REQ_VOLTAGE_L2
            r += RSCPTag.PM_REQ_VOLTAGE_L3
            r += RSCPTag.PM_REQ_ENERGY_L1
            r += RSCPTag.PM_REQ_ENERGY_L2
            r += RSCPTag.PM_REQ_ENERGY_L3
            r += RSCPTag.PM_REQ_FIRMWARE_VERSION
            r += RSCPTag.PM_REQ_ACTIVE_PHASES
            r += RSCPTag.PM_REQ_MODE
            r += RSCPTag.PM_REQ_ERROR_CODE
            r += RSCPTag.PM_REQ_TYPE
            r += RSCPTag.PM_REQ_DEVICE_ID
            r += RSCPTag.PM_REQ_COMM_STATE
            r += RSCPTag.PM_REQ_IS_CAN_SILENCE
            r += RSCPTag.PM_REQ_DEVICE_STATE

            requests.append(r)

        return requests

    def getPVIData(self, pvi_index=0, pvi_indexes=None, phase=None, string=None):
        requests = []

        phases = phase if isinstance(phase,list) else [phase] if phase else phase
        strings = string if isinstance(string, list) else [string] if string else string

        if not pvi_indexes:
            pvi_indexes = [pvi_index]

        for pvi_index in pvi_indexes:
            r = RSCPDTO(tag=RSCPTag.PVI_REQ_DATA)
            r += RSCPDTO(tag=RSCPTag.PVI_INDEX, data=pvi_index)
            r += RSCPTag.PVI_REQ_AC_MAX_PHASE_COUNT
            r += RSCPTag.PVI_REQ_TEMPERATURE_COUNT
            r += RSCPTag.PVI_REQ_DC_MAX_STRING_COUNT
            data = self.get_data([r], True)

            tempcount = int(data['PVI_TEMPERATURE_COUNT'])

            if not phases:
                phases = range(0,int(data['PVI_AC_MAX_PHASE_COUNT']))

            if not strings:
                strings = range(0,int(data['PVI_DC_MAX_STRING_COUNT']))

            r = RSCPDTO(tag=RSCPTag.PVI_REQ_DATA)
            r += RSCPDTO(tag=RSCPTag.PVI_INDEX, data=pvi_index)
            r += RSCPTag.PVI_REQ_TEMPERATURE_COUNT
            r += RSCPTag.PVI_REQ_TYPE
            r += RSCPTag.PVI_REQ_SERIAL_NUMBER
            r += RSCPTag.PVI_REQ_VERSION
            r += RSCPTag.PVI_REQ_ON_GRID
            r += RSCPTag.PVI_REQ_STATE
            r += RSCPTag.PVI_REQ_LAST_ERROR
            r += RSCPTag.PVI_REQ_COS_PHI
            r += RSCPTag.PVI_REQ_VOLTAGE_MONITORING
            r += RSCPTag.PVI_REQ_POWER_MODE
            r += RSCPTag.PVI_REQ_SYSTEM_MODE
            r += RSCPTag.PVI_REQ_FREQUENCY_UNDER_OVER
            r += RSCPTag.PVI_REQ_AC_MAX_PHASE_COUNT
            r += RSCPTag.PVI_REQ_MAX_TEMPERATURE
            r += RSCPTag.PVI_REQ_MIN_TEMPERATURE
            r += RSCPTag.PVI_REQ_AC_MAX_APPARENTPOWER
            r += RSCPTag.PVI_REQ_DEVICE_STATE

            for phase in phases:
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_POWER, data=phase)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_VOLTAGE, data=phase)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_CURRENT, data=phase)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_APPARENTPOWER, data=phase)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_REACTIVEPOWER, data=phase)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_ENERGY_ALL, data=phase)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_AC_ENERGY_GRID_CONSUMPTION, data=phase)

            for string in strings:
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_DC_POWER, data=string)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_DC_VOLTAGE, data=string)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_DC_CURRENT, data=string)
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_DC_STRING_ENERGY_ALL, data=string)

            for temps in range(0,tempcount):
                r += RSCPDTO(tag=RSCPTag.PVI_REQ_TEMPERATURE, data=temps)

            requests.append(r)

        return requests

    def setCharge(self, state):
        return self.setIdlePeriod(0, state)

    def setDischarge(self, state):
        return self.setIdlePeriod(1, state)

    def setIdlePeriod(self, type=0, active=True, day=None, start='01:00', end='23:00'):
        if not day:
            day = datetime.datetime.today().weekday()
        periodData = []
        periodData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_TYPE, data=int(type)))
        periodData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_DAY, data=int(day)))
        periodData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_ACTIVE, data=active))
        timeData = []
        timeData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_HOUR, data=int(start[:2])))
        timeData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_MINUTE, data=int(start[3:])))
        periodData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_START, data=timeData))
        timeData = []
        timeData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_HOUR, data=int(end[:2])))
        timeData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_MINUTE, data=int(end[3:])))
        periodData.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD_END, data=timeData))

        data = []
        data.append(RSCPDTO(tag=RSCPTag.EMS_IDLE_PERIOD, rscp_type=RSCPType.Container, data=periodData))

        containerData = []
        containerData.append(RSCPDTO(tag=RSCPTag.EMS_REQ_SET_IDLE_PERIODS, rscp_type=RSCPType.Container, data=data))

        return containerData

    def get_data(self, requests, raw=False):
        responses = self.e3dc.send_requests(requests)
        if raw:
            if len(responses) == 1:
                return responses[0]
            else:
                rscp = RSCPDTO(tag=RSCPTag.LIST_TYPE, rscp_type=RSCPType.Container, data=responses)
                return rscp
        else:
            raise Exception('Deprecated')
