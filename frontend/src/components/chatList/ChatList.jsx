import { Link } from "react-router-dom";
import "./chatList.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faComment } from "@fortawesome/free-solid-svg-icons";
const ChatList = () => {
  return (
    <div className="chatList">
      <span className="title">Video Captioning System</span>
      <Link to="/dashboard">
        Create a new 
        <FontAwesomeIcon icon={faComment} />
      </Link>
    </div>
  );
};

export default ChatList;
