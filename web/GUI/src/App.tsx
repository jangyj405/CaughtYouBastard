import React from 'react';
import {BrowserRouter as Router, Routes, Route, Outlet} from "react-router-dom"
import UploadImg from "./pages/uploadImg"
import MngCarNum from './pages/mngCarNum'
import CarNumberlog from './pages/carNumberlog'
import {SideBar}  from "./components/sideBar"


import Main from "./pages/main"
import './App.css';

const Layout = () =>{
  return (
    <div>
      <main>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"></link>
        <SideBar />
        <Outlet />
      </main>
    </div>
  )
}

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          
          <Route element={<Layout/>}>
              <Route index element={<Main/>} />
              <Route path="upload" element={<UploadImg/>} />
              <Route path="mng-car-num" element={<MngCarNum/>} />
              <Route path="logs" element={<CarNumberlog/>} />

          </Route>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
