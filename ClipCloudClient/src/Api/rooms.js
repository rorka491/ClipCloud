// Убираем baseAddress, используем window.location

export const createRoom = async () => {
  const res = await fetch(`/api/rooms`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to create room");
  }

  return res.json();
};

export const checkRoom = async (code) => {
  const res = await fetch(`/api/rooms/${code}`, {
    method: "GET",
  });

  if (!res.ok) {
    throw new Error("Room not found");
  }

  const data = await res.json();

  if (!data.is_exists) {
    alert("Комната не найдена");
    console.log(data.is_exists);
    return data.is_exists;
  }

  return data.is_exists;
};

export const createSocket = (code) => {

  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const ws = new WebSocket(`${protocol}//${window.location.host}/api/ws/${code}`);
  ws.onopen = () => console.log('✅ Работает!');
  ws.onerror = (e) => console.log('❌ Не работает:', e);
  return ws
};

// export const createSocket = (code) => {
//   const ws = new WebSocket(`ws://127.0.0.1:8000/api/ws/${code}`);

//   ws.onopen = () => console.log("✅ WebSocket connected");
//   ws.onerror = (e) => console.log("❌ WebSocket error:", e);
//   ws.onclose = () => console.log("🔴 WebSocket closed");

//   return ws;
<<<<<<< HEAD
// };
=======
// };
>>>>>>> main
