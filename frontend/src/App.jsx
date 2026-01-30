import { Routes, Route } from "react-router-dom";
import SignupPage from "./pages/signup";
import LoginPage from "./pages/Login";
import UploadReports from "./pages/UploadReports"; 

function App() {
  return (
    <Routes>
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/upload" element={<UploadReports />} />
    </Routes>
  );
}

export default App;
