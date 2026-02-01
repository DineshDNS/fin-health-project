export default function ProductRecommendations({ products }) {
  if (!products || products.length === 0) {
    return (
      <div className="glass-card p-6">
        <h3 className="font-semibold text-slate-900 mb-2">
          Product Recommendations
        </h3>
        <p className="text-sm text-slate-600">
          Suitable bank and NBFC products will be suggested once your financial profile is assessed.
        </p>
      </div>
    );
  }

  return (
    <div className="glass-card p-6">
      <h3 className="font-semibold text-slate-900 mb-4">
        Product Recommendations
      </h3>

      <div className="space-y-4">
        {products.map((item, index) => (
          <div
            key={index}
            className="p-4 rounded-xl bg-white/60 border border-slate-100"
          >
            <div className="flex justify-between items-start gap-4">
              <div>
                <p className="text-sm font-semibold text-slate-900">
                  {item.product}
                </p>
                <p className="text-xs text-slate-500 mt-1">
                  {item.provider}
                </p>
              </div>
            </div>

            <p className="mt-3 text-sm text-slate-700">
              {item.reason}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
