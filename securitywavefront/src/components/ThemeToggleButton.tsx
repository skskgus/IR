import React, { useEffect, useState } from "react";

const ThemeToggleButton: React.FC = () => {
  // 초기값을 localStorage에서 가져오거나 기본값 라이트 모드로 설정
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const savedMode = localStorage.getItem("theme");
    return savedMode === "dark"; // 기본값 라이트모드
  });

  useEffect(() => {
    // 화면 모드 설정
    if (isDarkMode) {
      document.body.classList.add("dark-mode");
      document.body.classList.remove("light-mode");
      localStorage.setItem("theme", "dark");
    } else {
      document.body.classList.add("light-mode");
      document.body.classList.remove("dark-mode");
      localStorage.setItem("theme", "light");
    }
  }, [isDarkMode]);

  const toggleTheme = () => {
    setIsDarkMode((prevMode) => !prevMode);
  };

  return (
    <div
      style={{
        position: "fixed",
        bottom: "20px",
        right: "20px",
        display: "flex",
        flexDirection: "column",
        gap: "10px",
      }}
    >
      <button
        onClick={toggleTheme}
        style={{
          fontSize: "14px",
          padding: "10px 20px",
          backgroundColor: "#3a3a3a",
          color: "#ffffff",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        {isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
      </button>
    </div>
  );
};

export default ThemeToggleButton;
