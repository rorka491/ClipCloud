import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { checkRoom } from "../Api/rooms";

export default function JoinRoom() {
    const [code, setCode] = useState("");
    const navigate = useNavigate();

    const joinRoom = async () => {
        if (!code.trim()) return;

        try {
            const findRoom = await checkRoom(code)
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
                <input
                    className="bg-white w-full h-8 text-center rounded-xl outline-none"
                    placeholder="Код комнаты"
                    value={code}
                    onChange={(e) => setCode((e.target.value).toUpperCase())}
<<<<<<< HEAD
                    onKeyDown={handleOnKeyDown}
=======
>>>>>>> main
                />

                <button className="bg-white cursor-pointer hover:bg-black/25 hover:text-white transition duration-200 h-8 rounded-xl w-full" onClick={joinRoom}>
                    Присоединиться
                </button>
            </div>

        </div>
    );
}