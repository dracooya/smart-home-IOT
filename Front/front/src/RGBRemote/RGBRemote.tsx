import {
    Dialog,
    DialogContent,
    DialogTitle,
    Grid,
    IconButton, ToggleButton, ToggleButtonGroup,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import React from "react";
import {Socket} from "socket.io-client";

interface RGBRemoteProps {
    open: boolean,
    handleClose: () => void,
    socket: Socket
}

export function RGBRemote({open, handleClose, socket} : RGBRemoteProps) {
    const [mode, setMode] = React.useState<string | null>("");
    const close = () => { handleClose(); }

    const handleMode = (
        _event: React.MouseEvent<HTMLElement>,
        newMode: string | null,
    ) => {
        setMode(newMode);
        let modeToSend = newMode;
        if(newMode?.includes("OK"))
            modeToSend = "OK"
        socket.emit('rgb_remote', modeToSend);
    };



    return (
        <>
            <React.Fragment>
                <Dialog
                    open={open}
                    maxWidth={'xs'}
                    onClose={handleClose}>
                    <DialogTitle textAlign={'center'}>RGB Settings</DialogTitle>
                    <DialogContent>
                            <Grid container alignItems={'center'} alignContent={'center'}>
                                <Grid item xl={11} lg={11} alignSelf={'center'}>
                                    <ToggleButtonGroup
                                        exclusive
                                        color="primary"
                                        value={mode}
                                        sx={{ flexWrap: "wrap", marginLeft:'80px'}}
                                        onChange={handleMode}
                                        aria-label="options">
                                        <ToggleButton value="OK_ON" sx={{margin:'5px 10px 5px 60px'}}  selected={mode == "OK_ON"} color={'success'}>ON</ToggleButton>
                                        <ToggleButton value="OK_OFF" sx={{margin:'5px 100px'}}  selected={mode == "OK_OFF"} color={'error'}>OFF</ToggleButton>
                                        <ToggleButton value="0"  sx={{margin:'5px 10px'}} selected={mode == "0"}>WHITE</ToggleButton>
                                        <ToggleButton value="1"  sx={{margin:'5px 10px'}} selected={mode == "1"}>RED</ToggleButton>

                                        <ToggleButton value="2"  sx={{margin:'5px 10px'}} selected={mode == "2"}>GREEN</ToggleButton>
                                        <ToggleButton value="3"  sx={{margin:'5px 10px'}} selected={mode == "3"}>BLUE</ToggleButton>
                                        <ToggleButton value="4"  sx={{margin:'5px 10px'}}  selected={mode == "4"}>YELLOW</ToggleButton>

                                        <ToggleButton value="5"  sx={{margin:'5px 10px'}} selected={mode == "5"}>PURPLE</ToggleButton>
                                        <ToggleButton value="6"  sx={{margin:'5px 10px'}} selected={mode == "6"}>CYAN</ToggleButton>
                                        <ToggleButton value="*"  sx={{margin:'5px 10px'}} selected={mode == "*"}>LUDILO</ToggleButton>
                                    </ToggleButtonGroup>
                                </Grid>
                            </Grid>

                        <IconButton aria-label="close" sx={{position:'absolute',top:'2px',right:'3px'}} onClick={close}>
                            <CloseIcon />
                        </IconButton>
                    </DialogContent>
                </Dialog>
            </React.Fragment>
        </>
    );
}