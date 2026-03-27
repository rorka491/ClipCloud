import { Eye, EyeClosed, QrCode } from "lucide-react"
import { memo, useState } from "react"
import { QRCodeSVG } from "qrcode.react";

const RoomCode = ({ code }) => {
    const [isVisible, setIsVisible] = useState(false)
    const [showQR, setShowQR] = useState(false)

    const hiddenCode = "*".repeat(code.length)
    const roomUrl = `${window.location.origin}/room/${code}`
    return (
        <div className="absolute flex justify-center items-center py-2">
            <div className="flex w-37.5 h-12.5 items-center justify-center gap-1 rounded-xl pl-2 pr-2 py-2 border font-bold bg-white">
                <button
                    onClick={() => setShowQR(true)}
                    className="cursor-pointer py-1"
                >
                    <QrCode className="w-4" />
                </button>
                <div className="w-21 text-center text-xl">
                    {isVisible ? code : hiddenCode}
                </div>
                <button className="cursor-pointer py-1 " onClick={() => setIsVisible(!isVisible)}>
                    {isVisible ? <Eye className="w-4" /> : <EyeClosed className="w-4" />}
                </button>
            </div>
            {showQR && (
                <div className="fixed inset-0 bg-black/40 flex items-center justify-center">
                    <div className="bg-white p-5 rounded-xl flex flex-col items-center gap-3">
                        <QRCodeSVG value={roomUrl} size={200} />

                        <button
                            onClick={() => setShowQR(false)}
                            className="cursor-pointer text-sm px-3 py-1 border rounded-lg"
                        >
                            Закрыть
                        </button>
                    </div>
                </div>
            )}
        </div>
    )
}

export default memo(RoomCode)