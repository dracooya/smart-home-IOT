import {DeviceService} from "../services/DeviceService.ts";
import {
    Box,
    Button,
    Card,
    CardContent,
    CardMedia,
    Grid,
    ImageList,
    Tab,
    Tabs,
    Typography
} from "@mui/material";
import React, {useEffect, useRef} from "react";
import {Device} from "../models/Device.ts";
import {DeviceTypeEnum} from "../models/enums/DeviceTypeEnum.ts";
import SettingsIcon from '@mui/icons-material/Settings';
import io from 'socket.io-client';
import {RGBRemote} from "../RGBRemote/RGBRemote.tsx";
import {AlarmClockRemote} from "../AlarmClockRemote/AlarmClockRemote.tsx";
import {AlarmClockDialog} from "../AlarmClockDialog/AlarmClockDialog.tsx";
import {AlarmDialog} from "../AlarmDialog/AlarmDialog.tsx";
import {AlarmStatus} from "../models/AlarmStatus.ts";

interface DeviceStatusesProps {
    deviceService: DeviceService
}

interface TabPanelProps {
    children?: React.ReactNode;
    dir?: string;
    index: number;
    value: number;
}

function TabPanel(props: TabPanelProps) {
    const { children, value, index, ...other } = props;
    return (
        <Grid
            role="tabpanel"
            hidden={value !== index}
            id={`tabs-${index}`}
            aria-labelledby={`tabs-${index}`}
            {...other}>
            {value === index && (
                <Box sx={{ p: 3 }}>
                    <Typography>{children}</Typography>
                </Box>
            )}
        </Grid>
    );
}

function a11yProps(index: number) {
    return {
        id: `full-width-tab-${index}`,
        'aria-controls': `full-width-tabpanel-${index}`,
    };
}


export function DeviceStatuses({deviceService} : DeviceStatusesProps) {
    const [value, setValue] = React.useState(0);
    const [devices, setDevices] = React.useState<Device[]>([]);
    const [devicesStatuses, setDevicesStatuses] = React.useState<Map<string,string>>(new Map<string, string>());
    const shouldLoad = useRef(true);
    const [rgbRemoteOpen, setRgbRemoteOpen] = React.useState<boolean>(false);
    const [alarmClockRemoteOpen, setAlarmClockRemoteOpen] = React.useState<boolean>(false);
    const socket = io('http://localhost:5000');
    const [alarmClockOn, setAlarmClockOn] = React.useState<boolean>(false);
    const [lastAlarmClockTime, setLastAlarmClockTime] = React.useState<string>("");
    const [alarmStatuses, setAlarmStatuses] = React.useState<Map<string,object>>(new Map<string, AlarmStatus>());
    const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
        setValue(newValue);
    };

    const handleRgbRemoteOpen = () => {
        setRgbRemoteOpen(false);
    }

    const handleAlarmClockRemoteOpen = () => {
        setAlarmClockRemoteOpen(false);
    }

    const handleAlarmClockDialogClose = () => {
        setAlarmClockOn(false);
    }

    const handleAlarmDialogClose = (type: string) => {
        const obj_old = alarmStatuses.get(type) as AlarmStatus;
        obj_old.does_alarm_work = false
        setAlarmStatuses(alarmStatuses => new Map(alarmStatuses.set(type, { ...alarmStatuses.get(type), ...obj_old })));
        console.log(alarmStatuses);
    }

    useEffect(() => {
        if(!shouldLoad.current) return;
        deviceService.getDevices().then( response => {
            if (response.length > 0) {
                response.forEach(device => {
                    devicesStatuses.set(device.id, device.status)
                })
                setDevices(response);
            }
            shouldLoad.current = false;
        }).catch(err => console.log(err));

        deviceService.getAlarmClockStatus().then( response => {
            setLastAlarmClockTime(response.alarm_clock_time);
            setAlarmClockOn(response.does_alarm_clock_work);
        }).catch(err => console.log(err));

        deviceService.getAlarmStatus().then( response => {
            response.forEach(status => {
                alarmStatuses.set(status.alarm_type, status);
            })
        }).catch(err => console.log(err));

    }, []);

    useEffect(() => {
        socket.on('status', (message) => {
            const summary = JSON.parse(message);
            const newMap = new Map<string,string>(Object.entries(summary));
            setDevicesStatuses(newMap);
        });
        socket.on('alarm_clock_status', (alarm_clock_time) => {
            const json = JSON.parse(alarm_clock_time)
            setLastAlarmClockTime(json["alarm_clock_time"]);
            setAlarmClockOn(json["does_alarm_clock_work"]);
        });
        socket.on('alarm_status', (alarm_status) => {
            const json = JSON.parse(alarm_status)
            const type = json["alarm_type"];
            const status : AlarmStatus = {
                alarm_reason: json["alarm_reason"],
                does_alarm_work: json["does_alarm_work"],
                alarm_type: type
            };
            setAlarmStatuses(alarmStatuses => new Map(alarmStatuses.set(type, { ...alarmStatuses.get(type), ...status })));
        });
    }, []);


    return (
        <>
            <Grid container height={'100%'}>
                <Grid item xs={12} sm={12} md={12} lg={12} xl={12} alignItems={"flex-start"}>
                            <Tabs value={value} variant={'fullWidth'} onChange={handleChange} aria-label="tabs">
                                <Tab label="Device Statuses" {...a11yProps(0)} />
                                <Tab label="Device Charts" {...a11yProps(1)} />
                            </Tabs>
                        <TabPanel value={value} index={0}>
                            <Grid
                                item
                                xl={12}
                                lg={12}
                                md={12}
                                sm={12}
                                xs={12}
                                p={0}
                                style={{
                                    borderRadius: '1.5em',
                                    overflowY: 'auto',
                                }}
                                alignItems={'flex-start'}
                                mt={{xl: 0, lg: 0, md: 0, sm: '64px', xs: '64px'}}>
                                <ImageList  sx={{
                                    columnCount: {
                                        xs: '2 !important',
                                        sm: '4 !important',
                                        md: '4 !important',
                                        lg: '5 !important',
                                        xl: '5 !important',
                                    },
                                    width: "100%"}} cols={4} rowHeight={164}>
                                    {devices.map((device) => (
                                        <Card sx={{ display: 'flex',
                                            border:'1px solid #D3D3D3',
                                            borderRadius:'0.6em',
                                            padding:'0.5em',
                                            margin:'0.2em 0.1em',

                                            boxShadow:'none'}}
                                              key={device.id}>
                                            <Box sx={{ display: 'flex', flexDirection: 'column', width:'250px' }}>
                                                <CardContent sx={{ flex: '1 0 auto' }}>
                                                    <Typography  mb={1}>
                                                        <b>{device.name}</b>
                                                    </Typography>

                                                    <Typography variant="h5" alignItems={'center'} color="text.secondary">
                                                        <b>{devicesStatuses.get(device.id)}</b>
                                                    </Typography>

                                                </CardContent>
                                                {device.type == DeviceTypeEnum.RGB || device.type == DeviceTypeEnum.ALARM ?
                                                <Box sx={{ display: 'flex', justifyContent:'center', width:'100%', alignItems: 'center', pl: 1, pb: 1 }}>
                                                    <Button variant="contained" startIcon={<SettingsIcon />}
                                                        onClick={() => {
                                                            device.type == DeviceTypeEnum.RGB ? setRgbRemoteOpen(true) : setAlarmClockRemoteOpen(true);
                                                        }}>
                                                        Settings
                                                    </Button>
                                                </Box>
                                                : null }
                                            </Box>
                                            <CardMedia
                                                component="img"
                                                sx={{ width: 151 }}
                                                image={device.type == "DHT" ? "../dht.png" :
                                                       device.type == "FOUR_SD" ? "../4sd.png" :
                                                       device.type == "LED" ? "../led.png" :
                                                       device.type == "RGB" ? "../rgb.png" :
                                                       device.type == "PIR" ? "../pir.png" :
                                                       device.type == "GYRO" ? "../gyro.png" :
                                                       device.type == "BUZZER" ? "../buzzer.png" :
                                                       device.type == "ALARM" ? "../alarm.png" :
                                                       device.type == "UDS" ? "../uds.png" :
                                                       device.type == "DMS" ? "../keypad.png" :
                                                       device.type == "DS" ? "../door.png" :
                                                       device.type == "LCD" ? "../lcd.png" :
                                                       device.type == "IR" ? "../ir.png" : ""
                                                }
                                                alt="Device image"
                                            />
                                        </Card>
                                    ))}
                                </ImageList>
                            </Grid>
                        </TabPanel>
                        <TabPanel value={value} index={1}>
                            <iframe src="http://localhost:3000/public-dashboards/1dee33112b164846abd2142c38e20895" width="100%" height="700px"></iframe>
                        </TabPanel>
                </Grid>
                <RGBRemote open={rgbRemoteOpen} handleClose={handleRgbRemoteOpen} socket={socket}></RGBRemote>
                <AlarmClockRemote open={alarmClockRemoteOpen} handleClose={handleAlarmClockRemoteOpen} socket={socket}></AlarmClockRemote>
                <AlarmClockDialog open={alarmClockOn} handleClose={handleAlarmClockDialogClose} lastAlarmClockTime={lastAlarmClockTime} socket={socket}></AlarmClockDialog>
                {Array.from(alarmStatuses.entries()).map(([key, status]) => (
                    <AlarmDialog open={(status as AlarmStatus).does_alarm_work}
                                 handleClose={() => handleAlarmDialogClose(key)}
                                 reason={(status as AlarmStatus).alarm_reason}
                                 alarmType={(status as AlarmStatus).alarm_type}
                                 deviceService={deviceService}></AlarmDialog>
                ))}
                </Grid>
        </>
    );
}