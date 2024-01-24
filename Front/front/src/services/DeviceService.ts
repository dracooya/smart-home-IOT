import axios from "axios";
import {Device} from "../models/Device.ts";
import {AlarmClockStatus} from "../models/AlarmClockStatus.ts";
import {Password} from "../models/Password.ts";
import {AlarmStatus} from "../models/AlarmStatus.ts";

export class DeviceService {
    private api_host = "http://localhost:5000"

    public getDevices(): Promise<Device[]> {
        return axios({
            method: 'GET',
            url: `${this.api_host}/all`,
        }).then((response) => response.data
        ).catch((err) => {
            throw err
        });
    }

    public getAlarmClockStatus() : Promise<AlarmClockStatus> {
        return axios({
            method: 'GET',
            url: `${this.api_host}/alarm_clock_status`,
        }).then((response) => response.data
        ).catch((err) => {
            throw err
        });
    }


    public disableAlarm(password : Password, alarmType: string) : Promise<string> {
        return axios({
            method: 'PUT',
            url: `${this.api_host}/alarm_disable/${alarmType}`,
            data: password
        }).then((response) => response.data
        ).catch((err) => {
            throw err
        });
    }

    public getAlarmStatus() : Promise<AlarmStatus[]> {
        return axios({
            method: 'GET',
            url: `${this.api_host}/alarm_status`,
        }).then((response) => response.data
        ).catch((err) => {
            throw err
        });
    }
}