import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Grid, TextField,
    Typography
} from "@mui/material";
import React from "react";
import {PopupMessage} from "../PopupMessage/PopupMessage.tsx";
import {Password} from "../models/Password.ts";
import {DeviceService} from "../services/DeviceService.ts";


interface AlarmProps {
    open: boolean,
    handleClose: () => void,
    reason : string,
    deviceService : DeviceService
}

export function AlarmDialog({open, handleClose, reason, deviceService}: AlarmProps) {

    const [password, setPassword] = React.useState<string>("");
    const [errorColor, setErrorColor] = React.useState<string>("transparent");
    const [errorMessage, setErrorMessage] = React.useState<string>("");
    const [errorPopupOpen, setErrorPopupOpen] = React.useState<boolean>(false);
    const [isSuccess, setIsSuccess] = React.useState(true);

    const handleErrorPopupClose = (reason?: string) => {
        if (reason === 'clickaway') return;
        setErrorPopupOpen(false);
    };

    const disableAlarm = () => {
        if(password == "") {
            setErrorColor("red");
            return;
        }
        setErrorColor("transparent");
        const passwordObj : Password = {
            password: password
        }
        deviceService.disableAlarm(passwordObj).then(() => {
            handleClose();
        }).catch(() => {
            setErrorMessage("Incorrect password!");
            setIsSuccess(false);
            setErrorPopupOpen(true);
        });
    }
    return (
        <>
            <Dialog
                PaperProps={{
                    style: {
                        border: '2px solid red'
                    },
                }}
                open={open}>
                <DialogTitle textAlign={'center'} sx={{background:"rgba(255,0,0,0.2)"}}>
                    <Typography variant={'h4'}><b>{"Alarm Activated! \\Ö/ \\Ö/ \\Ö/ \\Ö/"}</b></Typography>
                </DialogTitle>
                <DialogContent>
                    <Grid container pb={3} pt={3}>
                        <Grid item container xs={12} sm={12} md={12} lg={12} xl={12} justifyContent={'center'}>
                            <DialogContentText textAlign={'center'}>
                                <Typography variant={'h5'} color={'red'}>
                                    Alarm activated due to: <b>{reason}</b>
                                </Typography>
                            </DialogContentText>
                        </Grid>
                        <Grid item container xs={12} sm={12} md={12} lg={12} xl={12} pl={10} pr={10} mt={3} justifyContent={'center'}>
                            <TextField
                                id="password"
                                type={'password'}
                                fullWidth={true}
                                label="Input Alarm Password"
                                value={password}
                                onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                                    setPassword(event.target.value);
                                }}
                            />
                        </Grid>
                        <Grid item container xs={12} sm={12} md={12} lg={12} xl={12} pl={10} pr={10} mt={1} justifyContent={'center'}>
                            <Typography color={errorColor}>Please input the password!</Typography>
                        </Grid>
                    </Grid>
                </DialogContent>
                <DialogActions sx={{background:"rgba(255,0,0,0.2)"}}>
                    <Grid container>
                        <Grid item container xs={12} sm={12} md={12} lg={12} xl={12} justifyContent={'center'} pt={2} pb={2} alignItems={'center'}>
                            <Button variant='contained' color={'error'} onClick={disableAlarm}>Turn Off</Button>
                        </Grid>
                    </Grid>
                </DialogActions>
            </Dialog>
            <PopupMessage message={errorMessage} isSuccess={isSuccess} handleClose={handleErrorPopupClose}
                          open={errorPopupOpen}/>
        </>
    );
}