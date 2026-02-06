import { useEffect, useState } from "react";
import api from "../../../services/apiClient";

export default function HistoryModal({ documentId, onClose }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get(`/documents/history/${documentId}/`);
        setHistory(res.data.data || []);
      } catch (err) {
        console.error("History fetch failed", err);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [documentId]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">

      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/35 backdrop-blur-[2px]"
        onClick={onClose}
      />

      {/* Gradient border wrapper */}
      <div className="relative p-[1.5px] rounded-3xl bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-400">

        {/* Glass Card */}
        <div
          className="
            w-[580px]
            max-h-[80vh]
            rounded-3xl
            bg-white/75
            backdrop-blur-xl
            border border-white/40
            shadow-[0_20px_60px_rgba(0,0,0,0.25)]
            p-8
          "
        >
          {/* Header */}
          <div className="mb-7">
            <h2 className="text-xl font-semibold text-gray-900 tracking-tight">
              Document History
            </h2>
            <p className="text-sm text-gray-500 mt-1">
              Complete audit trail of document lifecycle events
            </p>
          </div>

          {/* Content */}
          {loading ? (
            <div className="text-sm text-gray-500">Loading history…</div>
          ) : history.length === 0 ? (
            <div className="text-sm text-gray-500">No history available</div>
          ) : (
            <div className="relative space-y-7 overflow-y-auto pr-2 max-h-[420px]">

              {/* Timeline line */}
              <div className="absolute left-3 top-1 bottom-1 w-px bg-gradient-to-b from-gray-200 via-gray-300 to-gray-200" />

              {history.map((item, index) => (
                <div key={index} className="relative pl-10">

                  {/* Neon timeline dot */}
                  <div className="absolute left-[5px] top-[7px] w-3 h-3 rounded-full bg-gradient-to-r from-indigo-500 to-cyan-400 shadow-[0_0_6px_rgba(79,70,229,0.6)]" />

                  <div>
                    <div className="text-sm font-semibold text-gray-900 tracking-tight">
                      {item.action}
                    </div>

                    <div className="text-xs text-gray-500 mt-1">
                      {new Date(item.timestamp).toLocaleString()}
                    </div>
                  </div>

                </div>
              ))}
            </div>
          )}

          {/* Footer */}
          <div className="mt-8 pt-5 border-t border-gray-200 flex justify-end">
            <button
              onClick={onClose}
              className="
                text-sm font-medium
                text-gray-600
                hover:text-gray-900
                transition
              "
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
