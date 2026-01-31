import { useEffect, useState } from "react";
import { getDocuments } from "../api/documentsApi";

export default function Documents() {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDocuments().then((res) => {
      setDocs(res.data);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return <p className="text-slate-700">Loading documents...</p>;
  }

  return (
    <div
      className="min-h-full p-8 rounded-3xl
      bg-gradient-to-br from-rose-100 via-pink-100 to-amber-100"
    >
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-slate-900">
          Documents
        </h2>
        <p className="text-sm text-slate-600 mt-1">
          Uploaded financial statements and reports
        </p>
      </div>

      {/* Documents List */}
      <div className="glass-card p-6">
        {docs.length === 0 ? (
          <p className="text-sm text-slate-600">
            No documents uploaded yet.
          </p>
        ) : (
          <table className="w-full text-sm">
            <thead className="text-slate-500 border-b">
              <tr>
                <th className="py-2 text-left">File Name</th>
                <th className="py-2 text-left">Type</th>
                <th className="py-2 text-left">Uploaded</th>
                <th className="py-2 text-left">Action</th>
              </tr>
            </thead>
            <tbody>
              {docs.map((doc) => (
                <tr
                  key={doc.id}
                  className="border-b last:border-none"
                >
                  <td className="py-3 font-medium text-slate-900">
                    {doc.file_name}
                  </td>
                  <td className="py-3 uppercase text-slate-600">
                    {doc.file_type}
                  </td>
                  <td className="py-3 text-slate-600">
                    {new Date(doc.uploaded_at).toLocaleDateString()}
                  </td>
                  <td className="py-3">
                    <a
                      href={doc.file_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-rose-600 hover:underline"
                    >
                      View
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
