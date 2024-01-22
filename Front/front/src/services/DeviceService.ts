import axios from "axios";
import {Device} from "../models/Device.ts";
import {AlarmClockStatus} from "../models/AlarmClockStatus.ts";

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
}