import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import UploadPage from "./pages/UploadPage";
import ResultPage from "./pages/ResultPage";
import Header from "./components/Header";
import ThemeToggleButton from "./components/ThemeToggleButton"; // 테마 버튼 임포트
import ResultPage from "./pages/ResultPage";
import Register from "./pages/Register"; //추가
import Login from "./pages/Login"; //추가

const App: React.FC = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/result" element={<ResultPage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
      </Routes>
      {/* 테마 토글 버튼 */}
      <ThemeToggleButton />
    </Router>
  );
};

export default App;
