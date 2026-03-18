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
  const res = await fetch(`http://localhost:8000/rooms/${code}`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Room not found");
  }

  const data = await res.json();

  if (!data.is_exists) {
    alert("Комната не найдена");
    console.log(data.is_exists)
    return data.is_exists;
  }

  return data.is_exists;
};

export const createSocket = (code) => {
  return new WebSocket(`ws://localhost:8000/rooms/${code}`);
};
