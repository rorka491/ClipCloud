import { useParams } from "react-router-dom";
import { useEffect, useState, useRef } from "react";
import { createSocket } from "../Api/rooms";
import CopyButton from "../components/CopyButton";
import MessageComposer from "../components/MessageComposer";
import RoomCode from "../components/RoomCode";

export default function ChatRoom() {
    const { code } = useParams();

    const [messages, setMessages] = useState([]);
    const [blocked, setBlocked] = useState(false);
    const [hasScroll, setHasScroll] = useState(false);

    const socketRef = useRef(null);
    const scrollRef = useRef(null);

    useEffect(() => {
        const ws = createSocket(code);

        ws.onmessage = (event) => {
            console.log("SERVER:", event.data);

            const msg = JSON.parse(event.data);
            console.log(msg)

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


    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);


    useEffect(() => {
        const el = scrollRef.current;
        if (!el) return;

        const checkScroll = () => {
            setHasScroll(el.scrollHeight > el.clientHeight);
        };

        checkScroll();

        const observer = new ResizeObserver(checkScroll);
        observer.observe(el);

        return () => observer.disconnect();
    }, [messages]);

    const formatTime = (iso) =>
        new Date(iso).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
        });

    const nickname = localStorage.getItem("nickname")


    return (
        <div className="h-dvh md:h-screen w-full flex flex-col items-center bg-blue-400/70">
            <div className="h-full relative flex flex-col w-full">

                <div className="flex justify-center">
                    <RoomCode code={code} />
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
                                <div className="flex justify-end text-sm text-blue-600/80">
                                    {nickname}
                                </div>
                                <div className="text-end whitespace-pre-wrap wrap-break-word overflow-wrap-anywhere max-w-full inline-flex flex-col">
                                    {m.content}

                                </div>
                                <div className="flex justify-between gap-2">
                                    <span className="text-sm">{formatTime(m.created_at)}</span>
                                    <CopyButton text={m.content} />
                                </div>

                            </div>
                        ))}
                    </div>
                </div>

                <div className={`flex justify-center  ${hasScroll ? "md:mr-2.5" : ""}`}>
                    <MessageComposer blocked={blocked} socketRef={socketRef} />
                </div>

            </div>
        </div>
    );
}