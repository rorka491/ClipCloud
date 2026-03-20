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
        <div className="bg-blue-400/70 flex w-full h-screen justify-center items-center relative">

            <div className="fixed top-3 left-1/2 -translate-x-1/2 
                w-[90%] md:w-[80%] lg:w-[70%] 
                 h-30 
                bg-white rounded-2xl flex items-center justify-center shadow z-50">
                Реклама
            </div>

            <div className="fixed bottom-3 left-1/2 -translate-x-1/2 
                w-[90%] md:w-[80%] lg:w-[70%] 
                h-30 
                bg-white rounded-2xl flex items-center justify-center shadow z-50">
                Реклама
            </div>

            <div className="hidden lg:flex fixed top-5 bottom-5 left-3 
                w-40 xl:w-48 
                bg-white rounded-2xl items-center justify-center shadow z-50">
                Реклама
            </div>

            <div className="hidden lg:flex fixed top-5 bottom-5 right-3 
                w-40 xl:w-48 
                bg-white rounded-2xl items-center justify-center shadow z-50">
                Реклама
            </div>

            <div className="flex flex-col gap-2 w-full md:w-sm px-15 
                            md:ml-32 md:mr-32 md:mt-16 md:mb-16">

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