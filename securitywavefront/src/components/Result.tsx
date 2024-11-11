// src/components/Result.tsx
import React from "react";

interface ResultProps {
  result: {
    normal_probability: string;
    virus_probability: string;
    classification: number;
    chart_data: string;
  };
}

const Result: React.FC<ResultProps> = ({ result }) => {
  const classificationText =
    result.classification === 0 ? "Normal" : "Malicious";

  return (
    <div className="result">
      <p>Normal Probability: {result.normal_probability}</p>
      <p>Virus Probability: {result.virus_probability}</p>
      <p>Classification: {classificationText}</p>
      <div className="chart">
        <img
          src={`data:image/png;base64,${result.chart_data}`}
          alt="Pie Chart"
        />
      </div>
    </div>
  );
};

export default Result;
