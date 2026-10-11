import { useEffect, useRef, useState } from 'react'
import { Camera, ImagePlus, LoaderCircle, RotateCcw, Upload, X } from 'lucide-react'

const MAX_SIZE = 10 * 1024 * 1024
const TYPES = ['image/jpeg', 'image/png', 'image/webp']

export default function UploadBox({ onAnalyze, busy }) {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState('')
  const [error, setError] = useState('')
  const [cameraError, setCameraError] = useState('')
  const [cameraStarting, setCameraStarting] = useState(false)
  const [drag, setDrag] = useState(false)
  const [cameraOpen, setCameraOpen] = useState(false)
  const input = useRef(null)
  const video = useRef(null)
  const stream = useRef(null)

  useEffect(() => {
    if (cameraOpen && video.current && stream.current) video.current.srcObject = stream.current
  }, [cameraOpen])

  useEffect(() => () => stream.current?.getTracks().forEach(track => track.stop()), [])

  function closeCamera() {
    stream.current?.getTracks().forEach(track => track.stop())
    stream.current = null
    setCameraOpen(false)
  }

  function clear() {
    if (preview) URL.revokeObjectURL(preview)
    setFile(null)
    setPreview('')
    setError('')
    if (input.current) input.current.value = ''
  }

  function choose(next) {
    if (!next || busy) return
    setError('')
    if (!TYPES.includes(next.type)) {
      clear()
      return setError('Please choose a JPEG, PNG, or WebP image.')
    }
    if (next.size > MAX_SIZE) {
      clear()
      return setError('This image is over 10 MB. Choose a smaller file.')
    }
    if (preview) URL.revokeObjectURL(preview)
    setFile(next)
    setPreview(URL.createObjectURL(next))
  }

  async function openCamera() {
    setCameraError('')
    if (!navigator.mediaDevices?.getUserMedia) {
      setCameraError('Live camera capture is not available in this browser. Choose an image file instead.')
      return
    }
    setCameraStarting(true)
    try {
      stream.current = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: 'environment' } },
        audio: false,
      })
      setCameraOpen(true)
    } catch (err) {
      const message = err.name === 'NotAllowedError'
        ? 'Camera access was blocked. Allow camera permission in your browser settings, then try again.'
        : err.name === 'NotFoundError'
          ? 'No camera was found. Choose an image file instead.'
          : 'Could not start the camera. Check that another app is not using it, then try again.'
      setCameraError(message)
    } finally {
      setCameraStarting(false)
    }
  }

  function capturePhoto() {
    const player = video.current
    if (!player?.videoWidth || !player.videoHeight) {
      setCameraError('The camera is still starting. Wait a moment and try again.')
      return
    }
    const canvas = document.createElement('canvas')
    canvas.width = player.videoWidth
    canvas.height = player.videoHeight
    canvas.getContext('2d').drawImage(player, 0, 0, canvas.width, canvas.height)
    canvas.toBlob(blob => {
      if (!blob) return setCameraError('Could not capture the photo. Please try again.')
      const capture = new File([blob], `ecovision-${Date.now()}.jpg`, { type: 'image/jpeg' })
      closeCamera()
      choose(capture)
    }, 'image/jpeg', 0.9)
  }

  return <div
    className="upload-card"
    onDragOver={event => { event.preventDefault(); if (!busy) setDrag(true) }}
    onDragLeave={() => setDrag(false)}
    onDrop={event => { event.preventDefault(); setDrag(false); choose(event.dataTransfer.files[0]) }}
  >
    {cameraOpen ? <div className="camera-stage">
      <video ref={video} className="camera-view" autoPlay playsInline muted aria-label="Live camera preview" />
      <div className="camera-controls">
        <button type="button" className="button button-soft" onClick={closeCamera}>Cancel</button>
        <button type="button" className="button button-green" onClick={capturePhoto}><Camera size={17} /> Capture photo</button>
      </div>
    </div> : preview ? <div className="preview-wrap">
      <img className="preview-image" src={preview} alt="Selected waste item preview" />
      <button type="button" className="remove-image" onClick={clear} disabled={busy} aria-label="Remove selected image"><X size={18} /></button>
      <div className="preview-file">
        <span className="upload-icon small"><Upload size={16} /></span>
        <span><b>{file?.name}</b><small>{(file?.size / 1024 / 1024).toFixed(2)} MB · Ready to identify</small></span>
        <button className="replace-link" type="button" onClick={() => input.current?.click()} disabled={busy}>Replace</button>
      </div>
    </div> : <button
      className={`dropzone ${drag ? 'dragging' : ''}`}
      onClick={() => input.current?.click()}
      type="button"
      disabled={busy}
      aria-label="Choose a waste image"
    >
      <span className="upload-icon"><ImagePlus size={25} /></span>
      <strong>Drop a photo here, or <u>browse files</u></strong>
      <span>One item works best · JPG, PNG or WebP · up to 10 MB</span>
      <span className="camera-hint">Choose an existing photo or take one with your camera below.</span>
    </button>}

    <input
      ref={input}
      className="visually-hidden"
      type="file"
      accept="image/jpeg,image/png,image/webp"
      capture="environment"
      disabled={busy}
      onChange={event => choose(event.target.files?.[0])}
      aria-label="Select an image file"
    />
    {!cameraOpen && <button type="button" className="camera-launch" onClick={openCamera} disabled={busy || cameraStarting}>
      <Camera size={16} /> {cameraStarting ? 'Opening camera…' : preview ? 'Retake with camera' : 'Take a photo with camera'}
    </button>}
    {cameraError && <p className="inline-error" role="alert">{cameraError}</p>}
    {error && <p className="inline-error" role="alert">{error}</p>}
    <button className="button button-green analyze-button" type="button" disabled={!file || busy || cameraOpen} onClick={() => onAnalyze(file)}>
      {busy ? <><LoaderCircle className="spin" size={17} /> Looking closely…</> : <>Identify this item <span>→</span></>}
    </button>
    {busy && <p className="processing-note">Your image is being analysed securely.</p>}
    {file && !busy && <button type="button" className="reset-link" onClick={clear}><RotateCcw size={14} /> Start over</button>}
  </div>
}
