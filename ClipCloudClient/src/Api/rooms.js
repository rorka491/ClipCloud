const API_BASE = import.meta.env.VITE_API_BASE || "/api";

export const createRoom = async () => {
  const res = await fetch(`${API_BASE}/rooms`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to create room");
  }

  return res.json();
};

export const checkRoom = async (code) => {
  const res = await fetch(`${API_BASE}/rooms/${encodeURIComponent(code)}`, {
    method: "GET",
  });

  if (!res.ok) {
    throw new Error("Room not found");
  }

  const data = await res.json();

<<<<<<< HEAD
  if (!data.is_exists) {
    alert("Комната не найдена");
    console.log(data.is_exists)
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
// };
=======
  return Boolean(data.is_exists);
};

export const getHistory = async (code) => {
  const res = await fetch(
    `${API_BASE}/rooms/${encodeURIComponent(code)}/history`,
    {
      method: "GET",
    }
  );

  if (!res.ok) {
    throw new Error("Failed to fetch room history");
  }

  return res.json();
};

export const sendTextMessage = async (code, { text, authorName = "User" }) => {
  const formData = new FormData();
  formData.append("type", "text");
  formData.append("text", text);
  formData.append("author_name", authorName);

  const res = await fetch(
    `${API_BASE}/rooms/${encodeURIComponent(code)}/messages`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!res.ok) {
    const error = new Error("Failed to send message");
    error.status = res.status;
    throw error;
  }

  return res.json();
};

export const createSocket = (code) => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const ws = new WebSocket(
    `${protocol}//${window.location.host}/api/notify/${encodeURIComponent(code)}`
  );
  ws.onopen = () => console.log('✅ Работает!');
  ws.onerror = (e) => console.log('❌ Не работает:', e);
  return ws
};
>>>>>>> c2fe769 (Вторая версия проекта)
