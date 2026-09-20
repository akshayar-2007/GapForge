export default function RoadmapScreen({ selectedIdea, plan, onRestart }) {
  if (plan?.error) {
    return (
      <div className="max-w-lg">
        <p className="text-sm text-amber bg-amber-dim px-4 py-3 rounded mb-4">
          The roadmap generator hit an error. Try selecting the idea again.
        </p>
        <button onClick={onRestart} className="text-sm text-signal hover:underline">
          ← Start over
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-2xl pb-16">
      <h1 className="text-2xl font-medium mb-1">{selectedIdea?.title}</h1>
      <p className="text-slate text-sm mb-10">{plan?.architecture_overview}</p>

      <Section title="EXECUTION ROADMAP">
        <div className="space-y-4">
          {(plan?.roadmap || []).map((w) => (
            <div key={w.week} className="flex gap-4">
              <span className="font-mono text-xs text-slate w-14 shrink-0 pt-0.5">
                WEEK {w.week}
              </span>
              <div>
                <div className="text-sm font-medium mb-1">{w.title}</div>
                <ul className="text-sm text-slate space-y-0.5 mb-1.5">
                  {(w.tasks || []).map((t, i) => (
                    <li key={i}>· {t}</li>
                  ))}
                </ul>
                <div className="text-xs text-signal">{w.deliverable}</div>
              </div>
            </div>
          ))}
        </div>
      </Section>

      <Section title="TECH STACK JUSTIFICATION">
        <div className="space-y-3">
          {(plan?.tech_stack_justification || []).map((t, i) => (
            <div key={i}>
              <span className="font-mono text-xs bg-signal-dim text-signal rounded px-2 py-0.5 mr-2">
                {t.technology}
              </span>
              <span className="text-sm text-slate">{t.why}</span>
            </div>
          ))}
        </div>
      </Section>

      <Section title="RESUME BULLETS">
        <ul className="space-y-2">
          {(plan?.resume_bullets || []).map((b, i) => (
            <li key={i} className="text-sm bg-white border border-line rounded px-3 py-2">
              {b}
            </li>
          ))}
        </ul>
      </Section>

      <Section title="INTERVIEW TALKING POINTS">
        <ul className="text-sm text-slate space-y-1.5">
          {(plan?.interview_talking_points || []).map((p, i) => (
            <li key={i}>· {p}</li>
          ))}
        </ul>
      </Section>

      {plan?.potential_challenges?.length > 0 && (
        <Section title="POTENTIAL CHALLENGES">
          <div className="space-y-2">
            {plan.potential_challenges.map((c, i) => (
              <div key={i} className="text-sm">
                <span className="text-ink">{c.challenge}</span>
                <span className="text-slate"> — {c.mitigation}</span>
              </div>
            ))}
          </div>
        </Section>
      )}

      <button onClick={onRestart} className="text-sm text-signal hover:underline mt-8">
        ← Start a new analysis
      </button>
    </div>
  )
}

function Section({ title, children }) {
  return (
    <div className="mb-10">
      <div className="text-xs font-mono text-slate mb-3 tracking-wide">{title}</div>
      {children}
    </div>
  )
}
