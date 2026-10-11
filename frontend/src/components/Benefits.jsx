import { ArrowUpRight, Recycle, Sprout, Compass } from 'lucide-react'

const benefits = [
  { icon: Recycle, title: 'Reduce wish-cycling', text: 'Learn when an item needs a special collection or belongs outside the curbside bin.' },
  { icon: Sprout, title: 'Make reuse the first stop', text: 'Get simple reuse ideas alongside disposal guidance.' },
  { icon: Compass, title: 'Find a nearby option', text: 'Search mapped recycling points around your current location.' },
]

export default function Benefits() {
  return <section className="benefits-section section-pad" id="why">
    <div className="shell benefits-layout">
      <div className="benefits-copy">
        <span className="eyebrow">Good habits, real impact</span>
        <h2>Better sorting<br />starts with <em>knowing.</em></h2>
        <p>When materials are separated correctly, more of them have a chance to be reused or processed. EcoVision gives you a helpful starting point—then local guidance fills in the details.</p>
        <a href="#identify" className="text-link">Try it with an item <ArrowUpRight size={15} /></a>
      </div>
      <div className="benefit-list">
        {benefits.map(({ icon: Icon, title, text }, index) => <article key={title}>
          <span className="benefit-icon"><Icon /></span>
          <div><h3>{title}</h3><p>{text}</p></div>
          <span className="benefit-number">0{index + 1}</span>
        </article>)}
      </div>
    </div>
  </section>
}
