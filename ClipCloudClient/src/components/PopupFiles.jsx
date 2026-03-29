// import { useRef } from "react";
import { Image, File } from "lucide-react";

export default function Popup({ menuOpen }) {

    // const imageInputRef = useRef(null);
    // const fileInputRef = useRef(null);

    // const handleFileSelect = (type, files) => {
    //     const file = files[0];
    //     if (!file) return;

    //     console.log(`${type} выбран:`, file);
    // };

    return (

        menuOpen && (
            <div className="absolute bottom-full left-0 mb-2 w-36 bg-white shadow-lg rounded-2xl flex flex-col gap-2 p-2 z-40">
                <input
                    type="file"
                    accept="image/*"
                    style={{ display: "none" }}
                    // ref={imageInputRef}
                    // onChange={(e) => handleFileSelect("Image", e.target.files)}
                />
                <input
                    type="file"
                    style={{ display: "none" }}
                    // ref={fileInputRef}
                    // onChange={(e) => handleFileSelect("File", e.target.files)}
                />

                <button
                    className="flex gap-2 items-center hover:bg-black/10 rounded-lg px-2 py-1 cursor-pointer"
                    // onClick={() => imageInputRef.current.click()}
                >
                    <Image /> Image
                </button>

                

                <button
                    className="flex gap-2 items-center hover:bg-black/10 rounded-lg px-2 py-1 cursor-pointer"
                    // onClick={() => fileInputRef.current.click()}
                >
                    <File /> File
                </button>
            </div>
        )
    );
}