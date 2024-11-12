// src/components/Result.tsx
import React from "react";

interface ResultProps {
  result: {
    classification: number;
  };
}

const Result: React.FC<ResultProps> = ({ result }) => {
  const classificationText =
    result.classification === 0 ? "Normal" : "Malicious";

  return (
    <div className="result">
      <p>Classification: {classificationText}</p>
    </div>
  );
};

export default Result;
