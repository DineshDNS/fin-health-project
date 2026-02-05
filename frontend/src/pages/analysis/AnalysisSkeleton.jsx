export default function AnalysisSkeleton() {
  return (
    <div className="space-y-6">
      {[1, 2, 3, 4, 5, 6].map((i) => (
        <div
          key={i}
          className="h-32 rounded-xl bg-white/5 overflow-hidden"
        >
          <div className="h-full w-full shimmer" />
        </div>
      ))}
    </div>
  );
}
