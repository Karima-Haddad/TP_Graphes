import type { ExecutionRequest } from "../types/execution.types";
import type { ExecutionResponse } from "../types/executionResponse.types";

const API_BASE_URL = "http://localhost:8000";

export async function executeAlgorithm(
  payload: ExecutionRequest
): Promise<ExecutionResponse> {
  const response = await fetch(`${API_BASE_URL}/execute`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = (await response.json()) as ExecutionResponse;

  if (!response.ok) {
    throw new Error(data.message || "Erreur lors de l’exécution");
  }

  return data;
}