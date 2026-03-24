import { useParams } from "react-router-dom";
import { useEffect, useState, useRef } from "react";
import { ArrowUp, Plus } from "lucide-react";
import { createSocket } from "../Api/rooms";
import Popup from "../components/Popup";
import CopyButton from "../components/CopyButton";

export default function ChatRoom() {
    const { code } = useParams();

    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [menuOpen, setMenuOpen] = useState(false);
    const [blocked, setBlocked] = useState(false);

    const socketRef = useRef(null);
    const scrollRef = useRef(null);
    const textareaRef = useRef(null);

    useEffect(() => {
        const ws = createSocket(code);

        ws.onmessage = (event) => {
            console.log("SERVER:", event.data);

            const msg = JSON.parse(event.data);

            switch (msg.type) {
                case "history":
                    setMessages(msg.messages);
                    break;

                case "text":
                    setMessages((prev) => [...prev, msg]);
                    break;

                case "rate_limit":
                    setBlocked(true);
                    alert("Слишком много сообщений. Подожди немного.");

                    setTimeout(() => {
                        setBlocked(false);
                    }, 3000);

                    break;

                case "error":
                    if (msg.message?.toLowerCase().includes("too many")) {
                        setBlocked(true);
                        alert("Слишком много сообщений. Подожди немного.");

                        setTimeout(() => {
                            setBlocked(false);
                        }, 3000);

                        break;
                    }

                    alert(msg.message || "Ошибка сервера");
                    break;

                default:
                    console.log("Unknown message type:", msg);
            }
        };

        socketRef.current = ws;

        return () => ws.close();
    }, [code]);

    const sendMessage = () => {
        if (!input.trim() || !socketRef.current || blocked) return;

        socketRef.current.send(
            JSON.stringify({
                type: "text",
                content: input,
            })
        );

        setInput("");

        if (textareaRef.current) {
            textareaRef.current.style.height = "40px";
        }
    };

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleOnKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    const handleOnInput = (e) => {
        const el = e.target;
        el.style.height = "40px";

        if (el.value) {
            const newHeight = el.scrollHeight;
            const maxHeight = 120;

            if (newHeight > 40) {
                el.style.height = Math.min(newHeight, maxHeight) + "px";
            }
        }
    };


    return (
        <div className="h-dvh md:h-screen w-full flex flex-col items-center bg-blue-400/70">
            <div className="h-full relative flex flex-col w-full">

                <div className="flex justify-center">
                    <div className="absolute flex justify-center items-center py-2">
                        <div className="rounded-xl text-center text-2xl px-7 py-2 border font-bold bg-white">
                            {code}
                        </div>
                    </div>
                </div>

                <div
                    ref={scrollRef}
                    className="flex-1 overflow-y-auto p-4 flex flex-col items-end scrollbar-div-custom py-18"
                >
                    <div className="w-full md:w-2xl mx-auto flex flex-col gap-1 items-end">
                        {messages.map((m, i) => (
                            <div
                                key={i}
                                className="whitespace-pre-wrap wrap-break-word overflow-wrap-anywhere max-w-full bg-white rounded-xl px-5 py-1 inline-flex flex-col"
                            >
                                {m.content}

                                <CopyButton text={m.content} />
                            </div>
                        ))}
                    </div>
                </div>

                <div className="flex justify-center">
                    <div className="absolute w-full px-3 md:px-0 md:w-2xl bottom-0 py-4">
                        <div className="w-full border rounded-xl py-1 flex bg-white">

                            <div className="relative flex items-end bg-white rounded-l-xl pr-0.5">
                                <button
                                    onClick={() => setMenuOpen(!menuOpen)}
                                    type="button"
                                    className="bg-white rounded-3xl px-2 py-2 cursor-pointer hover:bg-black/20 transition duration-200"
                                >
                                    <Plus />
                                </button>

                                <Popup menuOpen={menuOpen} />
                            </div>

                            <textarea
                                className="flex-1 min-w-0 bg-white p-2  focus:outline-none resize-none h-10 scrollbar-textarea-custom"
                                value={input}
                                disabled={blocked}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={handleOnKeyDown}
                                onInput={handleOnInput}
                                ref={textareaRef}
                            />

                            <div className="flex items-end bg-white rounded-r-xl pr-0.5">
                                <button
                                    disabled={blocked}
                                    className={`bg-white rounded-3xl px-2 py-2 cursor-pointer transition duration-200 
                                    ${blocked ? "opacity-50 cursor-not-allowed" : "hover:bg-black/20"}`}
                                    onClick={sendMessage}
                                >
                                    <ArrowUp />
                                </button>
                            </div>

                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
}