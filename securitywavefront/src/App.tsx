// src/App.tsx
import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import Result from "./components/Result";
import "./App.css";

interface ResultType {
  normal_probability: string;
  virus_probability: string;
  classification: number;
  chart_data: string;
}

function App() {
  const [result, setResult] = useState<ResultType | null>(null);

  return (
    <div className="App">
      <h1>Upload a File</h1>
      <FileUpload setResult={setResult} />
      {result && <Result result={result} />}
    </div>
  );
}

export default App;
