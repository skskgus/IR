// src/pages/UploadPage.tsx
import React from "react";
import { useNavigate } from "react-router-dom";
import FileUpload from "../components/FileUpload";

function UploadPage() {
  const navigate = useNavigate();

  // 업로드된 결과를 받아와 결과 페이지로 이동하는 함수
  const handleResult = (data: any) => {
    navigate("/result", { state: { result: data } });
  };

  return (
    <div>
      <h1>Upload a File</h1>
      <FileUpload setResult={handleResult} />
    </div>
  );
}

export default UploadPage;
