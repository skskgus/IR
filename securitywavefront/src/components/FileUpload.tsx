// src/components/FileUpload.tsx
import React, { useState } from "react";

interface FileUploadProps {
  setResult: (data: any) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ setResult }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true); // 로딩 시작
    setError(null); // 기존 오류 초기화

    const formData = new FormData();
    const fileInput = document.getElementById("fileInput") as HTMLInputElement;
    if (fileInput?.files?.[0]) {
      formData.append("file", fileInput.files[0]);

      try {
        const response = await fetch("http://localhost:5000/upload", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        setLoading(false); // 로딩 완료
        setResult(result); // 결과 설정
      } catch (error) {
        setLoading(false);
        console.error("Error uploading file:", error);
        setError("파일 업로드 중 문제가 발생했습니다."); // 사용자에게 표시할 오류 메시지 설정
      }
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" id="fileInput" required />
        <button type="submit">Upload</button>
      </form>
      {loading && <p>로딩 중...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}{" "}
      {/* 오류 메시지 표시 */}
    </div>
  );
};

export default FileUpload;
