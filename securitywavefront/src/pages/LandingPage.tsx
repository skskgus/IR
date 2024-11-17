// src/pages/LandingPage.tsx
import React from "react";
import { useNavigate } from "react-router-dom";
import logo from "../Landinglogo.png"; // 이미지 파일의 위치에 맞게 경로 수정

const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate("/upload");
  };

  return (
    <div
      style={{
        position: "relative",
        height: "100vh",
        color: "var(--text-color)", // 텍스트 색상: CSS 변수 사용
      }}
    >
      {/* 상단 오른쪽에 Sign In, Log In 버튼 */}
      <div
        style={{
          position: "absolute",
          top: "20px",
          right: "20px",
          display: "flex",
          gap: "10px",
        }}
      >
        <button
          style={{
            fontSize: "18px",
            padding: "8px 16px",
            backgroundColor: "#3a3a3a",
            border: "1px solid var(--text-color)", // 테두리 색상
            borderRadius: "5px",
            color: "var(--text-color)", // 버튼 텍스트 색상
            cursor: "pointer",
          }}
        >
          Sign In
        </button>
        <button
          style={{
            fontSize: "18px",
            padding: "8px 16px",
            backgroundColor: "#3a3a3a",
            border: "1px solid var(--text-color)", // 테두리 색상
            borderRadius: "5px",
            color: "var(--text-color)", // 버튼 텍스트 색상
            cursor: "pointer",
          }}
        >
          Log In
        </button>
      </div>

      {/* 가운데 로고와 텍스트 */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          height: "100%",
          color: "var(--text-color)", // 텍스트 색상: CSS 변수 사용
        }}
      >
        <img
          src={logo}
          alt="Security Wave Logo"
          style={{
            width: "60%",
            maxWidth: "900px",
            height: "auto",
            marginBottom: "0",
          }}
        />
        <div
          style={{
            width: "70%",
            maxWidth: "1000px",
            height: "2px",
            backgroundColor: "var(--text-color)", // 선 색상
            margin: "0 0 30px 0",
          }}
        ></div>
        <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
          <button
            onClick={handleButtonClick}
            style={{
              fontSize: "36px",
              padding: "10px 20px",
              backgroundColor: "#3a3a3a",
              border: "2px solid var(--text-color)", // 테두리 색상
              borderRadius: "5px",
              color: "var(--text-color)", // 버튼 텍스트 색상
              cursor: "pointer",
            }}
          >
            Detecting
          </button>
          <button
            onClick={handleButtonClick}
            style={{
              fontSize: "36px",
              padding: "10px 20px",
              backgroundColor: "#3a3a3a",
              border: "2px solid var(--text-color)", // 테두리 색상
              borderRadius: "5px",
              color: "var(--text-color)", // 버튼 텍스트 색상
              cursor: "pointer",
            }}
          >
            Mining
          </button>
          <button
            onClick={handleButtonClick}
            style={{
              fontSize: "36px",
              padding: "10px 20px",
              backgroundColor: "#3a3a3a",
              border: "2px solid var(--text-color)", // 테두리 색상
              borderRadius: "5px",
              color: "var(--text-color)", // 버튼 텍스트 색상
              cursor: "pointer",
            }}
          >
            Dao
          </button>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
