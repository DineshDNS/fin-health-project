import { useState } from "react";
import { uploadFinancialDocument } from "../api/uploadApi";

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
    } catch {
      setMessage("Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-full flex justify-center items-start p-10 bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100">
      <div className="w-full max-w-3xl">
        {/* Header */}
        <div className="mb-8 text-center">
          <h2 className="text-2xl font-semibold text-slate-900">
            Upload Financial Documents
          </h2>
          <p className="text-sm text-slate-600 mt-2">
            Upload documents to assess financial health and generate insights
          </p>
        </div>

        {/* Form Card */}
        <div className="glass-card p-10 space-y-6">
          {/* Step 1 */}
          <div>
            <label className="text-sm font-medium text-slate-700">
              1. Document Category *
            </label>
            <select
              value={category}
              onChange={(e) => {
                setCategory(e.target.value);
                setDocType("");
              }}
              className="mt-2 w-full rounded-lg border-slate-300"
            >
              <option value="">Select category</option>
              <option value="FIN">Financial Statements</option>
              <option value="BANK">Bank Statements</option>
              <option value="GST">GST Returns</option>
            </select>
          </div>

          {/* Step 2 */}
          <div>
            <label className="text-sm font-medium text-slate-700">
              2. Document Type *
            </label>
            <select
              value={docType}
              onChange={(e) => setDocType(e.target.value)}
              disabled={!category}
              className="mt-2 w-full rounded-lg border-slate-300 disabled:bg-slate-100"
            >
              <option value="">
                {category ? "Select document type" : "Select category first"}
              </option>
              {category &&
                documentTypeOptions[category].map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
            </select>
          </div>

          {/* Step 3 */}
          <div>
            <label className="text-sm font-medium text-slate-700">
              3. Period Covered *
            </label>
            <div className="mt-2 grid grid-cols-1 sm:grid-cols-2 gap-4">
              <input
                type="date"
                value={periodFrom}
                onChange={(e) => setPeriodFrom(e.target.value)}
                className="rounded-lg border-slate-300"
              />
              <input
                type="date"
                value={periodTo}
                onChange={(e) => setPeriodTo(e.target.value)}
                className="rounded-lg border-slate-300"
              />
            </div>
          </div>

          {/* Step 4 */}
          <div>
            <label className="text-sm font-medium text-slate-700">
              4. Source (optional)
            </label>
            <input
              type="text"
              value={source}
              onChange={(e) => setSource(e.target.value)}
              placeholder="e.g. HDFC Bank, GST Portal, Tally"
              className="mt-2 w-full rounded-lg border-slate-300"
            />
          </div>

          {/* Step 5 */}
          <div className="border-2 border-dashed border-rose-300 rounded-2xl p-8 text-center">
            <p className="text-sm font-medium text-slate-700 mb-1">
              5. Upload File *
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

          {/* Submit */}
          <button
            onClick={handleUpload}
            disabled={loading}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-rose-500 to-pink-500 text-white font-semibold hover:opacity-90 transition"
          >
            {loading ? "Uploading..." : "Upload & Process"}
          </button>

          {message && (
            <p className="text-sm text-center text-slate-700">
              {message}
            </p>
          )}
        </div>

        {/* Footer note */}
        <p className="mt-6 text-xs text-center text-slate-600">
          You can upload multiple documents over time to improve analysis accuracy.
          All data is encrypted and securely processed.
        </p>
      </div>
    </div>
  );
}
