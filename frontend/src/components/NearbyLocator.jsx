import { useState } from 'react'
import { ArrowUpRight, LocateFixed, MapPin } from 'lucide-react'
import { findNearby } from '../services/api.js'

const SAMPLE_AREAS = [
  { name: 'Bengaluru, India', lat: 12.9716, lon: 77.5946 },
  { name: 'Mumbai, India', lat: 19.076, lon: 72.8777 },
  { name: 'Delhi, India', lat: 28.6139, lon: 77.209 },
  { name: 'London, UK', lat: 51.5072, lon: -0.1276 },
  { name: 'Singapore', lat: 1.3521, lon: 103.8198 },
]

function MapIllustration() {
  return <div className="map-preview"><div className="map-pattern">
    <span className="map-road road-one" /><span className="map-road road-two" /><span className="map-road road-three" />
    <span className="map-green green-one" /><span className="map-green green-two" />
    <span className="map-pin"><MapPin size={22} fill="currentColor" /></span>
    <span className="map-label">Location search preview</span>
    <div className="map-credit">© OpenStreetMap contributors</div>
  </div></div>
}

function PlaceCard({ place }) {
  const mapUrl = `https://www.openstreetmap.org/?mlat=${place.lat}&mlon=${place.lon}#map=17/${place.lat}/${place.lon}`
  const distance = place.distance_m >= 1000 ? `${(place.distance_m / 1000).toFixed(1)} km` : `${place.distance_m} m`
  return <a className="place-item" href={mapUrl} target="_blank" rel="noreferrer">
    <span className="place-pin"><MapPin size={17} /></span>
    <span><b>{place.name}</b><small>{place.address || place.type} · {distance}</small></span>
    <ArrowUpRight size={15} />
  </a>
}

export default function NearbyLocator() {
  const [places, setPlaces] = useState(null)
  const [locating, setLocating] = useState(false)
  const [error, setError] = useState('')
  const [location, setLocation] = useState(null)
  const [searchArea, setSearchArea] = useState('')

  async function searchAt(lat, lon, label) {
    setError('')
    setPlaces(null)
    setLocation({ lat, lon })
    setSearchArea(label)
    setLocating(true)
    try {
      setPlaces(await findNearby(lat, lon))
    } catch (err) {
      setError(err.message)
    } finally {
      setLocating(false)
    }
  }

  function locate() {
    setError('')
    setPlaces(null)
    if (!navigator.geolocation) return setError('Location is not available in this browser.')
    setLocating(true)
    navigator.geolocation.getCurrentPosition(({ coords }) => {
      searchAt(coords.latitude, coords.longitude, 'your location')
    }, (err) => {
      setLocating(false)
      setError(err.code === 1 ? 'Allow location access in your browser, then try again.' : 'Could not get your location. Check device location and try again.')
    }, { enableHighAccuracy: false, timeout: 12000, maximumAge: 300000 })
  }

  function searchRandomArea() {
    const area = SAMPLE_AREAS[Math.floor(Math.random() * SAMPLE_AREAS.length)]
    searchAt(area.lat, area.lon, area.name)
  }

  const first = places?.centers?.[0]
  const overviewUrl = first ? `https://www.openstreetmap.org/?mlat=${first.lat}&mlon=${first.lon}#map=14/${first.lat}/${first.lon}` : '#'
  const manualMapUrl = location ? `https://www.openstreetmap.org/?mlat=${location.lat}&mlon=${location.lon}#map=14/${location.lat}/${location.lon}` : 'https://www.openstreetmap.org/search?query=recycling'
  return <section className="locator-section section-pad" id="locator">
    <div className="shell locator-card">
      <div className="locator-copy">
        <span className="eyebrow">Around your area</span>
        <h2>Find a place to <em>drop it off.</em></h2>
        <p>Search mapped recycling points near you, or try a randomly selected urban area for a demo. Results come from OpenStreetMap and may be incomplete.</p>
        <div className="locator-actions">
        <button className="button button-dark" onClick={locate} disabled={locating}>
          {locating ? <><span className="spin">◌</span> Finding nearby…</> : <><LocateFixed size={17} /> Use my location</>}
        </button>
        <button className="button button-soft" onClick={searchRandomArea} disabled={locating}>
          Pick a random city
        </button>
        </div>
        {error && <p role="alert" className="inline-error">{error} <a href={manualMapUrl} target="_blank" rel="noreferrer">Open OpenStreetMap</a></p>}
        {places && !places.count && <p className="places-empty">No mapped recycling points found. <a href={manualMapUrl} target="_blank" rel="noreferrer">Explore this area in OpenStreetMap</a>.</p>}
      </div>
      <MapIllustration />
      {places?.count > 0 && <div className="places-results">
        <div className="places-heading">
          <div><h3>{places.count} nearby point{places.count === 1 ? '' : 's'}</h3><small className="places-area">Search area: {searchArea}</small></div>
          <a href={overviewUrl} target="_blank" rel="noreferrer">Open map <ArrowUpRight size={14} /></a>
        </div>
        <div className="places-grid">{places.centers.map((place, index) => <PlaceCard key={`${place.lat}-${place.lon}-${index}`} place={place} />)}</div>
        <small className="osm-credit">Map data © OpenStreetMap contributors · Confirm accepted materials with the facility.</small>
      </div>}
    </div>
  </section>
}
