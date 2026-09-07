/**
 * Basic GSAP Stagger Example
 * Library: GSAP
 * Framework: React (TypeScript)
 *
 * Demonstrates:
 * - gsap.context() for React scoping
 * - gsap.matchMedia() for prefers-reduced-motion
 * - Named constants
 * - Stagger
 * - Cleanup
 */

import { useEffect, useRef } from "react";
import gsap from "gsap";

// Named constants — never use magic numbers
const DURATION = 0.6;
const EASE = "power2.out";
const INITIAL_Y = 30;
const STAGGER_AMOUNT = 0.5; // total seconds distributed across all elements

interface Item {
  id: string;
  label: string;
}

interface StaggeredListProps {
  items: Item[];
}

export function StaggeredList({ items }: StaggeredListProps) {
  const containerRef = useRef<HTMLUListElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      const mm = gsap.matchMedia();

      mm.add("(prefers-reduced-motion: no-preference)", () => {
        // Staggered entrance from below
        gsap.from(".stagger-item", {
          opacity: 0,
          y: INITIAL_Y,
          duration: DURATION,
          ease: EASE,
          stagger: {
            amount: STAGGER_AMOUNT,
            from: "start",
          },
        });
      });

      mm.add("(prefers-reduced-motion: reduce)", () => {
        // Ensure items are visible immediately
        gsap.set(".stagger-item", { opacity: 1, y: 0 });
      });
    }, containerRef); // scope to container — prevents targeting outside

    return () => ctx.revert(); // cleanup all animations
  }, []);

  return (
    <ul ref={containerRef} style={{ listStyle: "none", padding: 0 }}>
      {items.map((item) => (
        <li
          key={item.id}
          className="stagger-item"
          style={{ opacity: 0 }} // initial state set via CSS to prevent FOUC
        >
          {item.label}
        </li>
      ))}
    </ul>
  );
}
