import { useParams } from "react-router-dom";
import { useEffect, useState, useRef } from "react";
import { ArrowUp, Copy, File, Image, Plus, Video } from "lucide-react";
import { createSocket } from "../Api/rooms";
import Popup from "../components/Popup";

export default function ChatRoom() {
    const { code } = useParams();

    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [menuOpen, setMenuOpen] = useState(false)

    const socketRef = useRef(null);
    const scrollRef = useRef(null);
    const messageTimesRef = useRef([]);
    const textareaRef = useRef(null);


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
        if (!input.trim() || !socketRef.current) return;

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
        if (textareaRef.current) {
            textareaRef.current.style.height = "40px"
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
    }

    const handelOnInput = (e) => {
        const el = e.target;
        el.style.height = "40px";

        if (el.value) {
            const newHeight = el.scrollHeight;
            const maxHeight = 120;
            if (newHeight > 40) {
                el.style.height = Math.min(newHeight, maxHeight) + "px";
            }
        }
    }
    return (

        <div className="h-screen flex flex-col items-center bg-blue-600/70">
            <div className="h-screen relative flex flex-col w-full md:w-xl">
                <div className="absolute  left-[35%] flex justify-center items-center py-2">
                    <div className=" rounded-xl text-center text-2xl px-7 py-2 border font-bold bg-white">
                        {code}
                    </div>

                </div>

                <div
                    ref={scrollRef}
                    className="flex-1 overflow-y-auto gap-1 p-4 flex flex-col items-end scrollbar-div-custom pb-15"
                >
                    {messages.map((m, i) => (
                        <>
                            <div key={i} className="  whitespace-pre-wrap max-w-full bg-white rounded-xl wrap-break-word px-5 py-1 inline-flex flex-col">
                                {m.content}
                                <button
                                    className="self-end text-end cursor-pointer text-gray-700  hover:text-gray-900 text-sm"
                                    onClick={() => navigator.clipboard.writeText(m.content)}
                                    title="Скопировать"
                                >
                                    <Copy width={15} />
                                </button>
                            </div>

                        </>


                    ))}
                </div>



                <div className=" absolute w-full bottom-0 p-4 flex ">
                    <div className="relative flex items-end bg-white rounded-l-xl pr-0.5">
                        <button onClick={() => setMenuOpen(!menuOpen)} type="button" className="bg-white rounded-3xl px-2 py-2 cursor-pointer hover:bg-black/20 transition duration-200">
                            <Plus />
                        </button>
                        <Popup menuOpen={menuOpen} />
                    </div>

                    <textarea
                        className="flex-1  bg-white p-2 focus:outline-none resize-none h-10 scrollbar-textarea-custom"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleOnKeyDown}
                        onInput={handelOnInput}
                        ref={textareaRef}
                    />
                    <div className="flex items-end bg-white rounded-r-xl pr-0.5">
                        <button className="bg-white rounded-3xl px-2 py-2 cursor-pointer hover:bg-black/20 transition duration-200" onClick={sendMessage}>
                            <ArrowUp />
                        </button>
                    </div>

                </div>
            </div>
        </div>
    );
}