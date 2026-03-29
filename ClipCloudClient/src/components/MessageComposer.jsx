import { memo, useRef, useState } from 'react'
import Popup from "./PopupFiles";
import { ArrowUp, Plus } from "lucide-react";


const MessageComposer = ({ blocked, socketRef }) => {

    const [input, setInput] = useState("");
    const [menuOpen, setMenuOpen] = useState(false);

    const textareaRef = useRef(null);


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
    )
}

export default memo(MessageComposer)