import { useState } from "react";

export default function ImageUpload({ onUpload, isLoading }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [dragOver, setDragOver] = useState(false);

  const handleFileSelect = (selectedFile) => {
    if (selectedFile && selectedFile.type.startsWith("image/")) {
      setFile(selectedFile);
      const reader = new FileReader();
      reader.onload = (e) => setPreview(e.target.result);
      reader.readAsDataURL(selectedFile);
    } else {
      alert("Please select a valid image file");
    }
  };

  const handleInputChange = (e) => {
    handleFileSelect(e.target.files[0]);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFileSelect(e.dataTransfer.files[0]);
  };

  const handleSubmit = () => {
    if (file) onUpload(file);
  };

  const handleClear = () => {
    setFile(null);
    setPreview(null);
  };

  return (
    <div className={`image-upload ${dragOver ? "drag-over" : ""}`}
         onDragOver={handleDragOver}
         onDragLeave={handleDragLeave}
         onDrop={handleDrop}>
      {!preview ? (
        <div className="file-input-wrapper">
          <input
            type="file"
            id="file-input"
            accepts="image/*"
            onChange={handleInputChange}
          />
          <label htmlFor="file-input" className="upload-label">
            <span className="upload-icon">📷</span>
            <span>Click to upload or drag and drop</span>
            <span style={{ fontSize: "12px", color: "#999" }}>
              PNG, JPG, GIF up to 10MB
            </span>
          </label>
        </div>
      ) : (
        <>
          <img src={preview} alt="Preview" className="image-preview" />
          <p className="file-info">✓ {file.name}</p>
          <button
            className="btn btn-secondary"
            onClick={handleClear}
            style={{ marginBottom: "10px" }}
          >
            Change Image
          </button>
        </>
      )}
      
      <button
        className="btn btn-primary"
        onClick={handleSubmit}
        disabled={!file || isLoading}
        style={{ marginTop: file ? "0" : "15px" }}
      >
        {isLoading ? (
          <>
            <span className="loading-spinner"></span> Scanning...
          </>
        ) : (
          "🔍 Scan Label"
        )}
      </button>
    </div>
  );
}
