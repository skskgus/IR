// src/pages/Register.tsx
import React from "react";
import { useNavigate } from "react-router-dom";
import logo from "../Landinglogo.png"; // 이미지 파일의 위치에 맞게 경로 수정

const Register: React.FC = () => {
  const navigate = useNavigate(); // 컴포넌트 내부로 이동

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
        onClick={() => navigate("/")} // 로고 클릭 시 LandingPage로 이동
        style={{
          position: "absolute",
          top: "0px",
          left: "0px",
          width: "10%",
          maxWidth: "90px",
          height: "auto",
          margin: "0",
          cursor: "pointer", // 클릭 가능하도록 커서 변경
        }}
      />

      <h1 style={{ fontSize: "36px", marginBottom: "20px" }}>Sign Up</h1>
      <form
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "15px",
          width: "300px",
        }}
      >
        <input
          type="text"
          placeholder="Username"
          style={{
            padding: "10px",
            borderRadius: "5px",
            border: "1px solid #ccc",
            fontSize: "16px",
          }}
        />
        <input
          type="email"
          placeholder="Email"
          style={{
            padding: "10px",
            borderRadius: "5px",
            border: "1px solid #ccc",
            fontSize: "16px",
          }}
        />
        <input
          type="password"
          placeholder="Password"
          style={{
            padding: "10px",
            borderRadius: "5px",
            border: "1px solid #ccc",
            fontSize: "16px",
          }}
        />
        <button
          type="submit"
          style={{
            padding: "10px 20px",
            fontSize: "18px",
            backgroundColor: "#3a3a3a",
            border: "2px solid #ffffff",
            borderRadius: "5px",
            color: "#ffffff",
            cursor: "pointer",
          }}
        >
          Sign Up
        </button>
      </form>
    </div>
  );
};

export default Register;
