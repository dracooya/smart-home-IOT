import React from "react";
import {
    Button,
    Dialog,
    DialogContent,
    DialogTitle,
    Grid,
    IconButton,
    Typography
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import {Socket} from "socket.io-client";
import {LocalizationProvider, MobileTimePicker} from "@mui/x-date-pickers";
import {AdapterDayjs} from "@mui/x-date-pickers/AdapterDayjs";
import {Dayjs} from "dayjs";
import {PopupMessage} from "../PopupMessage/PopupMessage.tsx";

interface AlarmClockRemoteProps {
    open: boolean,
    handleClose: () => void,
    socket: Socket
}

export function AlarmClockRemote({open, handleClose, socket} : AlarmClockRemoteProps) {
    const [time, setTime] = React.useState<Dayjs | null>(null);
    const [errorMessage, setErrorMessage] = React.useState<string>("");
    const [errorPopupOpen, setErrorPopupOpen] = React.useState<boolean>(false);
    const [isSuccess, setIsSuccess] = React.useState(true);
    const close = () => { handleClose(); }

    const handleErrorPopupClose = (reason?: string) => {
        if (reason === 'clickaway') return;
        setErrorPopupOpen(false);
    };

    const setAlarmClock = () => {
        if(time == null) {
            setErrorMessage("Specify the alarm clock time!");
            setIsSuccess(false);
            setErrorPopupOpen(true);
            return;
        }
        let timeLocal : number = time!.valueOf();
        const now = new Date().getTime();
        if(timeLocal < now) {
            timeLocal += 1000 * 60 * 60 * 24;
        }
        const timeOffset = timeLocal - now;
        const hours = Math.floor((timeOffset % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeOffset % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeOffset % (1000 * 60)) / 1000);
        socket.emit('alarm_clock_time', timeLocal.toString());

        setErrorMessage("Alarm will go off in " + hours + " hours, " + minutes + " minutes and " + seconds + " seconds.");
        setIsSuccess(true);
        setErrorPopupOpen(true);
        handleClose();
    }
    return (
        <>
            <React.Fragment>
                <Dialog
                    open={open}
                    fullWidth={true}
                    onClose={handleClose}>
                    <DialogTitle textAlign={'center'}>Alarm Clock Settings</DialogTitle>
                    <DialogContent>
                        <Grid container alignItems={'center'} alignContent={'center'}>
                            <Grid container item xl={12} lg={12} alignItems={'center'} mt={2}>
                                <Grid item xs={12} sm={12} md={12} lg={5} xl={4} alignItems={'center'}>
                                    <Typography variant={"body1"} display={'inline'}>Set Alarm Time: </Typography>
                                </Grid>
                                <Grid item xs={12} sm={12} md={12} lg={7} xl={8}>
                                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                                        <MobileTimePicker  label={'Set Alarm Time'}
                                                           value={time}
                                                           sx={{width:'100%'}}
                                                           onChange={(newValue) => setTime(newValue)}/>
                                    </LocalizationProvider>
                                </Grid>
                                <Grid container item xs={12} sm={12} md={12} lg={12} xl={12} mb={1} mt={2}  justifyContent={'center'} alignItems={'center'}>
                                    <Button variant={'contained'}
                                            onClick={setAlarmClock}
                                            sx={{marginRight:5}}
                                            color={'primary'}>Set Alarm Clock</Button>
                                </Grid>
                            </Grid>
                        </Grid>

                        <IconButton aria-label="close" sx={{position:'absolute',top:'2px',right:'3px'}} onClick={close}>
                            <CloseIcon />
                        </IconButton>
                    </DialogContent>
                </Dialog>
            </React.Fragment>
            <PopupMessage message={errorMessage} isSuccess={isSuccess} handleClose={handleErrorPopupClose}
                          open={errorPopupOpen}/>
        </>
    );
}