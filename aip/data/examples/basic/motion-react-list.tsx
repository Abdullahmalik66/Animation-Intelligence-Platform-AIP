/**
 * Motion for React — Animated List with Exit
 * Library: Motion for React
 * Framework: React (TypeScript)
 *
 * Demonstrates:
 * - variants defined outside component
 * - AnimatePresence for exit animations
 * - useReducedMotion for accessibility
 * - Stagger children
 */

import { motion, AnimatePresence, useReducedMotion } from "motion/react";
import { useState } from "react";

// Variants outside component — stable reference, no recreation on render
const CONTAINER_VARIANTS = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
    },
  },
};

const ITEM_VARIANTS = {
  hidden: { opacity: 0, x: -16 },
  visible: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 16, transition: { duration: 0.2 } },
};

const REDUCED_ITEM_VARIANTS = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 },
  exit: { opacity: 0 },
};

interface NotificationItem {
  id: string;
  message: string;
}

interface NotificationListProps {
  initialItems?: NotificationItem[];
}

export function NotificationList({ initialItems = [] }: NotificationListProps) {
  const [items, setItems] = useState<NotificationItem[]>(initialItems);
  const prefersReducedMotion = useReducedMotion();

  const itemVariants = prefersReducedMotion ? REDUCED_ITEM_VARIANTS : ITEM_VARIANTS;

  const removeItem = (id: string) => {
    setItems((prev) => prev.filter((item) => item.id !== id));
  };

  return (
    <div role="log" aria-live="polite" aria-label="Notifications">
      <motion.ul
        variants={CONTAINER_VARIANTS}
        initial="hidden"
        animate="visible"
        style={{ listStyle: "none", padding: 0 }}
      >
        <AnimatePresence mode="sync">
          {items.map((item) => (
            <motion.li
              key={item.id} // stable key — required for AnimatePresence
              variants={itemVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              layout // animate layout changes smoothly
              style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}
            >
              <span>{item.message}</span>
              <button
                onClick={() => removeItem(item.id)}
                aria-label={`Dismiss: ${item.message}`}
              >
                ✕
              </button>
            </motion.li>
          ))}
        </AnimatePresence>
      </motion.ul>
    </div>
  );
}
