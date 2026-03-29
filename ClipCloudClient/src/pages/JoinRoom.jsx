import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { checkRoom } from "../Api/rooms";
import NicknameInput from "../components/NicknameInput";
import generateNickname from "../GenerateNickname/generateNickname";

export default function JoinRoom() {
    const getRoomFromUrl = () => {
        const params = new URLSearchParams(window.location.search)
        return params.get("room") || ""
    }
    const [code, setCode] = useState(getRoomFromUrl());
    const [nickname, setNickname] = useState(() => generateNickname())

    const navigate = useNavigate();

    const joinRoom = async () => {
        if (!code.trim()) return;

        try {
            const findRoom = await checkRoom(code)
            localStorage.setItem('nickname', nickname)
            console.log(findRoom)
            if (findRoom) {
                navigate(`/room/${code}`);
            }

        } catch (err) {
            console.error("Ошибка подключения:", err);
        }
    };

    const handleOnKeyDown = (e) => {
        if (e.key === "Enter") {
            joinRoom();
        }
    };

    return (
        <div className="bg-blue-400/70 flex w-full h-screen justify-center items-center ">
            <div className="flex flex-col gap-2 w-full md:w-sm px-15">
                <NicknameInput nickname={nickname} setNickname={setNickname} />
                <input
                    className="bg-white w-full h-8 text-center rounded-xl outline-none"
                    placeholder="Код комнаты"
                    value={code}
                    onChange={(e) => setCode((e.target.value).toUpperCase())}
                    onKeyDown={handleOnKeyDown}
                />

                <button className="bg-white cursor-pointer hover:bg-black/25 hover:text-white transition duration-200 h-8 rounded-xl w-full" onClick={joinRoom}>
                    Присоединиться
                </button>
            </div>

        </div>
    );
}