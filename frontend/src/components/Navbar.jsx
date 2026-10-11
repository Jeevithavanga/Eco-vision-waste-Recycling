import { Leaf, Menu, X } from 'lucide-react'
import { useState } from 'react'
export default function Navbar() {
  const [open, setOpen] = useState(false)
  return <header className="nav-wrap"><nav className="navbar shell" aria-label="Main navigation"><a className="brand" href="#top" aria-label="EcoVision AI home"><span className="brand-mark"><Leaf size={20}/></span><span>EcoVision<span className="brand-ai">AI</span></span></a><button className="menu-toggle" onClick={() => setOpen(!open)} aria-label={open ? 'Close menu' : 'Open menu'}>{open ? <X/> : <Menu/>}</button><div className={`nav-links ${open ? 'open' : ''}`}><a href="#how" onClick={() => setOpen(false)}>How it works</a><a href="#why" onClick={() => setOpen(false)}>Why recycle</a><a href="#locator" onClick={() => setOpen(false)}>Find a centre</a><a className="nav-cta" href="#identify" onClick={() => setOpen(false)}>Identify waste <span>↗</span></a></div></nav></header>
}
