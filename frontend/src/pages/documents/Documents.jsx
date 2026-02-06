import { useEffect, useState } from "react";
import UploadDocumentCard from "./cards/UploadDocumentCard";
import DocumentsTable from "./cards/DocumentsTable";
import DocumentHealthCard from "./cards/DocumentHealthCard";
import CoverageMapCard from "./cards/CoverageMapCard";
import MissingDocumentsCard from "./cards/MissingDocumentsCard";
import ReplaceDocumentModal from "./cards/ReplaceDocumentModal";
import DeleteConfirmModal from "./cards/DeleteConfirmModal";
import HistoryModal from "./cards/HistoryModal";
import api from "../../services/apiClient";

export default function Documents() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  const [replaceDoc, setReplaceDoc] = useState(null);
  const [deleteDoc, setDeleteDoc] = useState(null);
  const [historyDocId, setHistoryDocId] = useState(null);

  // animation state
  const [deletingId, setDeletingId] = useState(null);

  // ---------------- CENTRAL REFRESH ----------------
  const fetchSummary = async () => {
    try {
      const res = await api.get("/documents/summary/");
      setSummary(res.data.data);
    } catch (err) {
      console.error("Failed to load documents summary", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  // ---------------- ACTION HANDLERS ----------------
  const handleReplace = (doc) => setReplaceDoc(doc);
  const handleDelete = (doc) => setDeleteDoc(doc);
  const handleHistory = (id) => setHistoryDocId(id);

  // DELETE FLOW — ensures animation + refresh
  const handleDeleteSuccess = async (id) => {
    setDeletingId(id);

    // short animation delay
    setTimeout(async () => {
      await fetchSummary();
      setDeletingId(null);
    }, 300);
  };

  const handleReplaceSuccess = async () => {
    await fetchSummary();
    setReplaceDoc(null);
  };

  const handleUploadSuccess = async () => {
    await fetchSummary();
  };

  // ---------------- DATA EXTRACTION ----------------
  const documents = summary?.documents || [];
  const coverage = summary?.coverage_map || {};
  const missingDocuments = summary?.missing_documents || [];
  const healthScore = summary?.health_score ?? 0;

  return (
    <div className="space-y-10">

      {/* UPLOAD */}
      <UploadDocumentCard onUploadSuccess={handleUploadSuccess} />

      {/* HERO GLASS PANEL */}
      <div className="relative p-[2px] rounded-3xl bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-400">
        <div className="bg-white/70 backdrop-blur-2xl rounded-3xl p-8 shadow-[0_25px_80px_rgba(0,0,0,0.25)]">

          <DocumentHealthCard score={healthScore} />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
            <CoverageMapCard coverage={coverage} />
            <MissingDocumentsCard missing={missingDocuments} />
          </div>

        </div>
      </div>

      {/* TABLE */}
      <div className="relative p-[2px] rounded-3xl bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-400">
        <div className="bg-white/75 backdrop-blur-2xl rounded-3xl shadow-[0_20px_60px_rgba(0,0,0,0.25)]">
          <DocumentsTable
            documents={documents}
            deletingId={deletingId}
            onDelete={handleDelete}
            onReplace={handleReplace}
            onHistory={handleHistory}
          />
        </div>
      </div>

      {/* REPLACE MODAL */}
      {replaceDoc && (
        <ReplaceDocumentModal
          doc={replaceDoc}
          onClose={() => setReplaceDoc(null)}
          onSuccess={handleReplaceSuccess}
        />
      )}

      {/* DELETE MODAL */}
      {deleteDoc && (
        <DeleteConfirmModal
          doc={deleteDoc}
          onClose={() => setDeleteDoc(null)}
          onSuccess={() => handleDeleteSuccess(deleteDoc.id)}
        />
      )}

      {/* HISTORY MODAL */}
      {historyDocId && (
        <HistoryModal
          documentId={historyDocId}
          onClose={() => setHistoryDocId(null)}
        />
      )}

      {loading && (
        <div className="text-center text-gray-400 py-10">
          Loading documents…
        </div>
      )}
    </div>
  );
}
