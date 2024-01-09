import {DeviceService} from "../services/DeviceService.ts";
import {Box, Button, Card, CardContent, Grid, ImageList, Tab, Tabs, Typography} from "@mui/material";
import React from "react";

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
    const [devices, setDevices] = React.useState<number[]>([]);
    const [menuAnchorEl, setMenuAnchorEl] = React.useState<null | HTMLElement>(null);
    const openMenu = !!menuAnchorEl;
    const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
        setValue(newValue);
    };
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
                                height={'100%'}
                                xl={10}
                                lg={10}
                                md={10}
                                sm={12}
                                xs={12}
                                p={2}
                                style={{
                                    borderRadius: '1.5em',
                                    overflowY: 'auto',
                                    maxHeight: '100vh',
                                }}
                                alignItems={'flex-start'}
                                ml={{xl: '20%', lg: '20%', md: '25%', sm: '0', xs: '0'}}
                                mt={{xl: 0, lg: 0, md: 0, sm: '64px', xs: '64px'}}>
                                <ImageList  sx={{
                                    columnCount: {
                                        xs: '2 !important',
                                        sm: '4 !important',
                                        md: '4 !important',
                                        lg: '5 !important',
                                        xl: '5 !important',
                                    },
                                    width: "100%"}} cols={3} rowHeight={164}>
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
                                                    <Typography component="div" variant="h5" mb={1}>
                                                        {device.name}
                                                    </Typography>

                                                    <Typography variant="subtitle1" alignItems={'center'} color="text.secondary" component="div">
                                                        <span style={{display: 'inline-flex'}}> <HomeIcon/> {device.propertyName} </span>
                                                    </Typography>
                                                    <Typography variant="subtitle1" alignItems={'center'} color="text.secondary" component="div">
                                                        <span style={{display: 'inline-flex'}}> <BoltIcon/>  {device.powerSource} </span>
                                                    </Typography>
                                                    <Typography variant="subtitle1" alignItems={'center'} color="text.secondary" component="div">
                                                        <span style={{display: 'inline-flex'}}> <Battery3BarIcon/> {device.energyConsumption} kWh </span>
                                                    </Typography>
                                                </CardContent>
                                                <Box sx={{ display: 'flex', justifyContent:'center', width:'100%', alignItems: 'center', pl: 1, pb: 1 }}>
                                                    <Button  color={'secondary'} variant={'contained'} sx={{marginRight:'10px'}}>Share</Button>
                                                    <div>
                                                        <Button
                                                            id={"button_" + device.id}
                                                            aria-controls={openMenu ? 'menu_' + device.id : undefined}
                                                            aria-haspopup="true"
                                                            aria-expanded={openMenu ? 'true' : undefined}
                                                            variant="contained"
                                                            disableElevation
                                                            onClick={(evt) => handleMenuClick(evt,device.id)}
                                                            endIcon={<KeyboardArrowDownIcon />}>
                                                            More
                                                        </Button>

                                                    </div>
                                                </Box>
                                            </Box>
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