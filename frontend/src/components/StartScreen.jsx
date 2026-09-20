import { useState } from 'react'

const COMPANIES = ['Goldman Sachs', 'Meta', 'Jane Street', 'default']

export default function StartScreen({ onSubmitResume, onSubmitManual, error }) {
  const [mode, setMode] = useState('resume')
  const [company, setCompany] = useState('Goldman Sachs')
  const [file, setFile] = useState(null)

  const [name, setName] = useState('')
  const [skills, setSkills] = useState('')
  const [experience, setExperience] = useState('')
  const [role, setRole] = useState('')

  function handleResumeSubmit(e) {
    e.preventDefault()
    if (!file) return
    onSubmitResume(file, company)
  }

  function handleManualSubmit(e) {
    e.preventDefault()
    onSubmitManual({
      target_company: company,
      name: name || 'Candidate',
      technical_skills: skills.split(',').map((s) => s.trim()).filter(Boolean),
      soft_skills: [],
      past_projects: [],
      languages: [],
      years_experience: parseFloat(experience) || 0,
      target_roles: role ? [role] : [],
    })
  }

  return (
    <div className="max-w-lg">
      <h1 className="text-2xl font-medium mb-2">Find your next resume project</h1>
      <p className="text-slate text-sm mb-8">
        Tell us who you're targeting. We'll find the gaps in your profile and generate
        projects built to close them.
      </p>

      <div className="mb-6">
        <label className="block text-xs font-mono text-slate mb-2 tracking-wide">
          TARGET COMPANY
        </label>
        <select
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          className="w-full border border-line rounded px-3 py-2 text-sm bg-white focus:outline-none focus:ring-1 focus:ring-signal"
        >
          {COMPANIES.map((c) => (
            <option key={c} value={c}>
              {c === 'default' ? 'General SDE (no specific company)' : c}
            </option>
          ))}
        </select>
      </div>

      <div className="flex gap-1 mb-6 border-b border-line">
        <button
          onClick={() => setMode('resume')}
          className={`px-4 py-2 text-sm border-b-2 -mb-px ${
            mode === 'resume' ? 'border-signal text-ink font-medium' : 'border-transparent text-slate'
          }`}
        >
          Upload resume
        </button>
        <button
          onClick={() => setMode('manual')}
          className={`px-4 py-2 text-sm border-b-2 -mb-px ${
            mode === 'manual' ? 'border-signal text-ink font-medium' : 'border-transparent text-slate'
          }`}
        >
          No resume yet
        </button>
      </div>

      {mode === 'resume' ? (
        <form onSubmit={handleResumeSubmit} className="space-y-4">
          <label className="block border border-dashed border-line rounded px-4 py-8 text-center cursor-pointer hover:border-signal transition-colors">
            <input
              type="file"
              accept=".pdf,.docx"
              className="hidden"
              onChange={(e) => setFile(e.target.files[0])}
            />
            <span className="text-sm text-slate">
              {file ? file.name : 'Click to choose a PDF or DOCX file'}
            </span>
          </label>
          <button
            type="submit"
            disabled={!file}
            className="bg-signal text-white text-sm px-5 py-2.5 rounded disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Analyze resume
          </button>
        </form>
      ) : (
        <form onSubmit={handleManualSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-mono text-slate mb-1.5">NAME</label>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full border border-line rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-signal"
              placeholder="Your name"
            />
          </div>
          <div>
            <label className="block text-xs font-mono text-slate mb-1.5">
              TECHNICAL SKILLS (comma-separated)
            </label>
            <input
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
              className="w-full border border-line rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-signal"
              placeholder="Python, React, SQL, REST APIs"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-mono text-slate mb-1.5">YEARS EXPERIENCE</label>
              <input
                value={experience}
                onChange={(e) => setExperience(e.target.value)}
                className="w-full border border-line rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-signal"
                placeholder="0.5"
              />
            </div>
            <div>
              <label className="block text-xs font-mono text-slate mb-1.5">TARGET ROLE</label>
              <input
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full border border-line rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-signal"
                placeholder="SDE Intern"
              />
            </div>
          </div>
          <button
            type="submit"
            disabled={!skills.trim()}
            className="bg-signal text-white text-sm px-5 py-2.5 rounded disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Analyze profile
          </button>
        </form>
      )}

      {error && (
        <p className="mt-4 text-sm text-amber bg-amber-dim px-3 py-2 rounded">{error}</p>
      )}
    </div>
  )
}
