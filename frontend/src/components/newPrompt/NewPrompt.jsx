import React from "react";
import "./newPrompt.css";
import Upload from "../upload/Upload";

const NewPrompt = () => {
  return (
    <>
      {/* ADD NEW CHAT */}
      <div className="message user">User's question will appear here</div>
      <div className="message">AI's answer will appear here</div>
      <div className="endChat"></div>
      <form className="newForm">
        <Upload />
        <input id="file" type="file" multiple={false} hidden />
        <input type="text" name="text" placeholder="Ask anything..." />
        <button>
          <img src="/arrow.png" alt="" />
        </button>
      </form>
    </>
  );
};

export default NewPrompt;
