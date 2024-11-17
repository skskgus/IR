import React from "react";

interface ResultProps {
  result: {
    classification: number; // classification 값 사용
  };
}

const Result: React.FC<ResultProps> = ({ result }) => {
  const { classification } = result;

  // classification 값에 따라 상태 결정
  const isMalicious = classification > 0.5; // 기준값 0.5 예시 (필요에 따라 변경 가능)

  return (
    <div
      style={{
        fontSize: "24px",
        fontWeight: "bold",
        color: isMalicious ? "#ff4d4d" : "#4caf50", // 빨간색 또는 초록색
        textTransform: "capitalize",
      }}
    >
      {isMalicious ? "Malicious" : "Normal"}
    </div>
  );
};

export default Result;
