import { useState } from 'react'
import './App.css'
import {BrowserRouter, Route, Routes} from "react-router-dom";
import {DeviceStatuses} from "./deviceStatuses/DeviceStatuses.tsx";
import {DeviceService} from "./services/DeviceService.ts";

function App() {
  const deviceServiceSingleton = new DeviceService()

  return (
      <>
          <BrowserRouter>
              <Routes>
                  <Route path="/" element={<DeviceStatuses deviceService={deviceServiceSingleton}/>}/>
              </Routes>
          </BrowserRouter>
      </>
  )
}

export default App
