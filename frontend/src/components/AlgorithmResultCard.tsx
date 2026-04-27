import type { ExecutionResponse } from "../types/executionResponse.types";

type Props = {
  executionResult: ExecutionResponse | null;
  isLoading: boolean;
};

function renderArray(value: unknown) {
  if (!Array.isArray(value)) return "—";
  return value.join(" → ");
}

function renderComponents(value: unknown) {
  if (!Array.isArray(value)) return null;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
      {value.map((component, index) => (
        <div key={index} className="result-block">
          <div className="r-label">Composante {index + 1}</div>
          <div className="r-value">
            {Array.isArray(component) ? component.join(" , ") : String(component)}
          </div>
        </div>
      ))}
    </div>
  );
}

function renderNodeColors(value: unknown) {
  if (!value || typeof value !== "object") return null;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
      {Object.entries(value as Record<string, unknown>).map(([node, color]) => (
        <div key={node} className="result-block">
          <div className="r-label">Sommet {node}</div>
          <div className="r-value">{String(color)}</div>
        </div>
      ))}
    </div>
  );
}

export function AlgorithmResultCard({
  executionResult,
  isLoading,
}: Props) {
  if (isLoading) {
    return (
      <div className="card">
        <div className="card-title">Résultat textuel</div>
        <div className="result-block">
          <div className="r-label">État</div>
          <div className="r-value">Exécution en cours...</div>
        </div>
      </div>
    );
  }

  if (!executionResult) {
    return (
      <div className="card">
        <div className="card-title">Résultat textuel</div>

        <div className="result-block">
          <div className="r-label">État</div>
          <div className="r-value">Aucune exécution pour le moment</div>
        </div>

        <div className="result-block success">
          <div className="r-label">Résultat</div>
          <div className="r-value">
            Lance un algorithme pour afficher le résultat.
          </div>
        </div>
      </div>
    );
  }

  if (!executionResult.success) {
    return (
      <div className="card">
        <div className="card-title">Résultat textuel</div>

        <div className="result-block highlight">
          <div className="r-label">État</div>
          <div className="r-value">Échec d’exécution</div>
        </div>

        <div className="result-block">
          <div className="r-label">Message</div>
          <div className="r-value">{executionResult.message}</div>
        </div>
      </div>
    );
  }

  const { algorithm, message, result, meta } = executionResult;
  const summary = result.summary as Record<string, unknown>;
  const details = result.details as Record<string, unknown>;

  const isShortestPath =
    algorithm === "dijkstra" ||
    algorithm === "bellman-ford" ||
    algorithm === "bellman";

  const isMst = algorithm === "prim" || algorithm === "kruskal";
  const isComponents =
    algorithm === "connected-components" ||
    algorithm === "strongly-connected-components";
  const isEuler = algorithm === "euler";
  const isColoring = algorithm === "welsh-powell";

  return (
    <div className="card">
      <div className="card-title">Résultat textuel</div>

      <div className="result-block">
        <div className="r-label">Algorithme</div>
        <div className="r-value">{algorithm}</div>
      </div>

      <div className="result-block success">
        <div className="r-label">Message</div>
        <div className="r-value">{message}</div>
      </div>

      {isShortestPath && (
        <>
          <div className="result-block">
            <div className="r-label">Chemin</div>
            <div className="r-value">{renderArray(summary.path)}</div>
          </div>

          <div className="result-block highlight">
            <div className="r-label">Distance</div>
            <div className="r-value">{String(summary.distance ?? "—")}</div>
          </div>
        </>
      )}

      {isMst && (
        <>
          <div className="result-block highlight">
            <div className="r-label">Coût total</div>
            <div className="r-value">{String(summary.total_cost ?? "—")}</div>
          </div>

          <div className="result-block">
            <div className="r-label">Arêtes retenues</div>
            <div className="r-value">
              {Array.isArray(details.mst_edges)
                ? details.mst_edges.join(" , ")
                : "—"}
            </div>
          </div>
        </>
      )}

      {isComponents && (
        <>
          <div className="result-block highlight">
            <div className="r-label">Nombre de composantes</div>
            <div className="r-value">{String(summary.count ?? "—")}</div>
          </div>

          {renderComponents(details.components)}
        </>
      )}

      {isEuler && (
        <>
          <div className="result-block">
            <div className="r-label">Existe</div>
            <div className="r-value">{String(summary.exists ?? "—")}</div>
          </div>

          <div className="result-block">
            <div className="r-label">Type</div>
            <div className="r-value">{String(summary.type ?? "—")}</div>
          </div>

          <div className="result-block">
            <div className="r-label">Chemin</div>
            <div className="r-value">{renderArray(details.path)}</div>
          </div>
        </>
      )}

      {isColoring && (
        <>
          <div className="result-block highlight">
            <div className="r-label">Nombre de couleurs</div>
            <div className="r-value">{String(summary.color_count ?? "—")}</div>
          </div>

          {renderNodeColors(details.node_colors)}
        </>
      )}

      <div className="result-block">
        <div className="r-label">Temps d’exécution</div>
        <div className="r-value">{meta.execution_time_ms} ms</div>
      </div>

      <div className="result-block">
        <div className="r-label">Nombre d’étapes</div>
        <div className="r-value">{meta.step_count}</div>
      </div>
    </div>
  );
}