import { useEffect, useState } from 'react'
import Navbar from './components/Navbar.jsx'
import Hero from './components/Hero.jsx'
import UploadBox from './components/UploadBox.jsx'
import DetectionResult from './components/DetectionResult.jsx'
import HowItWorks from './components/HowItWorks.jsx'
import Benefits from './components/Benefits.jsx'
import WasteToEnergy from './components/WasteToEnergy.jsx'
import NearbyLocator from './components/NearbyLocator.jsx'
import Footer from './components/Footer.jsx'
import { detectWaste, getHealth } from './services/api.js'

export default function App() {
  const [health, setHealth] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)
  const [resultImage, setResultImage] = useState('')

  useEffect(() => {
    getHealth().then(setHealth).catch(() => setHealth({ status: 'offline', model: { ready: false } }))
  }, [])

  async function analyze(file) {
    setBusy(true)
    setError('')
    setResult(null)
    try {
      const data = await detectWaste(file)
      setResult(data)
      setResultImage(URL.createObjectURL(file))
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  function reset() {
    if (resultImage) URL.revokeObjectURL(resultImage)
    setResult(null)
    setResultImage('')
    setError('')
  }

  const modelReady = Boolean(health?.model?.ready)
  return <>
    <Navbar />
    <main>
      <Hero modelReady={modelReady} />
      <section className="identify-section section-pad" id="identify">
        <div className="shell identify-layout">
          <div className="identify-intro">
            <span className="eyebrow"><span className="eyebrow-mark">✳</span> Your sorting companion</span>
            <h2>What are you<br />throwing <em>away?</em></h2>
            <p>Give us a photo and we’ll help you figure out what it might be and where it could go next.</p>
            <div className="privacy-line">
              <span className="privacy-icon">◎</span>
              <span><b>Private by design</b><small>Your photo is processed for this request and is not saved by the app.</small></span>
            </div>
            {health && <div className={`backend-note ${health.status === 'ok' ? '' : 'offline'}`}>
              <span className="status-dot ready" />
              {health.status === 'ok' ? (modelReady ? 'AI model connected' : 'Backend connected · model needs setup') : 'Backend is offline'}
            </div>}
          </div>
          <div className="identify-work">
            <UploadBox onAnalyze={analyze} busy={busy} />
            {error && <div role="alert" className="api-error">
              <b>We couldn’t analyse that image</b><span>{error}</span>
              <button onClick={() => setError('')}>Dismiss</button>
            </div>}
            <DetectionResult result={result} image={resultImage} onReset={reset} />
          </div>
        </div>
      </section>
      <HowItWorks />
      <Benefits />
      <WasteToEnergy />
      <NearbyLocator />
    </main>
    <Footer />
  </>
}
