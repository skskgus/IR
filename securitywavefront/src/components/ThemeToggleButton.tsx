import React, { useState } from "react";

const ThemeToggleButton: React.FC = () => {
  const [isDarkMode, setIsDarkMode] = useState(true);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
    // Body에 테마 클래스 추가
    document.body.className = isDarkMode ? "light-mode" : "dark-mode";
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
