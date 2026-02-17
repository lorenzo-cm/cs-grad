const API_URL = "http://localhost:8000/api/v1/wordle";

export async function createGame() {
  const res = await fetch(`${API_URL}/games`, { method: "POST" });
  const data = await res.json();
  return data.game_id;
}

export async function makeGuess(game_id: string, word: string) {
  const res = await fetch(`${API_URL}/games/${game_id}/guess`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ word }),
  });
  if (!res.ok) throw new Error((await res.json()).detail || "Erro ao enviar palpite");
  return await res.json();
}

export async function getGameState(game_id: string) {
  const res = await fetch(`${API_URL}/games/${game_id}`);
  if (!res.ok) throw new Error("Jogo não encontrado");
  return await res.json();
}
