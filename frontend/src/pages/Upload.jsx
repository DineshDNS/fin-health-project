import { useState } from "react";
import { uploadFinancialDocument } from "../api/uploadApi";

export default function UploadFinancials() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file to upload");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("file_type", file.name.split(".").pop());

    try {
      setLoading(true);
      setMessage("");

      await uploadFinancialDocument(formData);

      setMessage("File uploaded successfully. Processing started.");
      setFile(null);
    } catch (err) {
      setMessage("Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-full p-8 rounded-3xl
      bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100"
    >
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-slate-900">
          Upload Financials
        </h2>
        <p className="text-sm text-slate-600 mt-1">
          Upload bank statements, GST data, or financial exports
        </p>
      </div>

      {/* Upload Card */}
      <div className="glass-card p-8 max-w-xl">
        <div className="border-2 border-dashed border-rose-300 rounded-2xl p-8 text-center">
          <p className="text-sm text-slate-700 mb-2">
            Drag & drop your financial file here
          </p>
          <p className="text-xs text-slate-500 mb-4">
            Supported formats: CSV, XLSX, PDF
          </p>

          <input
            type="file"
            accept=".csv,.xlsx,.pdf"
            onChange={(e) => setFile(e.target.files[0])}
            className="block mx-auto text-sm"
          />
        </div>

        <button
          onClick={handleUpload}
          disabled={loading}
          className="mt-6 w-full py-3 rounded-xl
            bg-gradient-to-r from-rose-500 to-pink-500
            text-white font-semibold
            hover:opacity-90 transition"
        >
          {loading ? "Uploading..." : "Upload & Process"}
        </button>

        {message && (
          <p className="mt-4 text-sm text-slate-700">
            {message}
          </p>
        )}
      </div>

      {/* Info */}
      <div className="mt-8 max-w-xl text-sm text-slate-600">
        <p>
          All uploaded financial data is encrypted and securely processed.
          This information is used only to generate insights and reports.
        </p>
      </div>
    </div>
  );
}
