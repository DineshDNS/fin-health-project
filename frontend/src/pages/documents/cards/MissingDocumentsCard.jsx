import { CheckCircle, AlertTriangle } from "lucide-react";

export default function MissingDocumentsCard({ missing = [] }) {
  const allDone = missing.length === 0;

  return (
    <div className="bg-white rounded-3xl shadow-xl p-6 border-l-4 
                    transition-all duration-300 hover:shadow-2xl
                    border-orange-500">

      <h3 className="text-lg font-semibold mb-4">Missing Documents</h3>

      {allDone ? (
        <div className="flex items-center gap-3 text-green-600">
          <CheckCircle size={22} />
          <p className="font-medium">All required docs uploaded</p>
        </div>
      ) : (
        <div className="space-y-2">
          {missing.map((doc) => (
            <div key={doc} className="flex items-center gap-2 text-red-600 text-sm">
              <AlertTriangle size={16} />
              {doc}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
