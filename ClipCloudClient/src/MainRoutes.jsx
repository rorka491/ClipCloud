import {  BrowserRouter, Route, Router, Routes } from "react-router-dom";
import Home from "./pages/Home";
import JoinRoom from "./pages/JoinRoom";
import ChatRoom from "./pages/ChatRoom";

export default function MainRoutes() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/join" element={<JoinRoom />} />
                <Route path="/room/:code" element={<ChatRoom />} />
            </Routes>
        </BrowserRouter>

    )
}
