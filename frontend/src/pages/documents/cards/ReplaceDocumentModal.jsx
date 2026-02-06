import { useState } from "react";
import api from "../../../services/apiClient";

export default function ReplaceDocumentModal({
  doc,
  onClose,
  onSuccess,
}) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleReplace = async () => {
    if (!file) {
      setError("Please select a file");
      return;
    }

    setError("");

    const form = new FormData();
    form.append("document_id", doc.id);
    form.append("type", doc.type);
    form.append("year", doc.year);
    form.append("file", file);

    if (doc.month !== null && doc.month !== undefined)
      form.append("month", doc.month);

    if (doc.quarter)
      form.append("quarter", doc.quarter);

    if (doc.source)
      form.append("source", doc.source);

    try {
      setLoading(true);
      await api.post("/documents/replace/", form);

      onSuccess();
      onClose();
    } catch (err) {
      console.error("Replace failed:", err);

      // 🔥 Extract backend error message
      const backendMsg =
        err?.response?.data?.message ||
        "Replace failed. Please try again.";

      setError(backendMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">

      {/* DARK BACKDROP */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* GLASS MODAL */}
      <div
        className="
          relative
          w-[460px]
          rounded-3xl
          p-7
          shadow-[0_20px_60px_rgba(0,0,0,0.35)]
          border border-white/40
          bg-white/70
          backdrop-blur-2xl
        "
      >
        {/* glow accents */}
        <div className="absolute -top-10 -right-10 w-40 h-40 bg-indigo-400/40 blur-3xl rounded-full" />
        <div className="absolute -bottom-10 -left-10 w-40 h-40 bg-purple-400/40 blur-3xl rounded-full" />

        <div className="relative">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">
            Replace Document
          </h2>

          <p className="text-sm text-gray-600 mb-5">
            {doc.type} — {doc.year}
          </p>

          {/* FILE INPUT */}
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="
              w-full mb-4
              bg-white/80
              border border-gray-300
              rounded-xl
              p-3
              text-sm
              focus:ring-2 focus:ring-indigo-400
              outline-none
            "
          />

          {/* 🔴 ERROR MESSAGE */}
          {error && (
            <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm">
              {error}
            </div>
          )}

          {/* ACTIONS */}
          <div className="flex justify-end gap-3">
            <button
              onClick={onClose}
              className="
                px-4 py-2 rounded-xl
                border border-gray-300
                bg-white/80
                text-gray-700
                hover:bg-white
              "
            >
              Cancel
            </button>

            <button
              onClick={handleReplace}
              disabled={!file || loading}
              className={`
                px-5 py-2 rounded-xl font-semibold text-white
                ${
                  !file || loading
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-gradient-to-r from-indigo-600 to-purple-600 hover:scale-[1.02]"
                }
              `}
            >
              {loading ? "Replacing..." : "Replace"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
