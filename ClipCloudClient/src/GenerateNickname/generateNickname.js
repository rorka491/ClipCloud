export default function generateNickname() {
  const numbers = [];

  for (let number = 0; number < 12; number++) {
    const rand = Math.floor(Math.random() * 12);
    numbers.push(rand);
  }
  return `User-${numbers.join("")} `;
}
