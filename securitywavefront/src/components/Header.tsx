import React from "react";
import { useNavigate } from "react-router-dom";
import logo from "../Landinglogo.png"; // 로고 이미지 경로 수정

const Header: React.FC = () => {
  const navigate = useNavigate();

  const handleLogoClick = () => {
    navigate("/"); // "/" 경로로 이동
  };

  const handleDevelopersClick = () => {
    console.log("For Developers clicked!");
    navigate("/upload"); // "/upload" 경로로 이동
  };

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        backgroundColor: "var(--background-color)", // CSS 변수 사용
        color: "var(--text-color)", // 텍스트 색상
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "20px 30px", // 세로 길이 조정 (1.5배로 증가)
        boxShadow: "0 4px 10px rgba(0, 0, 0, 0.5)",
        zIndex: 1000,
        boxSizing: "border-box", // 패딩 포함 박스 크기 계산
      }}
    >
      {/* 로고와 SECURITY WAVE */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "20px",
          cursor: "pointer",
        }}
        onClick={handleLogoClick}
      >
        <img src={logo} alt="Logo" style={{ height: "50px" }} />
        <span style={{ fontSize: "20px", fontWeight: "bold" }}>
          SECURITY WAVE
        </span>

        {/* 네비게이션 링크 - SECURITY WAVE 옆에 위치 */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "50px",
            marginLeft: "50px",
          }}
        >
          <a
            href="#company"
            style={{
              color: "var(--text-color)",
              textDecoration: "none",
              fontSize: "18px",
              fontWeight: "bold", // 굵게 표시
              cursor: "pointer",
            }}
          >
            Company
          </a>
          <span
            onClick={handleDevelopersClick} // 클릭 이벤트로 handleDevelopersClick 호출
            style={{
              color: "var(--text-color)",
              textDecoration: "none",
              fontSize: "18px",
              fontWeight: "bold", // 굵게 표시
              cursor: "pointer",
            }}
          >
            For Developers
          </span>
          <a
            href="#chains"
            style={{
              color: "var(--text-color)",
              textDecoration: "none",
              fontSize: "18px",
              fontWeight: "bold", // 굵게 표시
              cursor: "pointer",
            }}
          >
            For Chains
          </a>
          <a
            href="#enterprise"
            style={{
              color: "var(--text-color)",
              textDecoration: "none",
              fontSize: "18px",
              fontWeight: "bold", // 굵게 표시
              cursor: "pointer",
            }}
          >
            Enterprise
          </a>
          <a
            href="#docs"
            style={{
              color: "var(--text-color)",
              textDecoration: "none",
              fontSize: "18px",
              fontWeight: "bold", // 굵게 표시
              cursor: "pointer",
            }}
          >
            Docs
          </a>
        </div>
      </div>

      {/* Sign In & Log In 버튼 */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "10px", // 버튼 간격 조정
          flexShrink: 0, // 버튼 크기 줄어들지 않도록 설정
        }}
      >
        <button
          style={{
            fontSize: "14px",
            padding: "8px 16px", // 버튼 크기 조정
            backgroundColor: "transparent",
            border: "2px solid var(--text-color)",
            borderRadius: "5px",
            color: "var(--text-color)",
            cursor: "pointer",
          }}
        >
          Sign In
        </button>
        <button
          style={{
            fontSize: "14px",
            padding: "8px 16px", // 버튼 크기 조정
            backgroundColor: "transparent",
            border: "2px solid var(--text-color)",
            borderRadius: "5px",
            color: "var(--text-color)",
            cursor: "pointer",
          }}
        >
          Log In
        </button>
      </div>
    </div>
  );
};

export default Header;
