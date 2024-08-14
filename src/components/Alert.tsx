import React from "react";

interface AlertProps {
  message: string;
  type: string;
}

const Alert: React.FC<AlertProps> = ({ message, type }) => {
  return (
    <div className="alert-container">
      <div className={type}>{message}</div>
    </div>
  );
};

export default Alert;
