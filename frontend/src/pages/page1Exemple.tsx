import { useNavigate } from "react-router-dom";
import type { Graph } from "../types/graph.types";

export default function GraphPage() {
  const navigate = useNavigate();

  const graph: Graph = {
    directed: false,
    weighted: true,
    nodes: [
      { id: "A", label: "A", x: 120, y: 80 },
      { id: "B", label: "B", x: 290, y: 130 },
      { id: "C", label: "C", x: 110, y: 210 },
    ],
    edges: [
      { id: "e1", source: "A", target: "B", weight: 4 },
      { id: "e2", source: "A", target: "C", weight: 2 },
    ],
  };

  const goToPage2 = () => {
    navigate("/algorithm", {
      state: {
        graph,
      },
    });
  };

  return (
    <button onClick={goToPage2}>
      Continuer vers la page 2
    </button>
  );
}