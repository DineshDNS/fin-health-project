import { useState } from "react";
import { Upload, CheckCircle, AlertCircle } from "lucide-react";
import api from "../../../services/apiClient";

/*
  STAGE 1 — UPLOAD ENGINE (FINAL)
  -------------------------------
  - Validates required inputs
  - Ensures year is present and valid
  - Validates file types
  - Auto-clears month/quarter conflict
  - Calls backend upload API
  - Triggers parent refresh
*/

const DOCUMENT_TYPES = [
  { value: "BANK_STATEMENT", label: "Bank Statement" },
  { value: "GST_RETURN", label: "GST Return" },
  { value: "BALANCE_SHEET", label: "Balance Sheet" },
  { value: "PROFIT_AND_LOSS", label: "Profit & Loss" },
];

const ALLOWED_FILE_TYPES = [
  "application/pdf",
  "text/csv",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
];

export default function UploadDocumentCard({ onUploadSuccess }) {
  const [type, setType] = useState("BANK_STATEMENT");
  const [year, setYear] = useState("");
  const [month, setMonth] = useState("");
  const [quarter, setQuarter] = useState("");
  const [source, setSource] = useState("");
  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  // ---------------- VALIDATION ----------------
  const validate = () => {
    if (!file) return "Please select a file";

    if (!year || year.trim() === "") {
      return "Year is required";
    }

    if (!/^\d{4}$/.test(year)) {
      return "Enter a valid 4-digit year (e.g., 2024)";
    }

    if (!ALLOWED_FILE_TYPES.includes(file.type)) {
      return "Only PDF, CSV, XLSX files are allowed";
    }

    return "";
  };

  // ---------------- UPLOAD HANDLER ----------------
  const handleUpload = async () => {
    setError("");
    setSuccess(false);

    const validationError = validate();
    if (validationError) {
      setError(validationError);
      return;
    }

    const form = new FormData();
    form.append("type", type);
    form.append("year", year);

    if (month) form.append("month", month);
    if (quarter) form.append("quarter", quarter);
    if (source) form.append("source", source);

    form.append("file", file);

    try {
      setLoading(true);
      await api.post("/documents/upload/", form);

      // Reset form
      setFile(null);
      setYear("");
      setMonth("");
      setQuarter("");
      setSource("");
      setSuccess(true);

      onUploadSuccess?.();
    } catch (err) {
      console.error("Upload failed:", err);
      setError("Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-[70vw] h-[52vh] flex flex-row rounded-[2rem] shadow-2xl overflow-hidden bg-white border border-orange-100/60">

      {/* LEFT PANEL */}
      <div className="w-2/5 relative bg-gradient-to-br from-[#ffb3a1] via-[#f9957f] to-[#f06e5b] p-10 text-white flex flex-col justify-between">
        <div>
          <h2 className="text-4xl font-bold">Upload</h2>
          <p className="text-white/90 text-sm mt-2">
            Add your financial documents for analysis.
          </p>
        </div>

        {/* FILE DROP */}
        <div>
          <div
            className={`relative border-2 border-dashed rounded-2xl p-6 h-36 flex items-center justify-center transition-all duration-300 ${
              file
                ? "border-white bg-white/20 scale-105"
                : "border-white/40 bg-black/5 hover:bg-black/10 hover:scale-105"
            }`}
          >
            <input
              type="file"
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <div className="text-center">
              {file ? (
                <div className="flex flex-col items-center">
                  <CheckCircle className="w-9 h-9 text-white mb-1" />
                  <p className="text-sm font-medium truncate max-w-[170px]">
                    {file.name}
                  </p>
                </div>
              ) : (
                <div className="flex flex-col items-center">
                  <Upload className="w-9 h-9 text-white/80 mb-1" />
                  <p className="text-sm font-semibold uppercase tracking-tight">
                    Drop File
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* SUCCESS MESSAGE */}
        {success && (
          <div className="text-sm font-semibold flex items-center gap-2">
            <CheckCircle size={16} /> Uploaded successfully
          </div>
        )}

        <div className="absolute -bottom-10 -left-10 w-44 h-44 bg-white/20 rounded-full blur-3xl"></div>
      </div>

      {/* RIGHT PANEL */}
      <div className="w-3/5 p-10 flex flex-col justify-between bg-white">
        <div className="space-y-6">

          {/* TYPE + SOURCE */}
          <div className="grid grid-cols-2 gap-5">
            <div>
              <label className="text-xs uppercase font-bold text-gray-600">
                Document Type
              </label>
              <select
                className="w-full mt-1 p-3 border border-gray-300 rounded-xl text-sm font-medium"
                value={type}
                onChange={(e) => setType(e.target.value)}
              >
                {DOCUMENT_TYPES.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-xs uppercase font-bold text-gray-600">
                Source (optional)
              </label>
              <input
                className="w-full mt-1 p-3 border border-gray-300 rounded-xl text-sm font-medium"
                value={source}
                onChange={(e) => setSource(e.target.value)}
                placeholder="HDFC, GST Portal..."
              />
            </div>
          </div>

          {/* DATE FIELDS */}
          <div className="grid grid-cols-3 gap-4">
            <input
              type="number"
              min="2000"
              max="2100"
              className="p-3 border border-gray-300 rounded-xl text-sm font-medium"
              placeholder="Year *"
              value={year}
              onChange={(e) => setYear(e.target.value)}
            />

            <input
              className="p-3 border border-gray-300 rounded-xl text-sm font-medium"
              placeholder="Month"
              value={month}
              onChange={(e) => {
                setMonth(e.target.value);
                setQuarter("");
              }}
            />

            <input
              className="p-3 border border-gray-300 rounded-xl text-sm font-medium"
              placeholder="Quarter"
              value={quarter}
              onChange={(e) => {
                setQuarter(e.target.value);
                setMonth("");
              }}
            />
          </div>

          {/* ERROR MESSAGE */}
          {error && (
            <div className="flex items-center gap-2 text-red-600 text-sm font-medium">
              <AlertCircle size={16} />
              {error}
            </div>
          )}
        </div>

        {/* SUBMIT */}
        <button
          onClick={handleUpload}
          disabled={loading || !file}
          className={`w-full py-5 rounded-xl font-bold text-white text-lg shadow-xl transition-all duration-300 ${
            loading || !file
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-gradient-to-r from-[#f06e5b] via-[#f9957f] to-[#ffb3a1] hover:scale-[1.02]"
          }`}
        >
          {loading ? "Uploading..." : "Finish Upload"}
        </button>
      </div>
    </div>
  );
}
