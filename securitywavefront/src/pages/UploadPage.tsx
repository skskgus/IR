import React from "react";
import { useNavigate } from "react-router-dom";
import FileUpload from "../components/FileUpload";
import logo from "../Landinglogo.png"; // 이미지 파일의 위치에 맞게 경로 수정

const UploadPage: React.FC = () => {
  const navigate = useNavigate();

  // 업로드된 결과와 파일 이름을 받아 결과 페이지로 이동하는 함수
  const handleResult = (data: any, fileName: string) => {
    console.log("API Response Data:", data); // 응답 데이터 로그 출력
    console.log("Uploaded File Name:", fileName); // 업로드한 파일 이름 출력
    navigate("/result", { state: { result: data, fileName } });
  };

  return (
    <div
      style={{
        position: "relative",
        height: "100vh",
        backgroundColor: "var(--background-color)", // CSS 변수 사용
        color: "var(--text-color)", // CSS 변수 사용
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* 중앙 파일 업로드 영역 */}
      <div
        style={{
          width: "70%",
          maxWidth: "1000px",
          backgroundColor: "var(--background-color)", // 다크/라이트 모드에 따라 동적 변경
          border: "1px solid var(--text-color)", // 다크/라이트 모드 경계색
          padding: "30px",
          borderRadius: "10px",
          textAlign: "center",
          boxShadow: "0 4px 10px rgba(0, 0, 0, 0.5)",
        }}
      >
        <h1 style={{ fontSize: "36px", marginBottom: "20px" }}>
          Upload a File
        </h1>
        <FileUpload setResult={handleResult} />
      </div>
    </div>
  );
};

export default UploadPage;
