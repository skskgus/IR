import React from "react";

interface ResultProps {
  result: {
    classification: number; // classification 값 사용
    second_row_fourth_column: string; // 추가 데이터
  };
}

const Result: React.FC<ResultProps> = ({ result }) => {
  const { classification, second_row_fourth_column } = result;

  // classification 값에 따라 상태 결정
  const isMalicious = classification > 0.5; // 기준값 0.5 예시 (필요에 따라 변경 가능)

  // second_row_fourth_column 데이터를 ';' 기준으로 분리한 뒤 글자와 ::, []로 나누기
  const formattedTechniques = second_row_fourth_column
    ? second_row_fourth_column.split(";").map((technique, index) => {
        const [textWithOptional, code] = technique.trim().split(/\s*\[(.*)\]/); // '글자::옵션'과 '[코드]' 분리
        let [mainText, optionalText] = textWithOptional.split("::"); // '글자'와 '::뒤의 옵션' 분리

        // 첫 번째 열의 텍스트에서 맨 앞의 ':' 제거
        mainText = mainText.trim().startsWith(":")
          ? mainText.trim().slice(1).trim()
          : mainText.trim();

        // 소수점 제거 로직: T1547.009 -> T1547
        const codeWithoutDecimal = code?.includes(".")
          ? code.split(".")[0]
          : code || "N/A";

        // MITRE 링크 생성
        const mitreLink = `https://attack.mitre.org/techniques/${codeWithoutDecimal}`;

        return (
          <tr key={index}>
            <td
              style={{ padding: "8px", border: "1px solid var(--text-color)" }}
            >
              {mainText}
            </td>
            <td
              style={{ padding: "8px", border: "1px solid var(--text-color)" }}
            >
              {optionalText?.trim() || "none"} {/* :: 뒤의 옵션, 없으면 none */}
            </td>
            <td
              style={{ padding: "8px", border: "1px solid var(--text-color)" }}
            >
              {code || "N/A"} {/* 원래 코드 */}
            </td>
            <td
              style={{ padding: "8px", border: "1px solid var(--text-color)" }}
            >
              <a
                href={mitreLink}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  color: "var(--text-color)",
                  textDecoration: "underline", // 밑줄 추가
                }}
              >
                {mitreLink}
              </a>
            </td>
          </tr>
        );
      })
    : null;

  return (
    <div
      style={{
        textAlign: "center", // 텍스트 중앙 정렬
        marginTop: "50px", // 상단 여백 추가
      }}
    >
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

      {/* second_row_fourth_column 내용 표시 */}
      <div
        style={{
          marginTop: "20px", // 상단과의 간격 추가
          fontSize: "18px",
          color: "var(--text-color)", // CSS 변수로 텍스트 색상
        }}
      >
        {formattedTechniques ? (
          <table
            style={{
              margin: "20px auto", // 테이블 중앙 정렬
              borderCollapse: "collapse", // 테이블 경계선 제거
              width: "80%", // 테이블 너비 설정
            }}
          >
            <thead>
              <tr>
                <th
                  style={{
                    padding: "10px",
                    border: "1px solid var(--text-color)",
                    backgroundColor: "var(--background-color)",
                    color: "var(--text-color)",
                  }}
                >
                  Technique
                </th>
                <th
                  style={{
                    padding: "10px",
                    border: "1px solid var(--text-color)",
                    backgroundColor: "var(--background-color)",
                    color: "var(--text-color)",
                  }}
                >
                  Details (Optional)
                </th>
                <th
                  style={{
                    padding: "10px",
                    border: "1px solid var(--text-color)",
                    backgroundColor: "var(--background-color)",
                    color: "var(--text-color)",
                  }}
                >
                  Code
                </th>
                <th
                  style={{
                    padding: "10px",
                    border: "1px solid var(--text-color)",
                    backgroundColor: "var(--background-color)",
                    color: "var(--text-color)",
                  }}
                >
                  MITRE Link
                </th>
              </tr>
            </thead>
            <tbody>{formattedTechniques}</tbody>
          </table>
        ) : (
          <div>No data available</div> // 데이터가 없을 경우
        )}
      </div>
    </div>
  );
};

export default Result;
