import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Grid,
    Typography
} from "@mui/material";
import {Socket} from "socket.io-client";
import {useEffect, useRef} from "react";

interface AlarmDialogProps {
    open: boolean,
    handleClose: () => void,
    lastAlarmClockTime : string,
    socket: Socket
}

export function AlarmClockDialog({open, handleClose, lastAlarmClockTime, socket}: AlarmDialogProps) {

    const audioRef = useRef<HTMLAudioElement | null>(null);
    const disableAlarm = () => {
        socket.emit('alarm_clock_off', "off");
        handleClose();
    }

    useEffect(() => {
        if (audioRef.current) {
            if (!open) {
                audioRef.current.pause();
            } else {
                audioRef.current.play();
            }
        }
    }, [open]);


    return (
        <>
            <Dialog
                open={open}>
                <DialogTitle textAlign={'center'}>
                    {"Alarm Clock Activated!"}
                </DialogTitle>
                <DialogContent>
                    <DialogContentText textAlign={'center'}>
                        <Typography variant={'h2'} color={'black'} mb={2}><b>{lastAlarmClockTime}</b></Typography>
                        WAKEY WAKEY TIME FOR SCHOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO :))))))))))))))))))))))))))))))))))

                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Grid container>
                        <Grid item container xs={12} sm={12} md={12} lg={12} xl={12} justifyContent={'center'} mb={2}>
                            <Button variant='contained' onClick={disableAlarm}>Turn Off</Button>
                        </Grid>
                    </Grid>
                </DialogActions>
            </Dialog>
            <audio ref={audioRef} src={"../alarm_clock_sound.mp3"} loop={true} />
        </>
    );
}