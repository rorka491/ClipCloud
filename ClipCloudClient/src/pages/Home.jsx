import { useNavigate } from "react-router-dom";
import { createRoom } from "../Api/rooms";
import NicknameInput from "../components/NicknameInput";
import { useState } from "react";
import generateNickname from "../GenerateNickname/generateNickname";

export default function Home() {
    const navigate = useNavigate();


    const [nickname, setNickname] = useState(() => generateNickname())


    const handleCreate = async () => {
        try {
            const data = await createRoom();
            localStorage.setItem('nickname', nickname)
            navigate(`/room/${data.code}`);
        } catch (err) {
            console.error("Ошибка создания комнаты:", err);
        }

    };

    return (
        <div className="bg-blue-400/70 flex w-full h-screen justify-center items-center relative">

            <div className="flex flex-col gap-2 w-full md:w-sm md:px-15 
                            ml-32 mr-32 mt-16 mb-16">
                <NicknameInput nickname={nickname} setNickname={setNickname} />
                <button
                    className="bg-white hover:text-white cursor-pointer hover:bg-black/25 transition duration-200 h-8 rounded-2xl w-full"
                    onClick={handleCreate}
                >
                    Начать
                </button>

                <button
                    className="bg-white hover:text-white cursor-pointer hover:bg-black/25 transition duration-200 h-8 rounded-2xl  px-8 md:px-0 w-full"
                    onClick={() => navigate("/join")}
                >
                    Присоединиться
                </button>

            </div>

        </div>
    );
}