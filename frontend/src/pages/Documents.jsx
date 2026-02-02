import { useEffect, useState } from "react";
import { getDocuments, deleteDocument } from "../api/documentsApi";

export default function Documents() {
  const [docs, setDocs] = useState([]);

  const loadDocs = async () => {
    const res = await getDocuments();
    setDocs(res.data);
  };

  useEffect(() => {
    loadDocs();
  }, []);

  const handleDelete = async (id) => {
    if (!confirm("Delete this document?")) return;
    await deleteDocument(id);
    loadDocs();
  };

  return (
    <div className="p-8 rounded-3xl bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100">
      <h2 className="text-2xl font-semibold mb-6">Documents</h2>

      <div className="glass-card p-6">
        <table className="w-full text-sm">
          <thead className="border-b text-slate-500">
            <tr>
              <th className="text-left py-2">File</th>
              <th className="text-left py-2">Category</th>
              <th className="text-left py-2">Type</th>
              <th className="text-left py-2">Uploaded</th>
              <th className="text-left py-2">Actions</th>
            </tr>
          </thead>

          <tbody>
            {docs.map((d) => (
              <tr key={d.id} className="border-b last:border-none">
                <td className="py-3 font-medium">{d.file_name}</td>

                <td className="py-3">
                  <span className="px-3 py-1 rounded-full bg-slate-200 text-slate-700 text-xs font-semibold">
                    {d.category}
                  </span>
                </td>

                <td className="py-3">
                  <span className="px-3 py-1 rounded-full bg-indigo-100 text-indigo-700 text-xs font-semibold">
                    {d.document_type}
                  </span>
                </td>

                <td className="py-3 text-slate-600">
                  {new Date(d.uploaded_at).toLocaleDateString()}
                </td>

                <td className="py-3 flex gap-4">
                  {/* ✅ SAFE DOWNLOAD */}
                  <a
                    href={d.file_url}
                    download
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="text-indigo-600 hover:underline"
                  >
                    Download
                  </a>

                  <button
                    onClick={() => handleDelete(d.id)}
                    className="text-rose-600 hover:underline"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
