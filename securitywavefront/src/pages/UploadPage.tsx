import React from "react";
import { useNavigate } from "react-router-dom";
import FileUpload from "../components/FileUpload";
import logo from "../Landinglogo.png"; // 이미지 파일의 위치에 맞게 경로 수정

const UploadPage: React.FC = () => {
  const navigate = useNavigate();

  // 업로드된 결과를 받아와 결과 페이지로 이동하는 함수
  const handleResult = (data: any) => {
    navigate("/result", { state: { result: data } });
  };

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

      {/* 중앙 파일 업로드 영역 */}
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
        <h1 style={{ fontSize: "36px", marginBottom: "20px" }}>Upload a File</h1>
        <FileUpload setResult={handleResult} />
      </div>
    </div>
  );
};

export default UploadPage;
