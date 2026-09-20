const STAGES = [
  { n: 1, label: 'Profile & target' },
  { n: 2, label: 'Skill gaps' },
  { n: 3, label: 'Project shortlist' },
  { n: 4, label: 'Execution roadmap' },
]

export default function StageTracker({ current }) {
  return (
    <div className="w-56 shrink-0 pr-8 border-r border-line hidden md:block">
      <div className="font-mono text-xs text-slate mb-6 tracking-wide">
        RESUME-GAP RECOMMENDER
      </div>
      <ol className="space-y-1">
        {STAGES.map((s) => {
          const isActive = s.n === current
          const isDone = s.n < current
          return (
            <li key={s.n} className="flex items-start gap-3 py-2.5">
              <span
                className={`font-mono text-xs mt-0.5 w-5 shrink-0 ${
                  isActive ? 'text-signal font-semibold' : isDone ? 'text-slate' : 'text-line'
                }`}
              >
                {String(s.n).padStart(2, '0')}
              </span>
              <span
                className={`text-sm ${
                  isActive ? 'text-ink font-medium' : isDone ? 'text-slate' : 'text-line'
                }`}
              >
                {s.label}
              </span>
            </li>
          )
        })}
      </ol>
    </div>
  )
}
