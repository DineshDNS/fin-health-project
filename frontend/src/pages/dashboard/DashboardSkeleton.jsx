export default function DashboardSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      {/* Hero cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="h-28 rounded-xl bg-white/40" />
        <div className="h-28 rounded-xl bg-white/40" />
        <div className="h-28 rounded-xl bg-white/40" />
      </div>

      {/* Business context */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <div className="h-20 rounded-lg bg-white/40" />
        <div className="h-20 rounded-lg bg-white/40" />
        <div className="h-20 rounded-lg bg-white/40" />
        <div className="h-20 rounded-lg bg-white/40" />
      </div>

      {/* Key insights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="h-40 rounded-xl bg-white/40" />
        <div className="h-40 rounded-xl bg-white/40" />
      </div>
    </div>
  );
}
