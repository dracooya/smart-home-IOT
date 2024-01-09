import {DeviceService} from "../services/DeviceService.ts";
import {Box, Button, Card, CardContent, CardMedia, Grid, ImageList, Tab, Tabs, Typography} from "@mui/material";
import React, {useEffect, useRef} from "react";
import {Device} from "../models/Device.ts";
import {DeviceTypeEnum} from "../models/enums/DeviceTypeEnum.ts";
import SettingsIcon from '@mui/icons-material/Settings';
import io from 'socket.io-client';

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
    const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
        setValue(newValue);
    };

    useEffect(() => {
        if(!shouldLoad.current) return;
        deviceService.getDevices().then( response => {
            if (response.length > 0) {
                response.forEach(device => {
                    devicesStatuses.set(device.id, device.status)
                })
                setDevices(response);
            }
            setDevices(response);
            shouldLoad.current = false;
        }).catch(err => console.log(err));

    }, []);

    useEffect(() => {
        const socket = io('http://localhost:5000');
        socket.on('status', (message) => {
            const summary = JSON.parse(message);
            const newMap = new Map<string,string>(Object.entries(summary));
            setDevicesStatuses(newMap);
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
                                                    <Button variant="contained" startIcon={<SettingsIcon />}>
                                                        Settings
                                                    </Button>
                                                </Box>
                                                : null }
                                            </Box>
                                            <CardMedia
                                                component="img"
                                                sx={{ width: 151 }}
                                                image={device.type == "DHT" ? "../public/dht.png" :
                                                       device.type == "FOUR_SD" ? "../public/4sd.png" :
                                                       device.type == "LED" ? "../public/led.png" :
                                                       device.type == "RGB" ? "../public/rgb.png" :
                                                       device.type == "PIR" ? "../public/pir.png" :
                                                       device.type == "GYRO" ? "../public/gyro.png" :
                                                       device.type == "BUZZER" ? "../public/buzzer.png" :
                                                       device.type == "ALARM" ? "../public/alarm.png" :
                                                       device.type == "UDS" ? "../public/uds.png" :
                                                       device.type == "DMS" ? "../public/keypad.png" :
                                                       device.type == "DS" ? "../public/door.png" :
                                                       device.type == "LCD" ? "../public/lcd.png" :
                                                       device.type == "IR" ? "../public/ir.png" : ""
                                                }
                                                alt="Device image"
                                            />
                                        </Card>
                                    ))}
                                </ImageList>
                            </Grid>
                        </TabPanel>
                        <TabPanel value={value} index={1}>

                        </TabPanel>
                </Grid>
            </Grid>
        </>
    );
}