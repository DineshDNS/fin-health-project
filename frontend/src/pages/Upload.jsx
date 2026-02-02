import { useState } from "react";
import { uploadFinancialDocument } from "../api/ingestionApi";

export default function UploadFinancials() {
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState("");
  const [docType, setDocType] = useState("");
  const [periodFrom, setPeriodFrom] = useState("");
  const [periodTo, setPeriodTo] = useState("");
  const [source, setSource] = useState("");

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const documentTypeOptions = {
    FIN: [
      { value: "PL", label: "Profit & Loss Statement" },
      { value: "BS", label: "Balance Sheet" },
      { value: "CF", label: "Cash Flow Statement" },
    ],
    BANK: [{ value: "BANK", label: "Bank Statement" }],
    GST: [
      { value: "GSTR1", label: "GSTR-1 (Sales)" },
      { value: "GSTR3B", label: "GSTR-3B (Summary)" },
    ],
  };

  const handleUpload = async () => {
    if (!file || !category || !docType || !periodFrom || !periodTo) {
      setMessage("Please complete all required fields.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("category", category);
    formData.append("document_type", docType);
    formData.append("period_from", periodFrom);
    formData.append("period_to", periodTo);
    formData.append("source", source);

    try {
      setLoading(true);
      setMessage("");

      await uploadFinancialDocument(formData);

      setMessage("Upload successful. File is being processed.");

      setFile(null);
      setCategory("");
      setDocType("");
      setPeriodFrom("");
      setPeriodTo("");
      setSource("");
    } catch (error) {
      console.error(error);
      setMessage("Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-full flex justify-center items-start p-10 bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100">
      <div className="w-full max-w-3xl">
        <div className="mb-8 text-center">
          <h2 className="text-2xl font-semibold text-slate-900">
            Upload Financial Documents
          </h2>
          <p className="text-sm text-slate-600 mt-2">
            Upload documents to assess financial health and generate insights
          </p>
        </div>

        <div className="glass-card p-10 space-y-6">
          {/* Category */}
          <select
            value={category}
            onChange={(e) => {
              setCategory(e.target.value);
              setDocType("");
            }}
            className="w-full rounded-lg border px-3 py-2"
          >
            <option value="">Select category</option>
            <option value="FIN">Financial Statements</option>
            <option value="BANK">Bank Statements</option>
            <option value="GST">GST Returns</option>
          </select>

          {/* Document Type */}
          <select
            value={docType}
            onChange={(e) => setDocType(e.target.value)}
            disabled={!category}
            className="w-full rounded-lg border px-3 py-2"
          >
            <option value="">Select document type</option>
            {category &&
              documentTypeOptions[category].map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
          </select>

          {/* Period */}
          <div className="grid grid-cols-2 gap-4">
            <input
              type="date"
              value={periodFrom}
              onChange={(e) => setPeriodFrom(e.target.value)}
              className="rounded-lg border px-3 py-2"
            />
            <input
              type="date"
              value={periodTo}
              onChange={(e) => setPeriodTo(e.target.value)}
              className="rounded-lg border px-3 py-2"
            />
          </div>

          {/* Source */}
          <input
            type="text"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            placeholder="Source (optional)"
            className="rounded-lg border px-3 py-2"
          />

          {/* File */}
          <div className="border-2 border-dashed rounded-xl p-6 text-center bg-white/40">
            <input
              type="file"
              accept=".csv,.xlsx,.pdf"
              onChange={(e) => setFile(e.target.files[0])}
              className="mx-auto"
            />
            <p className="text-xs text-slate-500 mt-2">
              Supported formats: CSV, XLSX, PDF
            </p>
          </div>

          <button
            onClick={handleUpload}
            disabled={loading}
            className="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 transition text-white font-semibold shadow-md"
          >
            {loading ? "Uploading..." : "Upload & Process"}
          </button>

          {message && <p className="text-center text-sm">{message}</p>}
        </div>
      </div>
    </div>
  );
}
