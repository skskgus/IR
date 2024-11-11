// src/components/FileUpload.tsx
import React from "react";

interface FileUploadProps {
  setResult: React.Dispatch<React.SetStateAction<ResultType | null>>;
}

interface ResultType {
  normal_probability: string;
  virus_probability: string;
  classification: number;
  chart_data: string;
}

const FileUpload: React.FC<FileUploadProps> = ({ setResult }) => {
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById("fileInput") as HTMLInputElement;
    if (fileInput?.files?.[0]) {
      formData.append("file", fileInput.files[0]);

      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      setResult(result);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" id="fileInput" required />
      <button type="submit">Upload</button>
    </form>
  );
};

export default FileUpload;
