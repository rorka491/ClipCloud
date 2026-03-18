import { useNavigate } from "react-router-dom";
import { createRoom } from "../Api/rooms";

export default function Home() {
    const navigate = useNavigate();

    const handleCreate = async () => {
        try {
            const data = await createRoom();
            navigate(`/room/${data.code}`);
        } catch (err) {
            console.error("Ошибка создания комнаты:", err);
        }
    };

    return (
        <div className="bg-blue-600/70 flex w-full h-screen justify-center items-center relative">

            <div className="fixed rounded-2xl top-5 left-[15%] w-full md:w-[70%] h-30 bg-white flex items-center justify-center shadow z-50">
                Реклама
            </div>

            <div className="fixed rounded-2xl bottom-5 left-[15%] w-full md:w-[70%] h-30 bg-white flex items-center justify-center shadow z-50">
                Реклама
            </div>

            <div className="fixed rounded-2xl top-5 bottom-5 left-3 w-50 bg-white flex items-center justify-center shadow z-50">
                Реклама
            </div>

            <div className="fixed rounded-2xl top-5 bottom-5 right-3 w-50 bg-white flex items-center justify-center shadow z-50">
                Реклама
            </div>

            <div className="flex flex-col gap-2 w-full md:w-sm px-15 
                            ml-32 mr-32 mt-16 mb-16">

                <button
                    className="bg-white hover:text-white cursor-pointer hover:bg-black/25 transition duration-200 h-8 rounded-2xl w-full"
                    onClick={handleCreate}
                >
                    Начать
                </button>

                <button
                    className="bg-white hover:text-white cursor-pointer hover:bg-black/25 transition duration-200 h-8 rounded-2xl w-full"
                    onClick={() => navigate("/join")}
                >
                    Присоединиться
                </button>

            </div>

        </div>
    );
}