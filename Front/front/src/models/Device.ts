import {DeviceTypeEnum} from "./enums/DeviceTypeEnum.ts";

export interface Device {
    type: DeviceTypeEnum,
    id: string,
    name: string,
    status: string,
}