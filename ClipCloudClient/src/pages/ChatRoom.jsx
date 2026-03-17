import { useParams } from "react-router-dom";
import { useEffect, useState, useRef } from "react";
import { ArrowUp } from "lucide-react";
import { createSocket } from "../Api/rooms";

export default function ChatRoom() {
    const { code } = useParams();

    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    const socketRef = useRef(null);
    const scrollRef = useRef(null);
    const messageTimesRef = useRef([]);

    useEffect(() => {
        const ws = createSocket(code);

        ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);

            if (msg.type === "history") {
                setMessages(msg.messages);
            } else {
                setMessages((prev) => [...prev, msg]);
            }
        };

        socketRef.current = ws;

        return () => ws.close();
    }, [code]);

    const sendMessage = () => {
        if (!input || !socketRef.current) return;

        const now = Date.now();

        const times = messageTimesRef.current.filter(
            (t) => now - t < 5000
        );

        if (times.length >= 3) {
            alert("Too many messages. Wait.");
            return;
        }

        times.push(now);
        messageTimesRef.current = times;

        socketRef.current.send(
            JSON.stringify({
                type: "text",
                content: input,
            })
        );

        setInput("");
    };

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    return (

        <div className="h-screen flex flex-col items-center bg-blue-600/70">
            <div className="h-screen flex flex-col w-full md:w-xl">
                <div className="flex justify-center items-center py-2">
                    <div className="text-center text-2xl px-7 py-2 border font-bold bg-white">
                        {code}
                    </div>

                </div>

                <div
                    ref={scrollRef}
                    className="flex-1 overflow-y-auto p-4 flex flex-col items-end scrollbar-custom"
                >
                    {messages.map((m, i) => (
                        <div key={i} className="mb-3 max-w-[70%] bg-white rounded wrap-break-word px-5 py-1 inline-block">
                            {m.content}
                        </div>
                    ))}
                </div>

                <div className="p-4 flex ">
                    <input
                        className="flex-1 bg-white p-2 focus:outline-none"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === "Enter") sendMessage();
                        }}
                    />

                    <button className="bg-white px-3 cursor-pointer" onClick={sendMessage}>
                        <ArrowUp />
                    </button>
                </div>
            </div>
        </div>
    );
}