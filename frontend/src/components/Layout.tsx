import { AnimatePresence, motion } from "framer-motion";
import { Award, BarChart3, Bell, BookOpen, CalendarDays, Flame, Home, ListTodo, Menu, Plus, Settings, Timer, HelpCircle, X } from "lucide-react";
import { NavLink, Outlet, useBlocker, useLocation, useNavigate } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import { usePomodoro } from "../context/PomodoroContext";
import { useState } from "react";

/* Bottom nav: 2 left + FAB center + 2 right */
const bottomLeft = [
  { to: "/app", label: "Home", icon: Home },
  { to: "/app/goals", label: "Goals", icon: Flame },
];
const bottomRight = [
  { to: "/app/tasks", label: "Tasks", icon: ListTodo },
  { to: "/app/pomodoro", label: "Timer", icon: Timer },
];

/* Hamburger-only items */
const menuLinks = [
  { to: "/app/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/app/calendar", label: "Calendar", icon: CalendarDays },
  { to: "/app/journal", label: "Journal", icon: BookOpen },
  { to: "/app/achievements", label: "Badges", icon: Award },
  { to: "/app/notifications", label: "Alerts", icon: Bell },
  { to: "/app/guide", label: "Guide", icon: HelpCircle },
  { to: "/app/settings", label: "Settings", icon: Settings },
];

/* Full sidebar (desktop) */
const allLinks = [
  { to: "/app", label: "Dashboard", icon: Home },
  { to: "/app/goals", label: "Goals", icon: Flame },
  { to: "/app/tasks", label: "Tasks", icon: ListTodo },
  { to: "/app/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/app/calendar", label: "Calendar", icon: CalendarDays },
  { to: "/app/journal", label: "Journal", icon: BookOpen },
  { to: "/app/pomodoro", label: "Pomodoro", icon: Timer },
  { to: "/app/achievements", label: "Badges", icon: Award },
  { to: "/app/notifications", label: "Alerts", icon: Bell },
  { to: "/app/guide", label: "Guide", icon: HelpCircle },
  { to: "/app/settings", label: "Settings", icon: Settings },
];

function BottomNavItem({ to, label, icon: Icon }: { to: string; label: string; icon: any }) {
  return (
    <NavLink
      to={to}
      end={to === "/app"}
      className={({ isActive }) => `flex flex-col items-center justify-center gap-0.5 py-2 text-[10px] font-bold uppercase tracking-wider transition ${isActive ? "text-mint" : "text-white/45"}`}
    >
      <Icon size={20} />
      <span>{label}</span>
    </NavLink>
  );
}

export function Layout() {
  const { isRunning, pauseTimer, timeLeft, isBreak } = usePomodoro();
  const location = useLocation();
  const navigate = useNavigate();
  const [fabOpen, setFabOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  const blocker = useBlocker(({ currentLocation, nextLocation }) => {
    return isRunning && currentLocation.pathname === '/app/pomodoro' && nextLocation.pathname !== '/app/pomodoro';
  });

  const showTimer = isRunning && location.pathname !== '/app/pomodoro';

  return (
    <div className="min-h-screen bg-ink text-white">
      <Toaster position="top-right" toastOptions={{ style: { background: '#1f2937', color: '#fff' } }} />
      <div className="fixed inset-0 -z-10 bg-[radial-gradient(circle_at_15%_20%,rgba(94,243,179,.16),transparent_30%),radial-gradient(circle_at_85%_10%,rgba(125,211,252,.14),transparent_28%),linear-gradient(135deg,#070a12,#111827_52%,#07120f)]" />

      {/* ─── Mobile Top Bar ─── */}
      <header className="fixed top-0 left-0 right-0 z-30 flex items-center justify-between px-4 py-3 bg-black/40 backdrop-blur-xl border-b border-white/10 lg:hidden">
        <div className="flex items-center gap-2">
          <div className="grid h-8 w-8 place-items-center rounded-lg bg-mint text-ink font-black text-sm">M</div>
          <p className="font-bold text-sm">Momentum</p>
        </div>
        <button onClick={() => setMenuOpen(true)} className="grid h-9 w-9 place-items-center rounded-lg bg-white/10 hover:bg-white/20 transition-colors">
          <Menu size={20} />
        </button>
      </header>

      {/* ─── Desktop Sidebar ─── */}
      <aside className="fixed left-0 top-0 hidden h-screen w-64 border-r border-white/10 bg-black/25 p-4 backdrop-blur-xl lg:block overflow-y-auto">
        <div className="mb-8 flex items-center gap-3 px-2">
          <div className="grid h-10 w-10 place-items-center rounded-lg bg-mint text-ink font-black">M</div>
          <div>
            <p className="text-lg font-bold">Momentum</p>
            <p className="text-xs text-white/55">Accountability OS</p>
          </div>
        </div>
        <nav className="space-y-1">
          {allLinks.map(({ to, label, icon: Icon }) => (
            <NavLink key={to} to={to} end={to === "/app"} className={({ isActive }) => `focus-ring flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition ${isActive ? "bg-white/14 text-mint" : "text-white/68 hover:bg-white/8 hover:text-white"}`}>
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* ─── Hamburger Slide Menu (mobile) ─── */}
      <AnimatePresence>
        {menuOpen && (
          <>
            <motion.div
              key="menu-overlay"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="fixed inset-0 z-[60] bg-black/60 backdrop-blur-sm lg:hidden"
              onClick={() => setMenuOpen(false)}
            />
            <motion.div
              key="menu-panel"
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", damping: 28, stiffness: 300 }}
              className="fixed top-0 right-0 bottom-0 z-[70] w-72 bg-ink/95 backdrop-blur-xl border-l border-white/10 p-5 lg:hidden"
            >
              <div className="flex items-center justify-between mb-8">
                <p className="text-lg font-bold text-mint">More</p>
                <button onClick={() => setMenuOpen(false)} className="grid h-9 w-9 place-items-center rounded-lg bg-white/10 hover:bg-white/20 transition-colors">
                  <X size={20} />
                </button>
              </div>
              <nav className="space-y-1">
                {menuLinks.map(({ to, label, icon: Icon }) => (
                  <NavLink
                    key={to}
                    to={to}
                    end={to === "/app"}
                    onClick={() => setMenuOpen(false)}
                    className={({ isActive }) => `flex items-center gap-3 rounded-lg px-3 py-3 text-sm font-medium transition ${isActive ? "bg-white/14 text-mint" : "text-white/70 hover:bg-white/8 hover:text-white"}`}
                  >
                    <Icon size={18} />
                    {label}
                  </NavLink>
                ))}
              </nav>
              <div className="absolute bottom-6 left-5 right-5 p-4 bg-white/5 rounded-lg border border-white/10 text-center">
                <p className="text-xs text-white/40 italic">"Execution is the only currency that matters."</p>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* ─── Main Content ─── */}
      <main className="pt-16 pb-24 px-3 sm:px-4 lg:pt-5 lg:pb-8 lg:ml-64 lg:px-8">
        <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }}>
          <Outlet />
        </motion.div>
      </main>

      {/* ─── Mobile Bottom Nav with Center FAB ─── */}
      <nav className="fixed bottom-0 left-0 right-0 z-30 lg:hidden">
        <div className="relative flex items-end justify-around bg-black/70 backdrop-blur-xl border-t border-white/10 px-2">
          {/* Left 2 items */}
          {bottomLeft.map(link => <BottomNavItem key={link.to} {...link} />)}

          {/* Center FAB spacer */}
          <div className="w-16 shrink-0" />

          {/* Right 2 items */}
          {bottomRight.map(link => <BottomNavItem key={link.to} {...link} />)}
        </div>

        </nav>

      

      {/* ─── Mobile FAB (outside nav for z-index fix) ─── */}
      <div className="fixed left-1/2 -translate-x-1/2 bottom-8 z-50 flex flex-col items-center gap-2 lg:hidden">
        <AnimatePresence>
          {fabOpen && (
            <div className="absolute bottom-full mb-4 flex flex-col items-center gap-3 w-40">
              <motion.button
                key="m-fab-goal"
                initial={{ opacity: 0, y: 16, scale: 0.8 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 16, scale: 0.8 }}
                transition={{ duration: 0.15, delay: 0.05 }}
                onClick={() => { setFabOpen(false); navigate('/app/goals'); }}
                className="flex items-center gap-2 bg-ink border border-white/20 text-white px-4 py-3 rounded-full font-bold shadow-2xl text-sm whitespace-nowrap w-full justify-center pointer-events-auto"
              >
                <Flame size={16} className="text-mint" /> New Goal
              </motion.button>
              <motion.button
                key="m-fab-task"
                initial={{ opacity: 0, y: 16, scale: 0.8 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 16, scale: 0.8 }}
                transition={{ duration: 0.15 }}
                onClick={() => { setFabOpen(false); navigate('/app/tasks'); }}
                className="flex items-center gap-2 bg-ink border border-white/20 text-white px-4 py-3 rounded-full font-bold shadow-2xl text-sm whitespace-nowrap w-full justify-center pointer-events-auto"
              >
                <ListTodo size={16} className="text-sky-400" /> New Task
              </motion.button>
            </div>
          )}
        </AnimatePresence>

        <motion.button
          onClick={() => setFabOpen(!fabOpen)}
          whileTap={{ scale: 0.9 }}
          className="h-14 w-14 rounded-full bg-mint text-ink shadow-xl shadow-mint/30 grid place-items-center relative z-50 pointer-events-auto"
        >
          <motion.div animate={{ rotate: fabOpen ? 45 : 0 }} transition={{ duration: 0.2 }}>
            {fabOpen ? <X size={24} strokeWidth={3} /> : <Plus size={24} strokeWidth={3} />}
          </motion.div>
        </motion.button>
      </div>

      {/* ─── Desktop FAB (bottom-right) ─── */}
      <div className="hidden lg:flex fixed bottom-6 right-6 z-50 flex-col items-end gap-3">
        <AnimatePresence>
          {fabOpen && (
            <>
              <motion.button
                key="d-fab-goal"
                initial={{ opacity: 0, y: 20, scale: 0.8 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 20, scale: 0.8 }}
                transition={{ duration: 0.15, delay: 0.05 }}
                onClick={() => { setFabOpen(false); navigate('/app/goals'); }}
                className="flex items-center gap-2 bg-ink/90 backdrop-blur-md border border-white/20 text-white px-4 py-2.5 rounded-full font-bold shadow-lg hover:bg-white/20 transition-colors"
              >
                <Flame size={16} className="text-mint" /> New Goal
              </motion.button>
              <motion.button
                key="d-fab-task"
                initial={{ opacity: 0, y: 20, scale: 0.8 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 20, scale: 0.8 }}
                transition={{ duration: 0.15 }}
                onClick={() => { setFabOpen(false); navigate('/app/tasks'); }}
                className="flex items-center gap-2 bg-ink/90 backdrop-blur-md border border-white/20 text-white px-4 py-2.5 rounded-full font-bold shadow-lg hover:bg-white/20 transition-colors"
              >
                <ListTodo size={16} className="text-sky-400" /> New Task
              </motion.button>
            </>
          )}
        </AnimatePresence>

        <motion.button
          onClick={() => setFabOpen(!fabOpen)}
          whileTap={{ scale: 0.9 }}
          className="h-14 w-14 rounded-full bg-mint text-ink shadow-xl shadow-mint/25 grid place-items-center hover:bg-mint/90 transition-colors"
        >
          <motion.div animate={{ rotate: fabOpen ? 45 : 0 }} transition={{ duration: 0.2 }}>
            {fabOpen ? <X size={24} strokeWidth={3} /> : <Plus size={24} strokeWidth={3} />}
          </motion.div>
        </motion.button>
      </div>

      {/* ─── Pomodoro Blocker Modal ─── */}
      {blocker.state === "blocked" && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="bg-ink border border-white/10 p-6 rounded-xl shadow-2xl max-w-sm w-full">
            <h3 className="text-xl font-bold mb-4 text-mint">Timer is active</h3>
            <p className="text-white/70 mb-6 text-sm leading-relaxed">You are leaving the Pomodoro session. Would you like to keep the timer running in the background, or stop it entirely?</p>
            <div className="flex flex-col sm:flex-row gap-3">
              <button onClick={() => blocker.proceed && blocker.proceed()} className="flex-1 bg-mint text-ink font-bold py-2 rounded text-sm hover:bg-mint/80 transition-colors">Background</button>
              <button onClick={() => { pauseTimer(); blocker.proceed && blocker.proceed(); }} className="flex-1 border border-white/10 hover:border-white/20 py-2 rounded text-sm transition-colors">Stop Timer</button>
              <button onClick={() => blocker.reset && blocker.reset()} className="flex-1 border border-white/10 py-2 rounded text-sm opacity-50 hover:opacity-100 transition-colors">Cancel</button>
            </div>
          </div>
        </div>
      )}

      {/* ─── Floating Timer Pill ─── */}
      {showTimer && (
        <motion.div 
          initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
          onClick={() => navigate('/app/pomodoro')}
          className="fixed bottom-20 lg:bottom-24 left-4 lg:left-auto lg:right-6 bg-mint text-ink px-4 py-2.5 rounded-full font-bold shadow-lg shadow-mint/20 flex items-center gap-2 cursor-pointer hover:scale-105 transition-transform z-40 text-sm"
        >
          <Timer size={16} />
          {Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, '0')} {isBreak ? '☕' : ''}
        </motion.div>
      )}

      {/* FAB backdrop overlay */}
      {fabOpen && (
        <div className="fixed inset-0 z-40" onClick={() => setFabOpen(false)} />
      )}
    </div>
  );
}
