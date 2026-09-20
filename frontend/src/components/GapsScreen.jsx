export default function GapsScreen({ profile, gaps, onContinue }) {
  return (
    <div className="max-w-lg">
      <h1 className="text-2xl font-medium mb-1">
        {profile?.name ? `Here's what we found, ${profile.name.split(' ')[0]}` : "Here's what we found"}
      </h1>
      <p className="text-slate text-sm mb-8">
        Your top skill gaps against this company's interview benchmark, ranked by weight.
      </p>

      <div className="mb-8">
        <div className="text-xs font-mono text-slate mb-3 tracking-wide">YOUR SKILLS</div>
        <div className="flex flex-wrap gap-1.5">
          {(profile?.technical_skills || []).map((s) => (
            <span
              key={s}
              className="font-mono text-xs bg-white border border-line rounded px-2 py-1 text-ink"
            >
              {s}
            </span>
          ))}
        </div>
      </div>

      <div className="space-y-3 mb-8">
        {gaps.map((gap) => (
          <div key={gap.area} className="border border-line rounded px-4 py-3">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium">{gap.area}</span>
              <span className="font-mono text-xs text-amber">
                {Math.round(gap.coverage * 100)}% covered
              </span>
            </div>
            <div className="w-full h-1.5 bg-line rounded-full overflow-hidden mb-2">
              <div
                className="h-full bg-amber rounded-full"
                style={{ width: `${gap.coverage * 100}%` }}
              />
            </div>
            {gap.missing_keywords?.length > 0 && (
              <div className="text-xs text-slate">
                Missing: {gap.missing_keywords.join(', ')}
              </div>
            )}
          </div>
        ))}
      </div>

      <button
        onClick={onContinue}
        className="bg-signal text-white text-sm px-5 py-2.5 rounded"
      >
        Generate project ideas
      </button>
    </div>
  )
}
