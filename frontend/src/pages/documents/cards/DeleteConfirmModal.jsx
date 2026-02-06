import { useState } from "react";
import api from "../../../services/apiClient";

export default function DeleteConfirmModal({
  doc,
  onClose,
  onSuccess,
}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleDelete = async () => {
    try {
      setLoading(true);
      setError("");

      const form = new FormData();
      form.append("document_id", doc.id);

      await api.post("/documents/delete/", form);

      // refresh table
      await onSuccess();

      // close modal
      onClose();
    } catch (err) {
      const msg =
        err?.response?.data?.message ||
        "Delete failed. Please try again.";

      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/40 backdrop-blur-[2px]"
        onClick={onClose}
      />

      {/* Gradient border */}
      <div className="relative p-[1.5px] rounded-3xl bg-gradient-to-r from-red-400 via-rose-400 to-pink-400">

        {/* Glass card */}
        <div className="
          w-[460px]
          rounded-3xl
          bg-white/80
          backdrop-blur-xl
          border border-white/40
          shadow-[0_20px_60px_rgba(0,0,0,0.25)]
          p-7
        ">
          <h2 className="text-lg font-semibold text-gray-900">
            Delete Document
          </h2>

          <p className="text-sm text-gray-500 mt-1 mb-5">
            This action cannot be undone.
          </p>

          <div className="bg-gray-50 border border-gray-200 rounded-xl p-3 text-sm mb-4">
            <div className="font-medium text-gray-900">
              {doc.type}
            </div>
            <div className="text-gray-500">
              Year: {doc.year}
            </div>
          </div>

          {error && (
            <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm">
              {error}
            </div>
          )}

          <div className="flex justify-end gap-3 mt-6">
            <button
              onClick={onClose}
              className="px-4 py-2 text-sm rounded-xl border border-gray-300 text-gray-700 bg-white hover:bg-gray-50"
            >
              Cancel
            </button>

            <button
              onClick={handleDelete}
              disabled={loading}
              className={`px-5 py-2 text-sm rounded-xl font-semibold text-white ${
                loading
                  ? "bg-gray-400"
                  : "bg-gradient-to-r from-red-600 to-rose-600 hover:scale-[1.02]"
              }`}
            >
              {loading ? "Deleting..." : "Delete"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}