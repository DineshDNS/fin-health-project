import { useState } from "react";
import {
  FileText,
  Landmark,
  Receipt,
  Trash2,
  RotateCcw,
  Clock,
  Search,
} from "lucide-react";

export default function DocumentsTable({
  documents = [],
  deletingId,
  onDelete,
  onReplace,
  onHistory,
}) {
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("ALL");

  const getIcon = (type) => {
    if (type === "BANK_STATEMENT")
      return <Landmark size={18} className="text-indigo-600" />;
    if (type === "GST_RETURN")
      return <Receipt size={18} className="text-emerald-600" />;
    return <FileText size={18} className="text-purple-600" />;
  };

  const getBadge = (type) => {
    const base = "px-2 py-1 text-xs rounded-md font-semibold";

    if (type === "BANK_STATEMENT")
      return `${base} bg-indigo-50 text-indigo-700`;

    if (type === "GST_RETURN")
      return `${base} bg-emerald-50 text-emerald-700`;

    return `${base} bg-purple-50 text-purple-700`;
  };

  const filteredDocs = (documents || [])
    .filter((d) =>
      d?.type?.toLowerCase().includes(search.toLowerCase())
    )
    .filter((d) => (filter === "ALL" ? true : d.type === filter));

  return (
    <div className="p-6">

      {/* HEADER */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold text-gray-900">
          Uploaded Documents
        </h3>

        <div className="flex gap-3">
          <div className="flex items-center border border-gray-200 rounded-xl px-3 py-2 bg-white">
            <Search size={16} className="text-gray-400" />
            <input
              className="bg-transparent outline-none px-2 text-sm w-40"
              placeholder="Search type..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <select
            className="border border-gray-200 rounded-xl px-3 py-2 text-sm bg-white"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          >
            <option value="ALL">All</option>
            <option value="BANK_STATEMENT">Bank</option>
            <option value="GST_RETURN">GST</option>
            <option value="BALANCE_SHEET">Financial</option>
          </select>
        </div>
      </div>

      {/* TABLE */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="text-gray-500 border-b">
            <tr>
              <th className="text-left py-3">Document</th>
              <th className="text-center">Year</th>
              <th className="text-center">Month</th>
              <th className="text-center">Quarter</th>
              <th className="text-center">Status</th>
              <th className="text-right">Actions</th>
            </tr>
          </thead>

          <tbody>
            {filteredDocs.map((doc) => (
              <tr
                key={doc.id}
                className={`
                  border-b
                  transition-all duration-300 ease-in-out
                  ${
                    deletingId === doc.id
                      ? "opacity-0 -translate-x-6 scale-95"
                      : "opacity-100"
                  }
                `}
              >
                <td className="py-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-white rounded-lg shadow-sm">
                      {getIcon(doc.type)}
                    </div>

                    <div>
                      <div className="font-semibold text-gray-900">
                        {doc.type}
                      </div>
                      <span className={getBadge(doc.type)}>
                        {doc.source || "Unknown"}
                      </span>
                    </div>
                  </div>
                </td>

                <td className="text-center">{doc.year || "-"}</td>
                <td className="text-center">{doc.month || "-"}</td>
                <td className="text-center">{doc.quarter || "-"}</td>

                <td className="text-center">
                  <span className="px-3 py-1 text-xs rounded-full bg-emerald-50 text-emerald-700 font-semibold">
                    {doc.status || "UPLOADED"}
                  </span>
                </td>

                <td className="text-right space-x-4">
                  <button onClick={() => onReplace(doc)}>
                    <RotateCcw size={17} />
                  </button>

                  <button onClick={() => onDelete(doc)}>
                    <Trash2 size={17} />
                  </button>

                  <button onClick={() => onHistory(doc.id)}>
                    <Clock size={17} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredDocs.length === 0 && (
        <div className="text-center py-10 text-gray-400">
          No documents found
        </div>
      )}
    </div>
  );
}
