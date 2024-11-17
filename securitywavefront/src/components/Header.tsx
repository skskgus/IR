import React from "react";
import logo from "../Landinglogo.png"; // 로고 이미지 경로 수정

const Header: React.FC = () => {
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
        justifyContent: "space-between", // 요소 간 균등 분배
        padding: "20px 30px", // 오른쪽 패딩을 줄임
        boxShadow: "0 4px 10px rgba(0, 0, 0, 0.5)",
        zIndex: 1000,
        transition: "background-color 0.3s, color 0.3s", // 부드러운 전환 효과
        boxSizing: "border-box", // 박스 모델 계산 문제 방지
      }}
    >
      {/* Detecting과 로고 */}
      <div style={{ display: "flex", alignItems: "center", gap: "20px" }}>
        <img
          src={logo}
          alt="Logo"
          style={{ height: "50px", cursor: "pointer" }}
        />
        <span style={{ fontSize: "20px", fontWeight: "bold" }}>
          SECURITY WAVE
        </span>
      </div>

      {/* 네비게이션 링크 */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "80px", // 간격 두 배로 증가
        }}
      >
        <a
          href="#detecting"
          style={{
            color: "var(--text-color)",
            textDecoration: "none",
            fontSize: "18px",
            cursor: "pointer",
          }}
        >
          Detecting
        </a>
        <a
          href="#developers"
          style={{
            color: "var(--text-color)",
            textDecoration: "none",
            fontSize: "18px",
            cursor: "pointer",
          }}
        >
          For Developers
        </a>
        <a
          href="#chains"
          style={{
            color: "var(--text-color)",
            textDecoration: "none",
            fontSize: "18px",
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
            cursor: "pointer",
          }}
        >
          Enterprise
        </a>
        <a
          href="#company"
          style={{
            color: "var(--text-color)",
            textDecoration: "none",
            fontSize: "18px",
            cursor: "pointer",
          }}
        >
          Company
        </a>
      </div>

      {/* Sign In & Log In 버튼 */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "20px",
          flexShrink: 0, // 오른쪽 요소가 화면 밖으로 나가지 않도록 고정
        }}
      >
        <button
          style={{
            fontSize: "14px",
            padding: "12px 24px",
            backgroundColor: "transparent",
            border: "2px solid var(--text-color)", // 테두리 색상
            borderRadius: "5px",
            color: "var(--text-color)", // 버튼 텍스트 색상
            cursor: "pointer",
            transition: "background-color 0.3s, color 0.3s, border-color 0.3s", // 부드러운 전환 효과
          }}
        >
          Sign In
        </button>
        <button
          style={{
            fontSize: "14px",
            padding: "12px 24px",
            backgroundColor: "transparent",
            border: "2px solid var(--text-color)", // 테두리 색상
            borderRadius: "5px",
            color: "var(--text-color)", // 버튼 텍스트 색상
            cursor: "pointer",
            transition: "background-color 0.3s, color 0.3s, border-color 0.3s", // 부드러운 전환 효과
          }}
        >
          Log In
        </button>
      </div>
    </div>
  );
};

export default Header;
