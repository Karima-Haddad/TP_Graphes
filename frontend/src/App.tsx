import { BrowserRouter, Routes, Route } from "react-router-dom";

import GraphPage from "./pages/page1Exemple";
import AlgorithmPage from "./pages/AlgorithmPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Page 1 */}
        <Route path="/" element={<GraphPage />} />

        {/* Page 2 */}
        <Route path="/algorithm" element={<AlgorithmPage />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;



// import { BrowserRouter, Routes, Route } from "react-router-dom";
// import AlgorithmPage from "./pages/AlgorithmPage";

// function App() {
//   return (
//     <BrowserRouter>
//       <Routes>
//         <Route path="*" element={<AlgorithmPage />} />
//       </Routes>
//     </BrowserRouter>
//   );
// }

// export default App;