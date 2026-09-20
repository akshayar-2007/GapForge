import { useEffect, useState } from 'react'

export default function PipelineLoader({ steps }) {
  const [activeIdx, setActiveIdx] = useState(0)

  useEffect(() => {
    if (activeIdx >= steps.length - 1) return
    const t = setTimeout(() => setActiveIdx((i) => i + 1), 1400)
    return () => clearTimeout(t)
  }, [activeIdx, steps.length])

  return (
    <div className="max-w-sm">
      <ul className="space-y-3">
        {steps.map((step, i) => {
          const state = i < activeIdx ? 'done' : i === activeIdx ? 'active' : 'pending'
          return (
            <li key={step} className="flex items-center gap-3 text-sm">
              <span className="w-4 shrink-0 flex justify-center">
                {state === 'done' && <span className="text-signal">✓</span>}
                {state === 'active' && (
                  <span className="w-2 h-2 rounded-full bg-signal animate-pulse" />
                )}
                {state === 'pending' && <span className="w-1.5 h-1.5 rounded-full bg-line" />}
              </span>
              <span className={state === 'pending' ? 'text-line' : 'text-slate'}>{step}</span>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
