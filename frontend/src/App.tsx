// // import React, { useState } from 'react';
// // import { FormuleGraphe } from './components/FormuleGraphe';
// // import { VisualisationGraphe } from './components/VisualisationGraphe';
// // import { PannelConfigGraphe } from './components/PannelConfigGraphe';
// // import type { Graph } from './types/graph.types';
// // import './styles/App.css';

// // function App() {
// //   const [graph, setGraph] = useState<Graph | null>(null);

// //   return (
// //     <div className="app-container">
// //       <header className="app-header">
// //         <div className="header-content">
// //           <h1 className="app-title">
// //             <span className="icon">◆</span>
// //             Graph Lab
// //           </h1>
// //           <div className="header-tabs">
// //             <button className="tab active">1. Graphe</button>
// //             <button className="tab">2. Algorithme & résultat</button>
// //           </div>
// //         </div>
// //       </header>

// //       <div className="app-layout">
// //         {/* LEFT PANEL - INPUTS */}
// //         <div className="left-panel">
// //           <FormuleGraphe onGrapheCreé={setGraph} />
// //         </div>

// //         {/* RIGHT PANEL - VISUALIZATION & ANALYSIS */}
// //         <div className="right-panel">
// //           {/* VISUALIZATION */}
// //           <VisualisationGraphe graph={graph} />

// //           {/* ANALYSIS SECTION */}
// //           <div className="analysis-container">
// //             <PannelConfigGraphe graph={graph} />
// //           </div>
// //         </div>
// //       </div>
// //     </div>
// //   );
// // }

// // export default App;
// import { BrowserRouter, Routes, Route } from "react-router-dom";

// import GraphPage from "./pages/page1Exemple";
// import AlgorithmPage from "./pages/AlgorithmPage";

// function App() {
//   return (
//     <BrowserRouter>
//       <Routes>

//         {/* Page 1 */}
//         <Route path="/" element={<GraphPage />} />

//         {/* Page 2 */}
//         <Route path="/algorithm" element={<AlgorithmPage />} />

//       </Routes>
//     </BrowserRouter>
//   );
// }

// export default App;



// // import { BrowserRouter, Routes, Route } from "react-router-dom";
// // import AlgorithmPage from "./pages/AlgorithmPage";

// // function App() {
// //   return (
// //     <BrowserRouter>
// //       <Routes>
// //         <Route path="*" element={<AlgorithmPage />} />
// //       </Routes>
// //     </BrowserRouter>
// //   );
// // }

// // export default App;


import { BrowserRouter, Routes, Route } from "react-router-dom";

import GraphPage from "./pages/GraphPage";
import AlgorithmPage from "./pages/AlgorithmPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<GraphPage />} />
        <Route path="/algorithm" element={<AlgorithmPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;