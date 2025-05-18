import "./dashboardPage.css";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

const DashboardPage = () => {
  const [videoSrc, setVideoSrc] = useState(null);
  const [youtubeURL, setYoutubeURL] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [predictionResult, setPredictionResult] = useState("");

  const [loading, setLoading] = useState(false);

  const location = useLocation();

  //Lay video tu query parameter
  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const videoParam = queryParams.get("video"); //Lay video tu query parameter
    if (videoParam) {
      if (videoParam.includes("youtube.com")) {
        const videoId = videoParam.split("v=")[1]?.split("&")[0];
        if (videoId) {
          setVideoSrc(`https://www.youtube.com/embed/${videoId}`);
        }
      } else {
        setVideoSrc(videoParam); //Neu khoing phai youtube, lay video tu link
      }
    }
  }, [location]);

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const videoURL = URL.createObjectURL(file);
      setVideoSrc(videoURL);
    }
  };

  const handleYoutubeSubmit = (e) => {
    e.preventDefault();
    const videoId = youtubeURL.split("v=")[1]?.split("&")[0];
    if (videoId) {
      setVideoSrc(`https://www.youtube.com/embed/${videoId}`);
    }
  };

  const handlePredict = async () => {
    if (!videoSrc) {
      alert("Please upload a video or provide a YouTube URL.");
      return;
    }
    setLoading(true);
    try {
      let response;
      if (videoSrc.includes("youtube.com")) {
        // Gửi URL YouTube đến API
        response = await fetch("http://localhost:5000/api/predict", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ file_name: videoSrc }),
        });
      } else {
        // Gửi tệp video đến API
        const formData = new FormData();
        const videoFile = document.getElementById("videoUpload").files[0];
        if (!videoFile) {
          alert("Please upload a video file.");
          return;
        }
        formData.append("file", videoFile);

        response = await fetch("http://localhost:5000/api/predict", {
          method: "POST",
          body: formData,
        });
      }

      const data = await response.json();
      if (!data.caption) {
        throw new Error("No caption returned from API.");
      }
      setPredictionResult(data.caption); // Lưu kết quả dự đoán
    } catch (error) {
      console.error("Error predicting video:", error);
      alert("An error occurred while predicting the video.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboardPage">
      {/* <div className="texts">
        <div className="logo">
          <img src="/logo.png" alt="" />
          <h1>VIRE SYSTEM</h1>
        </div>
      </div>
  
      <div className="formContainer">
        <form>
          <input type="text" name="text" placeholder="Ask me anything..." />
          <button>
            <img src="/arrow.png" alt="" />
          </button>
        </form>
      </div>  */}
      <button
        className="uploadBtn"
        onClick={() => document.getElementById("videoUpload").click()}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="22"
          height="22"
          fill="none"
          viewBox="0 0 24 24"
          style={{ marginRight: "8px" }}
        >
          <path
            fill="currentColor"
            d="M12 16V4m0 0l-4 4m4-4l4 4M4 20h16"
            stroke="#fff"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        Upload from your computer
      </button>
      <input
        id="videoUpload"
        type="file"
        accept="video/*"
        style={{ display: "none" }}
        onChange={handleUpload}
      />

      <button onClick={() => setShowForm(!showForm)} className="uploadBtn">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="22"
          height="22"
          fill="none"
          viewBox="0 0 24 24"
          style={{ marginRight: "8px" }}
        >
          <path
            fill="currentColor"
            d="M12 16V4m0 0l-4 4m4-4l4 4M4 20h16"
            stroke="#fff"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        Upload from URL
      </button>
      <div className={`youtubeFormContainer ${showForm ? "show" : ""}`}>
        <form onSubmit={handleYoutubeSubmit} className="youtubeForm">
          <input
            type="text"
            placeholder="Enter YouTube URL"
            value={youtubeURL}
            onChange={(e) => setYoutubeURL(e.target.value)}
          />
          <button type="submit" className="uploadBtn">
            Submit
          </button>
        </form>
      </div>
      <div className="content">
        <div className="videoscreen">
          {videoSrc ? (
            videoSrc.includes("youtube.com") ? (
              <iframe
                src={videoSrc}
                title="YouTube Video"
                width="100%"
                height="100%"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
            ) : (
              <video src={videoSrc} controls width="100%" height="100%" />
            )
          ) : (
            "VIDEO UPLOAD"
          )}
        </div>
        <div className="retrievalevent">
          {loading ? (
            <div className="spinner"></div>
          ) : predictionResult ? (
            <p>{predictionResult}</p>
          ) : (
            <>
              Sự kiện từ video của bạn{" "}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="24"
                viewBox="0 0 24 24"
                width="24"
              >
                <path d="M0 0h24v24H0V0z" fill="none" />
                <path d="M21 3H3c-1.11 0-2 .89-2 2v12c0 1.1.89 2 2 2h5v2h8v-2h5c1.1 0 1.99-.9 1.99-2L23 5c0-1.11-.9-2-2-2zm0 14H3V5h18v12zm-5-6l-7 4V7z" />
              </svg>
            </>
          )}
        </div>
      </div>

      <button className="btnSum" onClick={handlePredict}>
        Run
        <img src="/send.png" alt="" />
      </button>
    </div>
  );
};

export default DashboardPage;
