export default function DocumentHealthCard({ score = 0 }) {
  return (
    <div className="relative overflow-hidden rounded-3xl p-8 text-white shadow-2xl 
                    bg-gradient-to-r from-indigo-500 via-purple-600 to-fuchsia-600
                    transition-all duration-300 hover:scale-[1.01]">

      {/* Glow background */}
      <div className="absolute -top-10 -right-10 w-40 h-40 bg-white/20 blur-3xl rounded-full"></div>

      <h2 className="text-sm uppercase tracking-widest opacity-80">
        Document Health Score
      </h2>

      <div className="mt-4 text-5xl font-bold animate-pulse">
        {score}
      </div>

      <p className="text-sm opacity-80 mt-2">
        Overall completeness of uploaded documents
      </p>
    </div>
  );
}
