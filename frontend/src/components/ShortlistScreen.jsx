import { useState } from 'react'

export default function ShortlistScreen({ shortlist, onRefine, onSelect, refining }) {
  const [feedback, setFeedback] = useState('')

  function handleRefine(e) {
    e.preventDefault()
    if (!feedback.trim()) return
    onRefine(feedback)
    setFeedback('')
  }

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-medium mb-1">Project ideas ranked for you</h1>
      <p className="text-slate text-sm mb-8">
        Each idea targets your top gaps and has been checked against GitHub for saturation.
      </p>

      <div className="space-y-4 mb-8">
        {shortlist.map((idea, i) => (
          <div key={i} className="border border-line rounded px-5 py-4">
            <div className="flex items-start justify-between mb-2">
              <h3 className="font-medium text-sm">{idea.title}</h3>
              <span className="font-mono text-xs text-slate shrink-0 ml-3">
                {idea.timeline_weeks}wk · {idea.saturation} saturation
              </span>
            </div>
            <p className="text-sm text-slate mb-3">{idea.description}</p>
            <div className="flex flex-wrap gap-1.5 mb-3">
              {(idea.tech_stack || []).map((t) => (
                <span key={t} className="font-mono text-xs bg-signal-dim text-signal rounded px-2 py-0.5">
                  {t}
                </span>
              ))}
            </div>
            <button
              onClick={() => onSelect(i)}
              className="text-sm text-signal font-medium hover:underline"
            >
              Choose this project →
            </button>
          </div>
        ))}
      </div>

      <form onSubmit={handleRefine} className="border-t border-line pt-6">
        <label className="block text-xs font-mono text-slate mb-2 tracking-wide">
          NOT QUITE RIGHT? REFINE THE SHORTLIST
        </label>
        <div className="flex gap-2">
          <input
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="e.g. I want ideas using machine learning instead"
            className="flex-1 border border-line rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-signal"
            disabled={refining}
          />
          <button
            type="submit"
            disabled={refining || !feedback.trim()}
            className="border border-line text-sm px-4 py-2 rounded disabled:opacity-40"
          >
            {refining ? 'Refining…' : 'Refine'}
          </button>
        </div>
      </form>
    </div>
  )
}
