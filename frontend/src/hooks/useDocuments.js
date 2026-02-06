import { useEffect, useState } from "react";
import api from "../services/apiClient";

export const useDocuments = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchDocuments = async () => {
    try {
      setLoading(true);

      const res = await api.get("/documents/summary/");

      setData(res.data.data);
      setError("");
    } catch (err) {
      console.error("Documents API Error:", err);
      setError("Error loading documents");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  return { data, loading, error, refresh: fetchDocuments };
};
