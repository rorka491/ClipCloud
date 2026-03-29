export default function NicknameInput({ nickname, setNickname }) {
    return (
        <input placeholder={nickname} onChange={(e) => setNickname(e.target.value)} className="bg-white outline-none text-center h-8 rounded-2xl w-full" type="text" />
    )
}
