'use client';

import { useRef } from 'react';
import Link from 'next/link';

export default function Home() {
  const featuresRef = useRef<HTMLDivElement>(null);
  const aboutRef = useRef<HTMLDivElement>(null);

  const scrollToSection = (ref: React.RefObject<HTMLDivElement>) => {
    ref.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-8 md:p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8">Welcome to UICare</h1>
        <p className="text-xl mb-4">Enhancing User Interfaces with Wellness in Mind</p>
        <div className="flex gap-4 mb-16">
          <button 
            onClick={() => scrollToSection(featuresRef)} 
            className="px-4 py-2 bg-foreground text-background rounded-md hover:opacity-90 transition-opacity"
          >
            Explore Features
          </button>
          <button 
            onClick={() => scrollToSection(aboutRef)} 
            className="px-4 py-2 border border-foreground rounded-md hover:bg-foreground/10 transition-colors"
          >
            Learn More
          </button>
          <Link 
            href="/documentation"
            className="px-4 py-2 border border-foreground rounded-md hover:bg-foreground/10 transition-colors"
          >
            Documentation
          </Link>
        </div>

        <div ref={featuresRef} className="mb-16 scroll-mt-20">
          <h2 className="text-3xl font-bold mb-6">Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 border border-foreground/20 rounded-lg">
              <h3 className="text-xl font-semibold mb-2">Reality Filters</h3>
              <p>Switch between different visual modes to suit your preferences and needs.</p>
            </div>
            <div className="p-6 border border-foreground/20 rounded-lg">
              <h3 className="text-xl font-semibold mb-2">Ninja Presence</h3>
              <p>A subtle indicator that provides gentle visual feedback without distractions.</p>
            </div>
            <div className="p-6 border border-foreground/20 rounded-lg">
              <h3 className="text-xl font-semibold mb-2">Trauma-Informed</h3>
              <p>Components designed with sensitivity to potential triggers for a safe experience.</p>
            </div>
          </div>
        </div>

        <div ref={aboutRef} className="mb-16 scroll-mt-20">
          <h2 className="text-3xl font-bold mb-6">About UICare</h2>
          <p className="mb-4">
            UICare is designed to embed wellness-centric components into web projects, focusing on accessibility and user comfort. 
            By incorporating features like customizable reality filters and trauma-informed interactions, 
            UICare aims to support neurodivergent users effectively.
          </p>
          <p>
            Our mission is to create interfaces that are not just functional, but supportive of mental well-being, 
            making the digital world more accessible and comfortable for everyone.
          </p>
        </div>
      </div>
    </main>
  );
}
