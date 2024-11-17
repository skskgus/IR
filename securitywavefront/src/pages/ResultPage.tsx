import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Result from "../components/Result";
import logo from "../Landinglogo.png"; // 이미지 파일의 위치에 맞게 경로 수정

const ResultPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const result = location.state?.result;

  return (
    <div
      style={{
        position: "relative",
        height: "100vh",
        backgroundColor: "#1a1a1a",
        color: "#ffffff",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* 왼쪽 상단 로고 */}
      <img
        src={logo}
        alt="Security Wave Logo"
        onClick={() => navigate("/")}
        style={{
          position: "absolute",
          top: "20px",
          left: "20px",
          width: "10%",
          maxWidth: "90px",
          height: "auto",
          cursor: "pointer",
        }}
      />

      {/* 중앙 결과 표시 영역 */}
      <div
        style={{
          width: "70%",
          maxWidth: "1000px",
          backgroundColor: "#2a2a2a",
          padding: "30px",
          borderRadius: "10px",
          textAlign: "center",
          boxShadow: "0 4px 10px rgba(0, 0, 0, 0.5)",
        }}
      >
        <h1 style={{ fontSize: "36px", marginBottom: "20px" }}>Analysis Result</h1>
        {result ? (
          <Result result={result} />
        ) : (
          <p style={{ fontSize: "18px" }}>No result available.</p>
        )}
      </div>
    </div>
  );
};

export default ResultPage;
