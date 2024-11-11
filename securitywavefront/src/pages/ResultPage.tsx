// src/pages/ResultPage.tsx
import React from "react";
import { useLocation } from "react-router-dom";
import Result from "../components/Result";

function ResultPage() {
  const location = useLocation();
  const result = location.state?.result;

  return (
    <div>
      <h1>Analysis Result</h1>
      {result ? <Result result={result} /> : <p>No result available.</p>}
    </div>
  );
}

export default ResultPage;
