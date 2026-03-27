import { useNavigate } from "react-router-dom";
import { createRoom } from "../Api/rooms";
import { useState } from "react";

export default function Home() {
    const navigate = useNavigate();

    function generateNickname() {
        const numbers = []

        for (let number = 0; number < 12; number++) {
            const rand = Math.floor(Math.random() * 12)
            numbers.push(rand)
        }
        return `User-${numbers.join('')} `
    }


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
                <input placeholder={nickname} onChange={(e) => setNickname(e.target.value)} className="bg-white outline-none text-center h-8 rounded-2xl w-full" type="text" />

                <button
                    className="bg-white hover:text-white cursor-pointer hover:bg-black/25 transition duration-200 h-8 rounded-2xl w-full"
                    onClick={handleCreate}
                >
                    Начать
                </button>

                <button
<<<<<<< HEAD
                    className="bg-white hover:text-white cursor-pointer hover:bg-black/25 transition duration-200 h-8 rounded-2xl  px-8 md:px-0 w-full"
=======
                    className="bg-white hover:text-white cursor-pointer hover:bg-black/25 transition duration-200 h-8 rounded-2xl  px-5 md:px-0 w-full"
>>>>>>> main
                    onClick={() => navigate("/join")}
                >
                    Присоединиться
                </button>

            </div>

        </div>
    );
}