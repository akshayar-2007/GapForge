import { useState } from 'react'
import StageTracker from './components/StageTracker'
import PipelineLoader from './components/PipelineLoader'
import StartScreen from './components/StartScreen'
import GapsScreen from './components/GapsScreen'
import ShortlistScreen from './components/ShortlistScreen'
import RoadmapScreen from './components/RoadmapScreen'
import { startWithResume, startManual, sendFeedback, selectIdea } from './api'

const STEP = { START: 1, GAPS: 2, SHORTLIST: 3, ROADMAP: 4 }

export default function App() {
  const [step, setStep] = useState(STEP.START)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const [sessionId, setSessionId] = useState(null)
  const [profile, setProfile] = useState(null)
  const [gaps, setGaps] = useState([])
  const [shortlist, setShortlist] = useState([])
  const [selectedIdea, setSelectedIdea] = useState(null)
  const [plan, setPlan] = useState(null)
  const [refining, setRefining] = useState(false)

  async function handleStart(fn) {
    setError(null)
    setLoading(true)
    try {
      const data = await fn()
      setSessionId(data.session_id)
      setProfile(data.user_profile)
      setGaps(data.skill_gaps)
      setShortlist(data.shortlist)
      setStep(STEP.GAPS)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleResumeSubmit = (file, company) =>
    handleStart(() => startWithResume(file, company))

  const handleManualSubmit = (payload) => handleStart(() => startManual(payload))

  async function handleRefine(feedback) {
    setRefining(true)
    setError(null)
    try {
      const data = await sendFeedback(sessionId, feedback)
      setShortlist(data.shortlist)
    } catch (e) {
      setError(e.message)
    } finally {
      setRefining(false)
    }
  }

  async function handleSelect(idx) {
    setLoading(true)
    setError(null)
    try {
      const data = await selectIdea(sessionId, idx)
      setSelectedIdea(data.selected_idea)
      setPlan(data.deep_plan)
      setStep(STEP.ROADMAP)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  function handleRestart() {
    setStep(STEP.START)
    setSessionId(null)
    setProfile(null)
    setGaps([])
    setShortlist([])
    setSelectedIdea(null)
    setPlan(null)
    setError(null)
  }

  return (
    <div className="min-h-screen flex">
      <div className="w-full max-w-5xl mx-auto flex px-6 py-12">
        <StageTracker current={step} />
        <div className="flex-1 md:pl-10">
          {loading && step === STEP.START && (
            <PipelineLoader
              steps={['Parsing profile…', 'Researching target company…', 'Analyzing skill gaps…', 'Generating project ideas…', 'Filtering and ranking…']}
            />
          )}

          {loading && step === STEP.SHORTLIST && (
            <PipelineLoader steps={['Building execution roadmap…', 'Drafting resume bullets…']} />
          )}

          {!loading && step === STEP.START && (
            <StartScreen
              onSubmitResume={handleResumeSubmit}
              onSubmitManual={handleManualSubmit}
              error={error}
            />
          )}

          {!loading && step === STEP.GAPS && (
            <GapsScreen profile={profile} gaps={gaps} onContinue={() => setStep(STEP.SHORTLIST)} />
          )}

          {!loading && step === STEP.SHORTLIST && (
            <ShortlistScreen
              shortlist={shortlist}
              onRefine={handleRefine}
              onSelect={handleSelect}
              refining={refining}
            />
          )}

          {!loading && step === STEP.ROADMAP && (
            <RoadmapScreen selectedIdea={selectedIdea} plan={plan} onRestart={handleRestart} />
          )}

          {error && step !== STEP.START && (
            <p className="mt-4 text-sm text-amber bg-amber-dim px-3 py-2 rounded max-w-lg">
              {error}
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
