import type { AlgorithmOption, AlgorithmKey } from "../types/algorithm.types";


type Props = {
  algorithms: AlgorithmOption[];
  selectedAlgorithm: AlgorithmKey;
  onSelect: (key: AlgorithmKey) => void;
};

export function AlgorithmSidebar({
  algorithms,
  selectedAlgorithm,
  onSelect,
}: Props) {
  const grouped = algorithms.reduce<Record<string, AlgorithmOption[]>>(
    (acc, algo) => {
      if (!acc[algo.category]) acc[algo.category] = [];
      acc[algo.category].push(algo);
      return acc;
    },
    {}
  );

  return (
    <aside className="sidebar">
      {Object.entries(grouped).map(([category, items], index) => (
        <div key={category}>
          {index > 0 && <div className="sb-divider" />}
          <div className="sb-section">{category}</div>

          {items.map((algo) => (
            <button
              key={algo.key}
              type="button"
              className={`sb-item ${selectedAlgorithm === algo.key ? "active" : ""}`}
              onClick={() => onSelect(algo.key)}
            >
              {algo.label}
            </button>
          ))}
        </div>
      ))}
    </aside>
  );
}