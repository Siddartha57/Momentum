import { motion } from "framer-motion";

export function Spinner({ message }: { message?: string }) {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4 text-white/50">
      <motion.div
        className="w-10 h-10 border-4 border-mint/20 border-t-mint rounded-full"
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
      />
      {message && <p className="text-sm font-bold tracking-widest uppercase">{message}</p>}
    </div>
  );
}

export function ButtonSpinner() {
  return (
    <motion.div
      className="w-4 h-4 border-2 border-ink/20 border-t-ink rounded-full"
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
    />
  );
}

export const MOTIVATIONAL_PHRASES = [
  "Discipline equals freedom.",
  "Execution is the only currency that matters.",
  "Great things take time. Keep building momentum.",
  "Consistency is quieter than motivation and far more durable.",
  "The harder you work for something, the greater you'll feel when you achieve it.",
  "Don't stop when you're tired. Stop when you're done."
];

export function getRandomMotivation() {
  return MOTIVATIONAL_PHRASES[Math.floor(Math.random() * MOTIVATIONAL_PHRASES.length)];
}
