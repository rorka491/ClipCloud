import { memo, useState } from "react";
import { Copy, Check } from "lucide-react";

const CopyButton = ({ text }) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(text);
        setCopied(true);

        setTimeout(() => {
            setCopied(false);
        }, 3000);
    };

    return (
        <button
            className="self-end text-gray-700 hover:text-gray-900 text-sm cursor-pointer"
            onClick={handleCopy}
        >
            {copied ? <Check width={15} /> : <Copy width={15} />}
        </button>
    );
}

export default memo(CopyButton);