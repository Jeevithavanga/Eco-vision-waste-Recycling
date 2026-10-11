import { ArrowRight, Flame, Leaf, Recycle, Zap } from 'lucide-react'

const pathways = [
  { icon: Leaf, title: 'Food & garden scraps', text: 'Keep organics separate. Depending on local services, they may be composted or processed into biogas.' },
  { icon: Recycle, title: 'Reusable materials', text: 'Reuse and recycling usually come first, keeping materials in circulation where facilities accept them.' },
  { icon: Flame, title: 'Residual waste', text: 'Some non-recyclable waste can supply heat or electricity at permitted energy-recovery facilities.' },
]

export default function WasteToEnergy() {
  return <section className="energy-section section-pad" aria-labelledby="energy-title">
    <div className="shell">
      <div className="energy-heading">
        <span className="eyebrow"><Zap size={15} /> A smarter next step</span>
        <h2 id="energy-title">Waste can become<br /><em>something useful.</em></h2>
        <p>With the right sorting and local facilities, some waste streams can support cleaner materials, compost, biogas, heat, or electricity.</p>
      </div>
      <div className="energy-flow" aria-label="Possible pathways from sorted waste">
        <div className="energy-start"><Recycle size={25} /><span>Sort it well</span></div>
        <ArrowRight className="energy-arrow" aria-hidden="true" />
        <div className="energy-paths">
          {pathways.map(({ icon: Icon, title, text }) => <article className="energy-path" key={title}>
            <span className="energy-icon"><Icon size={22} /></span>
            <div><h3>{title}</h3><p>{text}</p></div>
          </article>)}
        </div>
        <div className="energy-output"><Zap size={25} /><span>New possibilities</span></div>
      </div>
      <p className="energy-note">Energy recovery is only suitable for certain residual waste and depends on local facilities. Always check what your council or recycling center accepts.</p>
    </div>
  </section>
}
