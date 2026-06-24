import { ReactNode } from "react";

export function Card({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <section className={`glass rounded-xl p-4 sm:p-5 shadow-glow ${className}`}>{children}</section>;
}

export function StatCard({ label, value, tone = "mint" }: { label: string; value: string; tone?: "mint" | "amber" | "coral" | "sky" }) {
  const color = { mint: "text-mint", amber: "text-amber", coral: "text-coral", sky: "text-sky" }[tone];
  return (
    <Card className="!p-3 sm:!p-5">
      <p className="text-xs sm:text-sm text-white/60 truncate">{label}</p>
      <p className={`mt-1 sm:mt-2 text-xl sm:text-3xl font-black ${color}`}>{value}</p>
    </Card>
  );
}
