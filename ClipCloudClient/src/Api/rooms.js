export const createRoom = async () => {
  const res = await fetch("http://localhost:8000/rooms", {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to create room");
  }

  return res.json();
};


export const checkRoom = async (code) => {
    const res = await fetch(`http://localhost:8000/rooms/${code}`);

    if (res.ok) {
        throw new Error("Room not found");
    }

    return res.json();
};

export const createSocket = (code) => {
    return new WebSocket(`ws://localhost:8000/rooms/${code}`);
};