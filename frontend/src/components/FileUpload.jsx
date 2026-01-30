import { useState } from "react";
import { validateFile } from "../utils/fileValidation";
import { uploadFinancialFile } from "../api/uploadApi";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    const validationError = validateFile(selectedFile);

    if (validationError) {
      setError(validationError);
      setFile(null);
      return;
    }

    setError("");
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a valid file");
      return;
    }

    try {
      setLoading(true);
      await uploadFinancialFile(file);
      alert("✅ File uploaded successfully");
      setFile(null);
    } catch (err) {
      setError(
        err.response?.data?.error ||
        err.message ||
        "Upload failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        accept=".csv,.xlsx,.pdf"
        onChange={handleFileChange}
      />

      {error && <p style={{ color: "red" }}>{error}</p>}

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
}

export default FileUpload;
