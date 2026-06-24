import { motion } from "framer-motion";
import { Activity, ArrowRight, Bell, BookOpen, Check, ChevronRight, Clock, Edit3, Flame, HelpCircle, ListTodo, LogOut, Play, Plus, RotateCcw, Settings as SettingsIcon, Shield, ShieldCheck, Sparkles, Target, Trash2, Trophy, Upload, X, Zap } from "lucide-react";
import { toast } from "react-hot-toast";
import { usePomodoro } from "../context/PomodoroContext";

import { FormEvent, ReactNode, useMemo, useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Area, AreaChart, Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Card, StatCard } from "../components/Card";
import { api, setToken } from "../lib/api";
import { useFetch } from "../lib/hooks";
import { Spinner, ButtonSpinner, getRandomMotivation } from "../components/ui";

const chartData = [
  { day: "Mon", hours: 2.5, tasks: 4 },
  { day: "Tue", hours: 1.5, tasks: 2 },
  { day: "Wed", hours: 3.2, tasks: 5 },
  { day: "Thu", hours: 2.1, tasks: 3 },
  { day: "Fri", hours: 4.0, tasks: 6 },
  { day: "Sat", hours: 2.8, tasks: 4 },
  { day: "Sun", hours: 1.2, tasks: 1 }
];

const badges = ["First Goal", "7 Day Streak", "30 Day Streak", "100 Hours Logged", "Goal Completed", "Consistency Champion"];

export function Landing() {
  const navigate = useNavigate();

  return (
    <main className="min-h-screen bg-ink text-white selection:bg-mint/30 selection:text-white">
      {/* Dynamic Background */}
      <div className="fixed inset-0 z-0 bg-[radial-gradient(circle_at_20%_20%,rgba(94,243,179,.15),transparent_35%),radial-gradient(circle_at_80%_30%,rgba(125,211,252,.12),transparent_35%),linear-gradient(135deg,#070a12,#111827_55%,#07120f)]" />

      {/* Floating Header */}
      <header className="fixed top-0 left-0 right-0 z-50 px-3 sm:px-6 py-4">
        <motion.div 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className="mx-auto max-w-7xl flex items-center justify-between glass px-4 sm:px-6 py-3 rounded-2xl border border-white/10 shadow-2xl backdrop-blur-xl"
        >
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="grid h-8 w-8 sm:h-10 sm:w-10 place-items-center rounded-xl bg-mint text-ink font-black text-base sm:text-lg shadow-[0_0_15px_rgba(94,243,179,0.5)] shrink-0">M</div>
            <span className="text-lg sm:text-xl font-bold tracking-tight hidden sm:block">Momentum</span>
          </div>
          <div className="flex items-center gap-3 sm:gap-4">
            <Link to="/login" onClick={() => localStorage.setItem('auth_mode', 'login')} className="text-sm font-bold text-white/70 hover:text-white transition-colors">Login</Link>
            <Link to="/login" onClick={() => localStorage.setItem('auth_mode', 'register')} className="text-sm font-bold bg-white text-ink px-4 sm:px-5 py-2 rounded-lg hover:bg-white/90 transition-all hover:scale-105 active:scale-95 shadow-[0_0_20px_rgba(255,255,255,0.2)]">Register</Link>
          </div>
        </motion.div>
      </header>

      <div className="relative z-10 pt-32 pb-20">
        {/* Hero Section */}
        <section className="mx-auto max-w-5xl px-6 pt-20 text-center">
          <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.6, ease: "easeOut" }}>
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-mint/30 bg-mint/10 px-5 py-2 text-sm font-bold text-mint shadow-[0_0_20px_rgba(94,243,179,0.15)]">
              <Flame size={16} /> Welcome to the Elite Accountability OS
            </div>
            <h1 className="text-6xl font-black leading-[1.1] tracking-tight md:text-8xl">
              Forge Unstoppable <br/><span className="text-transparent bg-clip-text bg-gradient-to-r from-mint via-emerald-400 to-sky-400">Momentum.</span>
            </h1>
            <p className="mx-auto mt-8 max-w-2xl text-lg leading-relaxed text-white/60 md:text-xl">
              The premium environment for high achievers. Track roadmaps, protect streaks, execute deep work with Pomodoro, and journal your path to greatness.
            </p>
            <div className="mt-12 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link to="/login" onClick={() => localStorage.setItem('auth_mode', 'register')} className="flex items-center gap-2 rounded-xl bg-mint px-8 py-4 text-lg font-black text-ink shadow-[0_0_30px_rgba(94,243,179,0.3)] transition-all hover:scale-105 hover:shadow-[0_0_40px_rgba(94,243,179,0.5)] active:scale-95 w-full sm:w-auto justify-center">
                <Play fill="currentColor" size={20} /> Get Started Now
              </Link>
              <a href="#features" className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 backdrop-blur-md px-8 py-4 text-lg font-bold text-white transition-all hover:bg-white/10 hover:border-white/20 active:scale-95 w-full sm:w-auto justify-center">
                Explore Features <ArrowRight size={20} />
              </a>
            </div>
          </motion.div>
        </section>

        {/* Features Grid */}
        <section id="features" className="mx-auto max-w-7xl px-6 mt-40">
          <motion.div 
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-5xl font-black">Built for Execution.</h2>
            <p className="mt-4 text-white/50 text-lg">Everything you need to turn ambition into reality.</p>
          </motion.div>
          
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {[
              { icon: Target, title: "Roadmap tracking", desc: "Break massive goals into daily actionable steps. Never lose sight of the target." },
              { icon: Zap, title: "Streak Engine", desc: "Build unshakeable consistency. Use strategic Grace Days to protect your progress." },
              { icon: Clock, title: "Deep Work Pomodoro", desc: "Enter flow state instantly. Track work intervals and mandatory breaks perfectly." },
              { icon: Activity, title: "Advanced Analytics", desc: "Visualize your discipline. Real-time charts, accountability scores, and progress heatmaps." },
              { icon: BookOpen, title: "Daily Journaling", desc: "Reflect on learnings, document challenges, and architect tomorrow's victory today." },
              { icon: ShieldCheck, title: "Gamified Badges", desc: "Earn exclusive achievements for consistency and milestones. Make discipline addictive." },
            ].map((f, i) => (
              <motion.div 
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                className="glass p-8 rounded-2xl hover:border-mint/30 transition-colors group"
              >
                <div className="h-12 w-12 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center mb-6 group-hover:bg-mint/10 group-hover:text-mint group-hover:border-mint/30 transition-all">
                  <f.icon size={24} />
                </div>
                <h3 className="text-xl font-bold mb-3">{f.title}</h3>
                <p className="text-white/50 leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Call to Action Bottom */}
        <section className="mx-auto max-w-4xl px-6 mt-40 mb-20">
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-mint/20 to-sky-500/20 p-1 border border-white/10"
          >
            <div className="bg-ink/90 backdrop-blur-2xl rounded-[23px] px-8 py-16 md:py-24 text-center border border-white/5">
              <h2 className="text-4xl md:text-6xl font-black mb-6">Ready to execute?</h2>
              <p className="text-xl text-white/60 mb-10 max-w-2xl mx-auto">Join the elite individuals who are taking absolute control of their time and goals.</p>
              <Link to="/login" onClick={() => localStorage.setItem('auth_mode', 'register')} className="inline-flex items-center gap-2 rounded-xl bg-white px-10 py-5 text-xl font-black text-ink shadow-[0_0_30px_rgba(255,255,255,0.2)] transition-all hover:scale-105 hover:bg-mint hover:shadow-[0_0_40px_rgba(94,243,179,0.4)] active:scale-95">
                Start Your Journey <ChevronRight size={24} />
              </Link>
            </div>
          </motion.div>
        </section>
      </div>

      {/* Footer */}
      <footer className="border-t border-white/10 bg-black/40 backdrop-blur-lg py-10 relative z-10">
        <div className="mx-auto max-w-7xl px-6 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2 opacity-50">
            <div className="grid h-6 w-6 place-items-center rounded bg-white text-ink font-black text-[10px]">M</div>
            <span className="font-bold tracking-tight">Momentum</span>
          </div>
          <p className="text-white/30 text-sm">© {new Date().getFullYear()} Momentum Accountability OS. Built for greatness.</p>
        </div>
      </footer>
    </main>
  );
}

export function Login() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<"login" | "register" | "forgot">("register");

  useEffect(() => {
    const savedMode = localStorage.getItem('auth_mode');
    if (savedMode === 'register' || savedMode === 'login') {
      setMode(savedMode as any);
      localStorage.removeItem('auth_mode');
    }
  }, []);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.currentTarget));
    try {
      if (mode === "forgot") {
        const res = await api<{ message: string }>("/api/auth/forgot-password", {
          auth: false, method: "POST", body: JSON.stringify({ email: data.email })
        });
        setSuccess(res.message);
        setError("");
        return;
      }
      const payload = mode === "register"
        ? { ...data, daily_target_hours: Number(data.daily_target_hours || 1) }
        : { email: data.email, password: data.password, remember_me: true };
      
      const token = await api<{ access_token: string }>(mode === "register" ? "/api/auth/register" : "/api/auth/login", {
        auth: false,
        method: "POST",
        body: JSON.stringify(payload)
      });
      setToken(token.access_token);
      navigate("/app");
    } catch (err: any) {
      try {
        const parsed = JSON.parse(err.message);
        setError(parsed.detail || "Authentication failed.");
      } catch {
        setError(err.message || "Authentication failed. Check the backend is running.");
      }
    }
  }
  return (
    <main className="grid min-h-screen place-items-center bg-ink px-4 text-white relative">
      <div className="absolute top-6 left-6">
        <Link to="/" className="flex items-center gap-2 text-white/50 hover:text-white transition-colors font-bold text-sm">
          <ArrowRight size={16} className="rotate-180" /> Back to Home
        </Link>
      </div>
      <form onSubmit={submit} className="glass w-full max-w-md rounded-lg p-6">
        <h1 className="text-3xl font-black">{mode === "register" ? "Create Momentum" : mode === "login" ? "Welcome back" : "Reset Password"}</h1>
        <div className="mt-5 space-y-3">
          {mode === "register" && <input name="full_name" required placeholder="Full name" className="focus-ring w-full rounded-lg border border-white/12 bg-white/8 px-4 py-3" />}
          <input name="email" required type="email" placeholder="Email" className="focus-ring w-full rounded-lg border border-white/12 bg-white/8 px-4 py-3" />
          {mode !== "forgot" && <input name="password" required type="password" minLength={8} placeholder="Password" className="focus-ring w-full rounded-lg border border-white/12 bg-white/8 px-4 py-3" />}
          {mode === "register" && <input name="daily_target_hours" defaultValue="2" type="number" step="0.25" className="focus-ring w-full rounded-lg border border-white/12 bg-white/8 px-4 py-3" />}
        </div>
        {error && <p className="mt-3 text-sm text-coral">{error}</p>}
        {success && <p className="mt-3 text-sm text-mint">{success}</p>}
        <button className="focus-ring mt-5 w-full rounded-lg bg-mint px-4 py-3 font-bold text-ink">{mode === "register" ? "Register" : mode === "login" ? "Login" : "Send Reset Link"}</button>
        <div className="mt-3 grid grid-cols-2 gap-2">
          <button type="button" onClick={() => setMode(mode === "register" ? "login" : "register")} className="focus-ring w-full rounded-lg border border-white/12 px-4 py-3 text-sm text-white/80">
            {mode === "register" ? "Use existing account" : "Create new account"}
          </button>
          {mode !== "forgot" && (
            <button type="button" onClick={() => setMode("forgot")} className="focus-ring w-full rounded-lg border border-white/12 px-4 py-3 text-sm text-white/80">
              Forgot password?
            </button>
          )}
          {mode === "forgot" && (
             <button type="button" onClick={() => setMode("login")} className="focus-ring w-full rounded-lg border border-white/12 px-4 py-3 text-sm text-white/80">
             Back to Login
           </button>
          )}
        </div>
      </form>
    </main>
  );
}

export function Dashboard() {
  const { data: analytics, loading: analyticsLoading } = useFetch<any>("/api/analytics");
  const { data: tasks, refetch: refetchTasks, loading: tasksLoading } = useFetch<any[]>(`/api/tasks?day=${new Date().toISOString().split("T")[0]}`);
  const { data: goals, loading: goalsLoading } = useFetch<any[]>("/api/goals");
  const { data: quote } = useFetch<{ quote: string }>("/api/quotes/random");

  const [completingTask, setCompletingTask] = useState<number | null>(null);
  const [attachment, setAttachment] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);

  async function completeTaskFlow(e: FormEvent) {
    e.preventDefault();
    if (!completingTask) return;
    try {
      await api(`/api/tasks/${completingTask}/complete`, { 
        method: "PATCH",
        body: JSON.stringify({ attachment_data: attachment })
      });
      refetchTasks();
      setCompletingTask(null);
      setAttachment(null);
      setFileName(null);
      toast.success("Task completed! Momentum +1");
    } catch (e) { toast.error("Failed to complete task"); }
  }

  function handleFile(e: any) {
    const file = e.target.files[0];
    if (!file) return;
    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (event) => setAttachment(event.target?.result as string);
    reader.readAsDataURL(file);
  }

  if (analyticsLoading || tasksLoading || goalsLoading) return <Spinner message="Loading Dashboard..." />;

  const chartData = analytics?.daily_study_hours?.slice(-30).map((d: any) => ({
    day: new Date(d.date).toLocaleDateString('en-US', { weekday: 'short' }),
    hours: d.hours
  })) || [];

  const activeTasks = tasks?.filter(t => t.status !== 'completed')?.length || 0;

  return (
    <div className="space-y-4 sm:space-y-6 relative">
      <Header title="Today" action={quote?.quote || "Discipline equals freedom."} />

      {/* Stat cards: 2x2 grid on mobile, 4 cols on xl */}
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-3 sm:gap-4">
        <StatCard label="Current streak 🔥" value={`${analytics?.streak?.current || 0} days`} />
        <StatCard label="Best streak" value={`${analytics?.streak?.longest || 0} days`} tone="amber" />
        <StatCard label="Accountability" value={analytics?.accountability?.score || 0} tone="sky" />
        <StatCard label="Grace days" value={`${analytics?.grace_days_remaining || 0} left`} tone="coral" />
      </div>
      
      {/* Summary mini-cards: 3-col grid on mobile */}
      <div className="grid grid-cols-3 gap-3">
        <div className="p-3 sm:p-4 bg-white/5 rounded-xl border border-white/10 text-center">
          <p className="text-[10px] sm:text-xs text-white/50 uppercase tracking-wider mb-1">Goals</p>
          <p className="text-lg sm:text-2xl font-black text-mint">{goals?.length || 0}</p>
        </div>
        <div className="p-3 sm:p-4 bg-white/5 rounded-xl border border-white/10 text-center">
          <p className="text-[10px] sm:text-xs text-white/50 uppercase tracking-wider mb-1">Tasks</p>
          <p className="text-lg sm:text-2xl font-black text-sky-400">{activeTasks}</p>
        </div>
        <div className="p-3 sm:p-4 bg-white/5 rounded-xl border border-white/10 text-center">
          <p className="text-[10px] sm:text-xs text-white/50 uppercase tracking-wider mb-1">Hours</p>
          <p className="text-lg sm:text-2xl font-black text-amber-400">{analytics?.daily_study_hours?.reduce((a:number, b:any)=>a+b.hours,0) || 0}h</p>
        </div>
      </div>

      {/* Chart + Tasks: stack on mobile, side-by-side on xl */}
      <div className="grid gap-4 xl:grid-cols-[1.5fr_1fr]">
        <Card>
          <h2 className="text-base sm:text-xl font-bold flex items-center gap-2 mb-3 sm:mb-4"><Flame className="text-mint" size={18} /> 30-Day Progress</h2>
          <div className="h-48 sm:h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="hours" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="5%" stopColor="#5ef3b3" stopOpacity={0.65} />
                    <stop offset="95%" stopColor="#5ef3b3" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="rgba(255,255,255,.08)" />
                <XAxis dataKey="day" stroke="rgba(255,255,255,.45)" tick={{ fontSize: 11 }} />
                <YAxis stroke="rgba(255,255,255,.45)" tick={{ fontSize: 11 }} width={30} />
                <Tooltip contentStyle={{ backgroundColor: '#1a1b26', borderColor: '#ffffff20', color: '#fff', fontSize: 12 }} itemStyle={{ color: '#5ef3b3' }} />
                <Area type="monotone" dataKey="hours" stroke="#5ef3b3" fill="url(#hours)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>
        
        <Card className="flex flex-col">
          <h2 className="text-base sm:text-xl font-bold flex items-center gap-2"><ListTodo className="text-sky-400" size={18} /> Today's Focus</h2>
          {!tasks || tasks.length === 0 ? (
            <div className="flex-1 grid place-items-center py-8">
              <p className="text-sm text-white/50 text-center">{getRandomMotivation()}</p>
            </div>
          ) : (
            <div className="flex-1 overflow-y-auto mt-3 space-y-2 custom-scrollbar max-h-[300px] xl:max-h-none">
              {tasks.map((task) => (
                <div key={task.id} className={`flex items-center gap-3 rounded-lg bg-white/5 border border-white/10 p-2.5 sm:p-3 transition ${task.status === 'completed' ? 'opacity-50' : 'hover:bg-white/10'}`}>
                  <button 
                    onClick={() => task.status !== 'completed' && setCompletingTask(task.id)}
                    className={`shrink-0 grid h-5 w-5 place-items-center rounded border ${task.status === 'completed' ? 'border-mint bg-mint text-ink' : 'border-white/30'}`}
                  >
                    {task.status === 'completed' && <Check size={14} />}
                  </button>
                  <div className="flex-1 min-w-0">
                    <p className={`text-sm truncate ${task.status === 'completed' ? 'line-through text-white/50' : ''}`}>{task.name}</p>
                    {task.concept && <p className="text-[10px] text-white/40 mt-0.5">{task.concept}</p>}
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>

      {completingTask && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="bg-ink border border-white/10 p-5 sm:p-6 rounded-xl w-full max-w-md shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg sm:text-xl font-bold">Complete Task</h3>
              <button onClick={() => { setCompletingTask(null); setAttachment(null); setFileName(null); }} className="text-white/50 hover:text-white"><X size={20}/></button>
            </div>
            <p className="text-white/70 mb-5 text-sm">Upload any files or evidence before completing.</p>
            <form onSubmit={completeTaskFlow} className="space-y-4">
              <div className="border-2 border-dashed border-white/20 rounded-lg p-5 text-center hover:border-mint/50 transition-colors cursor-pointer relative bg-white/5">
                <input type="file" onChange={handleFile} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
                <Upload className="mx-auto text-white/40 mb-2" size={20} />
                {fileName ? (
                  <p className="text-sm font-bold text-mint">{fileName}</p>
                ) : (
                  <p className="text-xs text-white/60">Tap to attach file (optional)</p>
                )}
              </div>
              <button className="w-full bg-mint text-ink font-bold py-3 rounded-lg flex items-center justify-center gap-2 hover:bg-mint/90 focus-ring text-sm">
                <Check size={16}/> Mark as Completed
              </button>
            </form>
          </motion.div>
        </div>
      )}
    </div>
  );
}

export function Goals() {
  const { data: goals, refetch: refetchGoals, loading: goalsLoading } = useFetch<any[]>("/api/goals");
  const [selectedGoal, setSelectedGoal] = useState<number | null>(null);
  const { data: roadmap, refetch: refetchRoadmap, loading: roadmapLoading } = useFetch<any>(selectedGoal ? `/api/roadmaps/${selectedGoal}` : "");
  const [editingGoal, setEditingGoal] = useState<any | null>(null);
  const [conceptsInput, setConceptsInput] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  async function createGoal(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const payload = {
      name: fd.get("name"),
      description: fd.get("description"),
      category: fd.get("category"),
      start_date: fd.get("start_date"),
      end_date: fd.get("end_date"),
      priority: fd.get("priority"),
      daily_study_time: Number(fd.get("daily_study_time")),
      weekly_off_day: fd.get("weekly_off_day"),
      difficulty: fd.get("difficulty")
    };
    try {
      await api("/api/goals", { method: "POST", body: JSON.stringify(payload) });
      refetchGoals();
      (e.target as HTMLFormElement).reset();
      toast.success("Goal created! Let's build your roadmap.");
    } catch (err) {
      toast.error("Failed to create goal");
    }
  }

  async function updateStatus(id: number, status: string) {
    try {
      await api(`/api/goals/${id}/status?status_value=${status}`, { method: "PATCH" });
      refetchGoals();
      toast.success(`Goal ${status}`);
    } catch (err) {}
  }

  async function deleteGoal(id: number) {
    try {
      await api(`/api/goals/${id}`, { method: "DELETE" });
      refetchGoals();
      if (selectedGoal === id) setSelectedGoal(null);
      toast.success("Goal deleted");
    } catch (err) {}
  }

  async function saveEdit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const payload = {
      name: fd.get("name"),
      description: fd.get("description"),
      category: fd.get("category"),
      start_date: fd.get("start_date"),
      end_date: fd.get("end_date"),
      priority: fd.get("priority"),
      daily_study_time: Number(fd.get("daily_study_time")),
      weekly_off_day: fd.get("weekly_off_day"),
      difficulty: fd.get("difficulty")
    };
    try {
      await api(`/api/goals/${editingGoal.id}`, { method: "PUT", body: JSON.stringify(payload) });
      setEditingGoal(null);
      refetchGoals();
      toast.success("Goal updated");
    } catch (err) {}
  }

  async function generateRoadmap(e: FormEvent) {
    e.preventDefault();
    if (!selectedGoal || !conceptsInput.trim()) return;
    setIsGenerating(true);
    const concepts = conceptsInput.split('\n').map(c => c.trim()).filter(c => c);
    try {
      await api(`/api/goals/${selectedGoal}/roadmap`, {
        method: "POST",
        body: JSON.stringify({ concepts })
      });
      await refetchRoadmap();
      setConceptsInput("");
      toast.success("Roadmap generated successfully!");
    } catch (err) {
      toast.error("Failed to generate roadmap");
    } finally {
      setIsGenerating(false);
    }
  }

  if (goalsLoading) return <Spinner message="Loading Goals..." />;

  const milestonesData = roadmap?.milestones ? (typeof roadmap.milestones === 'string' ? JSON.parse(roadmap.milestones) : roadmap.milestones) : [];

  return (
    <div className="space-y-6">
      <Header title="Goals & Roadmaps" action={`${goals?.length || 0} active goals`} />
      <div className="grid gap-6 xl:grid-cols-2">
        <Card>
          <h2 className="text-xl font-bold flex items-center gap-2"><Flame className="text-mint" /> Create Goal</h2>
          <form onSubmit={createGoal} className="mt-4 space-y-4">
            <input name="name" required placeholder="Goal Name" className="w-full rounded bg-white/5 border border-white/10 p-2" />
            <textarea name="description" placeholder="Description" className="w-full rounded bg-white/5 border border-white/10 p-2" />
            <div className="grid grid-cols-2 gap-4">
              <input name="start_date" type="date" required className="w-full rounded bg-white/5 border border-white/10 p-2" />
              <input name="end_date" type="date" required className="w-full rounded bg-white/5 border border-white/10 p-2" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <select name="category" className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                <option value="Personal Development">Personal Development</option>
                <option value="Career">Career</option>
                <option value="Health">Health</option>
              </select>
              <select name="priority" className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <input name="daily_study_time" type="number" step="0.5" defaultValue="1.0" required placeholder="Daily Hrs" className="w-full rounded bg-white/5 border border-white/10 p-2" />
              <select name="weekly_off_day" className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                {["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"].map(d => <option key={d} value={d}>{d}</option>)}
              </select>
              <select name="difficulty" className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>
            <button className="w-full bg-mint text-ink font-bold py-2 rounded focus-ring flex justify-center items-center gap-2">
              Create Goal
            </button>
          </form>
        </Card>
        <div className="space-y-6">
          <Card>
            <h2 className="text-xl font-bold mb-4">Your Goals</h2>
            {(!goals || goals.length === 0) && <p className="text-white/50 text-sm">{getRandomMotivation()}</p>}
            {goals?.map(g => (
              <div key={g.id}>
                {editingGoal?.id === g.id ? (
                  <form onSubmit={saveEdit} className="p-3 mb-2 bg-white/5 rounded border border-mint/30 space-y-3">
                    <input name="name" required defaultValue={g.name} className="w-full rounded bg-white/5 border border-white/10 p-2" />
                    <textarea name="description" defaultValue={g.description} className="w-full rounded bg-white/5 border border-white/10 p-2" />
                    <div className="grid grid-cols-2 gap-3">
                      <input name="start_date" type="date" required defaultValue={g.start_date} className="w-full rounded bg-white/5 border border-white/10 p-2" />
                      <input name="end_date" type="date" required defaultValue={g.end_date} className="w-full rounded bg-white/5 border border-white/10 p-2" />
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <select name="category" defaultValue={g.category} className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                        <option value="Personal Development">Personal Development</option>
                        <option value="Career">Career</option>
                        <option value="Health">Health</option>
                      </select>
                      <select name="priority" defaultValue={g.priority} className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                        <option value="high">High</option>
                        <option value="medium">Medium</option>
                        <option value="low">Low</option>
                      </select>
                    </div>
                    <div className="flex justify-end gap-2 mt-2">
                      <button type="button" onClick={() => setEditingGoal(null)} className="text-white/50 text-sm">Cancel</button>
                      <button type="submit" className="text-mint font-bold text-sm">Save</button>
                    </div>
                  </form>
                ) : (
                  <div className={`p-4 mb-3 border rounded-lg transition-colors cursor-pointer ${selectedGoal === g.id ? 'bg-mint/10 border-mint/30' : 'bg-white/5 border-white/10 hover:border-white/20'}`} onClick={() => setSelectedGoal(g.id)}>
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="font-bold flex items-center gap-2">
                          {g.name}
                          {g.status === 'completed' && <Check size={14} className="text-mint" />}
                        </h3>
                        <p className="text-sm text-white/60 line-clamp-1">{g.description}</p>
                      </div>
                      <div className="flex gap-2">
                        <button onClick={(e) => { e.stopPropagation(); setEditingGoal(g); }} className="text-white/50 hover:text-white"><Edit3 size={16} /></button>
                        <button onClick={(e) => { e.stopPropagation(); deleteGoal(g.id); }} className="text-white/50 hover:text-coral"><Trash2 size={16} /></button>
                      </div>
                    </div>
                    <div className="flex justify-between text-xs mt-3">
                      <span className="bg-white/10 px-2 py-1 rounded">{g.category}</span>
                      <div className="flex gap-2 flex-wrap">
                        {g.status === 'active' && <button onClick={(e) => { e.stopPropagation(); updateStatus(g.id, 'paused'); }} className="text-amber">Pause</button>}
                        {g.status === 'paused' && <button onClick={(e) => { e.stopPropagation(); updateStatus(g.id, 'active'); }} className="text-mint">Resume</button>}
                        {g.status !== 'completed' && <button onClick={(e) => { e.stopPropagation(); updateStatus(g.id, 'completed'); }} className="text-mint font-bold">Complete</button>}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </Card>

          {selectedGoal && (
            <Card>
              <h2 className="text-xl font-bold mb-4 flex items-center gap-2"><ArrowRight className="text-mint" /> Roadmap Engine</h2>
              {roadmapLoading ? (
                <Spinner message="Loading Roadmap..." />
              ) : !roadmap || milestonesData.length === 0 ? (
                <div>
                  <p className="text-sm text-white/60 mb-4">No roadmap generated yet. List your main sub-goals or concepts below (one per line). We will allocate sub-timelines for each.</p>
                  <form onSubmit={generateRoadmap}>
                    <textarea 
                      value={conceptsInput} 
                      onChange={(e) => setConceptsInput(e.target.value)}
                      placeholder="e.g. Python\nHTML\nCSS\nReact" 
                      className="w-full rounded bg-white/5 border border-white/10 p-3 h-32 text-sm font-mono mb-3 custom-scrollbar focus-ring" 
                      required 
                    />
                    <button disabled={isGenerating} className="w-full bg-mint text-ink font-bold py-2 rounded focus-ring flex justify-center items-center gap-2">
                      {isGenerating ? <ButtonSpinner /> : "Build Animated Roadmap"}
                    </button>
                  </form>
                </div>
              ) : (
                <div className="space-y-6 relative pl-4 border-l-2 border-white/10">
                  {milestonesData.map((m: any, i: number) => (
                    <motion.div 
                      key={i}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1 }}
                      className="relative"
                    >
                      <div className="absolute -left-[25px] top-1 w-3 h-3 rounded-full bg-mint shadow-[0_0_10px_rgba(94,243,179,0.5)]" />
                      <div className="bg-white/5 border border-white/10 rounded-lg p-4 hover:border-mint/30 transition-colors">
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="font-bold text-mint">{m.concept || m.title || `Phase ${i+1}`}</h4>
                          <span className="text-xs bg-white/10 px-2 py-1 rounded">Week {i+1}</span>
                        </div>
                        <p className="text-sm text-white/70">Connect daily tasks to this concept to see progress.</p>
                      </div>
                    </motion.div>
                  ))}
                  <div className="mt-4 p-4 bg-mint/10 text-mint text-sm rounded-lg">
                    <strong>Tip:</strong> Create daily tasks in the Tasks tab and mention these concepts to progress through your timeline!
                  </div>
                </div>
              )}
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}

export function Tasks() {
  const [tab, setTab] = useState<'daily'|'history'>('daily');
  const [filterDate, setFilterDate] = useState<string>(new Date().toISOString().split("T")[0]);
  const { data: dailyTasks, refetch: refetchDaily, loading: dailyLoading } = useFetch<any[]>(`/api/tasks?day=${filterDate}`);
  const { data: allTasks, refetch: refetchAll, loading: allLoading } = useFetch<any[]>("/api/tasks");
  const { data: goals } = useFetch<any[]>("/api/goals");
  const [completingTask, setCompletingTask] = useState<number | null>(null);
  const [attachment, setAttachment] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const ITEMS_PER_PAGE = 10;

  const tasks = tab === 'daily' ? dailyTasks : allTasks?.filter(t => t.status === 'completed');
  const totalPages = Math.ceil((tasks?.length || 0) / ITEMS_PER_PAGE);
  const paginatedTasks = tab === 'history' ? tasks?.slice((page - 1) * ITEMS_PER_PAGE, page * ITEMS_PER_PAGE) : tasks;

  async function completeTaskFlow(e: FormEvent) {
    e.preventDefault();
    if (!completingTask) return;
    try {
      await api(`/api/tasks/${completingTask}/complete`, { 
        method: "PATCH",
        body: JSON.stringify({ attachment_data: attachment })
      });
      refetchDaily();
      refetchAll();
      setCompletingTask(null);
      setAttachment(null);
      setFileName(null);
      toast.success("Task completed! Momentum +1");
    } catch (e) { toast.error("Failed to complete task"); }
  }

  async function deleteTask(id: number) {
    try {
      await api(`/api/tasks/${id}`, { method: "DELETE" });
      refetchDaily();
      refetchAll();
      toast.success("Task deleted");
    } catch (e) { }
  }

  async function createTask(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const payload = {
      name: fd.get("name"),
      date: fd.get("date"),
      concept: fd.get("concept"),
      estimated_duration: Number(fd.get("estimated_duration"))
    };
    try {
      await api("/api/tasks", { method: "POST", body: JSON.stringify(payload) });
      refetchDaily();
      refetchAll();
      (e.target as HTMLFormElement).reset();
      toast.success("Task added!");
    } catch (e) { toast.error("Failed to add task"); }
  }

  function handleFile(e: any) {
    const file = e.target.files[0];
    if (!file) return;
    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (event) => setAttachment(event.target?.result as string);
    reader.readAsDataURL(file);
  }

  const groupedTasks = (paginatedTasks || []).reduce((acc: any, task: any) => {
    const concept = task.concept || "General";
    if (!acc[concept]) acc[concept] = [];
    acc[concept].push(task);
    return acc;
  }, {});

  return (
    <div className="space-y-6 relative">
      <Header title="Tasks" action="Session overview" />
      <Card>
        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-6">
          <div className="flex gap-4">
            <h2 className={`text-xl font-bold flex items-center gap-2 cursor-pointer ${tab === 'daily' ? 'text-mint' : 'text-white/50'}`} onClick={() => setTab('daily')}>
              <ListTodo size={20} /> Daily Tasks
            </h2>
            <h2 className={`text-xl font-bold flex items-center gap-2 cursor-pointer ${tab === 'history' ? 'text-mint' : 'text-white/50'}`} onClick={() => { setTab('history'); setPage(1); }}>
              <BookOpen size={20} /> History
            </h2>
          </div>
          {tab === 'daily' && (
            <input type="date" value={filterDate} onChange={(e) => setFilterDate(e.target.value)} className="bg-white/5 border border-white/10 rounded p-2 text-sm focus-ring w-full sm:w-auto" />
          )}
        </div>
        
        {tab === 'daily' && (
          <form onSubmit={createTask} className="flex gap-3 mb-6 p-3 rounded-lg bg-white/5 border border-white/10 flex-col sm:flex-row flex-wrap">
            <input name="name" required placeholder="Task name" className="flex-1 min-w-[200px] rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
            <select name="concept" className="w-full sm:w-40 rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring text-white">
              <option value="">Concept (Goal)...</option>
              {goals?.map(g => <option key={g.id} value={g.name}>{g.name}</option>)}
              <option value="General">General</option>
            </select>
            <input name="date" type="date" required defaultValue={filterDate} className="w-full sm:w-auto rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
            <div className="flex gap-2 w-full sm:w-auto">
              <input name="estimated_duration" type="number" step="0.25" defaultValue="1" required placeholder="Hours" className="w-20 rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
              <button className="bg-mint text-ink font-bold px-4 py-2 rounded text-sm flex-1 sm:flex-none flex items-center justify-center gap-1 hover:bg-mint/80 transition-colors"><Plus size={16} /> Add</button>
            </div>
          </form>
        )}

        {(dailyLoading && tab === 'daily') || (allLoading && tab === 'history') ? (
          <Spinner message="Loading Tasks..." />
        ) : (!paginatedTasks || paginatedTasks.length === 0) ? (
          <p className="text-white/50 py-10 text-center">{getRandomMotivation()}</p>
        ) : (
          <div className="space-y-6">
            {Object.entries(groupedTasks).map(([concept, conceptTasks]: [string, any]) => (
              <div key={concept}>
                <h3 className="text-sm font-bold text-white/60 uppercase tracking-widest mb-3 flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-mint"></div> {concept}
                </h3>
                <div className="space-y-3">
                  {conceptTasks.map((t: any) => (
                    <div key={t.id} className={`flex items-start sm:items-center justify-between p-4 rounded-lg bg-white/5 border border-white/10 transition-opacity ${t.status === 'completed' && tab === 'daily' ? 'opacity-40' : ''}`}>
                      <div className="flex items-start sm:items-center gap-4">
                        {tab === 'daily' && (
                          <button onClick={() => t.status !== 'completed' && setCompletingTask(t.id)} className={`mt-1 sm:mt-0 grid h-6 w-6 place-items-center rounded-full border transition-colors ${t.status === 'completed' ? 'border-mint bg-mint text-ink' : 'border-white/20 hover:border-mint'}`}>
                            {t.status === 'completed' && <Check size={14} />}
                          </button>
                        )}
                        <div>
                          <p className={`font-bold ${t.status === 'completed' && tab === 'daily' ? 'line-through text-white/50' : ''}`}>{t.name}</p>
                          <div className="flex flex-wrap items-center gap-3 text-xs text-white/50 mt-1">
                            <span>Est: {t.estimated_duration}h</span>
                            {t.attachment_data && (
                              <a href={t.attachment_data} download={`attachment_${t.id}`} className="flex items-center gap-1 text-sky hover:underline" onClick={e => e.stopPropagation()}>
                                <Upload size={12}/> Download File
                              </a>
                            )}
                            {tab === 'history' && <span>Completed on: {t.date}</span>}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2 shrink-0">
                        <span className="text-xs px-2 py-1 rounded bg-white/10 uppercase tracking-wide hidden sm:block">{t.status}</span>
                        <button onClick={() => deleteTask(t.id)} className="text-xs bg-coral/20 text-coral px-2 py-1 rounded hover:bg-coral/30"><Trash2 size={14} /></button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
        
        {tab === 'history' && totalPages > 1 && (
          <div className="flex justify-center items-center gap-4 mt-8">
            <button disabled={page === 1} onClick={() => setPage(p => p - 1)} className="px-3 py-1 bg-white/5 border border-white/10 rounded disabled:opacity-30">Previous</button>
            <span className="text-sm text-white/50">Page {page} of {totalPages}</span>
            <button disabled={page === totalPages} onClick={() => setPage(p => p + 1)} className="px-3 py-1 bg-white/5 border border-white/10 rounded disabled:opacity-30">Next</button>
          </div>
        )}
      </Card>

      {completingTask && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="bg-ink border border-white/10 p-6 rounded-xl w-full max-w-md shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">Complete Task</h3>
              <button onClick={() => { setCompletingTask(null); setAttachment(null); setFileName(null); }} className="text-white/50 hover:text-white"><X size={20}/></button>
            </div>
            <p className="text-white/70 mb-6 text-sm">Great job! Would you like to upload any files or evidence for this task before completing?</p>
            <form onSubmit={completeTaskFlow} className="space-y-4">
              <div className="border-2 border-dashed border-white/20 rounded-lg p-6 text-center hover:border-mint/50 transition-colors cursor-pointer relative bg-white/5">
                <input type="file" onChange={handleFile} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
                <Upload className="mx-auto text-white/40 mb-2" />
                {fileName ? (
                  <p className="text-sm font-bold text-mint">{fileName}</p>
                ) : (
                  <p className="text-sm text-white/70">Click or drag file to attach (optional)</p>
                )}
              </div>
              <button className="w-full bg-mint text-ink font-bold py-3 rounded-lg flex items-center justify-center gap-2 hover:bg-mint/90 focus-ring">
                <Check size={18}/> Mark as Completed
              </button>
            </form>
          </motion.div>
        </div>
      )}
    </div>
  );
}

export function Analytics() {
  const { data: analytics } = useFetch<any>("/api/analytics");
  
  const rawLogs = analytics?.daily_study_hours || [];
  const chartData = rawLogs.length > 0 ? rawLogs.map((d: any) => ({
    day: new Date(d.date).toLocaleDateString('en-US', { weekday: 'short' }),
    hours: d.hours
  })) : [
    { day: "Mon", hours: 0 }, { day: "Tue", hours: 0 }, { day: "Wed", hours: 0 }, 
    { day: "Thu", hours: 0 }, { day: "Fri", hours: 0 }, { day: "Sat", hours: 0 }, { day: "Sun", hours: 0 }
  ];

  return (
    <div className="space-y-6">
      <Header title="Analytics" action={`Score: ${analytics?.accountability?.score || 0}%`} />
      
      <div className="grid gap-4 md:grid-cols-4">
        <StatCard label="Accountability" value={analytics?.accountability?.label || "-"} />
        <StatCard label="Current Streak" value={`${analytics?.streak?.current || 0} days`} tone="amber" />
        <StatCard label="Task Completion" value={`${analytics?.task_completion || 0}%`} tone="sky" />
        <StatCard label="Grace Days" value={`${analytics?.grace_days_remaining || 0} left`} tone="coral" />
      </div>

      <Card>
        <h2 className="mb-6 text-xl font-bold">Study Hours (Last 30 Days)</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="colorHours" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#5ef3b3" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#5ef3b3" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,.08)" vertical={false} />
              <XAxis dataKey="day" stroke="rgba(255,255,255,.45)" axisLine={false} tickLine={false} />
              <YAxis stroke="rgba(255,255,255,.45)" axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ backgroundColor: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
              <Area type="monotone" dataKey="hours" stroke="#5ef3b3" strokeWidth={3} fillOpacity={1} fill="url(#colorHours)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
}

export function Calendar() {
  const { data: analytics, loading } = useFetch<any>("/api/analytics");
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const { data: dayTasks, loading: tasksLoading } = useFetch<any[]>(selectedDate ? `/api/tasks?day=${selectedDate}` : "");
  const { data: journals, loading: journalsLoading } = useFetch<any[]>(`/api/journal`); 

  const cells = useMemo(() => {
    const logs = analytics?.daily_study_hours || [];
    const logMap = new Map(logs.map((l: any) => [l.date, l.hours]));
    const today = new Date();
    return Array.from({ length: 120 }, (_, i) => {
      const d = new Date(today);
      d.setDate(d.getDate() - (119 - i));
      const dateStr = d.toISOString().split("T")[0];
      const hours: number = (logMap.get(dateStr) as number) || 0;
      let tone = "bg-white/10 hover:bg-white/20";
      if (hours >= 4) tone = "bg-mint";
      else if (hours >= 2) tone = "bg-mint/60 hover:bg-mint/80";
      else if (hours > 0) tone = "bg-mint/30 hover:bg-mint/50";
      return { dateStr, tone, hours };
    });
  }, [analytics]);

  const selectedJournal = useMemo(() => {
    return journals?.find(j => j.date === selectedDate);
  }, [journals, selectedDate]);

  return (
    <div className="space-y-6">
      <Header title="Calendar Heatmap" action="Last 120 Days" />
      <Card>
        {loading ? <Spinner message="Loading Heatmap..." /> : (
          <div className="grid gap-1 sm:gap-2" style={{ gridTemplateColumns: "repeat(20, minmax(0, 1fr))" }}>
            {cells.map((cell, i) => (
              <div 
                key={i} 
                title={`${cell.dateStr}: ${cell.hours} hours`}
                onClick={() => setSelectedDate(cell.dateStr)}
                className={`h-4 sm:h-6 rounded cursor-pointer transition-transform hover:scale-110 ${cell.tone} ${selectedDate === cell.dateStr ? 'ring-2 ring-white ring-offset-2 ring-offset-ink' : ''}`} 
              />
            ))}
          </div>
        )}
      </Card>

      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid gap-6 md:grid-cols-2">
        {!selectedDate ? (
          <div className="md:col-span-2 p-10 text-center text-white/50 bg-white/5 rounded-lg border border-white/10">
            <p className="mb-2 text-lg">Select a day from the heatmap to view details.</p>
            <p className="text-sm italic">"{getRandomMotivation()}"</p>
          </div>
        ) : (
          <>
            <Card>
              <h2 className="text-xl font-bold flex items-center gap-2 mb-4"><ListTodo className="text-mint" /> Tasks on {selectedDate}</h2>
              {tasksLoading ? <Spinner /> : !dayTasks || dayTasks.length === 0 ? (
                <p className="text-white/50">{getRandomMotivation()}</p>
              ) : (
                <div className="space-y-3">
                  {dayTasks.map(t => (
                    <div key={t.id} className="p-3 bg-white/5 border border-white/10 rounded flex justify-between items-center">
                      <div>
                        <p className={`font-bold ${t.status === 'completed' ? 'text-white/50 line-through' : ''}`}>{t.name}</p>
                        {t.concept && <p className="text-xs text-mint mt-1">{t.concept}</p>}
                      </div>
                      <span className="text-xs uppercase bg-white/10 px-2 py-1 rounded tracking-widest">{t.status}</span>
                    </div>
                  ))}
                </div>
              )}
            </Card>
            <Card>
              <h2 className="text-xl font-bold flex items-center gap-2 mb-4"><BookOpen className="text-mint" /> Journal on {selectedDate}</h2>
              {journalsLoading ? <Spinner /> : !selectedJournal ? (
                <p className="text-white/50">No journal entry recorded for this day.</p>
              ) : (
                <div className="space-y-4">
                  <h3 className="font-bold text-lg text-mint">{selectedJournal.title}</h3>
                  <p className="text-sm text-white/80 whitespace-pre-wrap">{selectedJournal.notes}</p>
                  {selectedJournal.learnings && (
                    <div>
                      <strong className="text-xs text-white/50 uppercase tracking-widest block mb-1">Learnings</strong>
                      <p className="text-sm bg-white/5 p-2 rounded border border-white/10">{selectedJournal.learnings}</p>
                    </div>
                  )}
                  {selectedJournal.challenges && (
                    <div>
                      <strong className="text-xs text-white/50 uppercase tracking-widest block mb-1">Challenges</strong>
                      <p className="text-sm bg-coral/10 text-coral p-2 rounded border border-coral/20">{selectedJournal.challenges}</p>
                    </div>
                  )}
                  {selectedJournal.tomorrow_plan && (
                    <div>
                      <strong className="text-xs text-white/50 uppercase tracking-widest block mb-1">Tomorrow's Plan</strong>
                      <p className="text-sm bg-sky-400/10 text-sky-400 p-2 rounded border border-sky-400/20">{selectedJournal.tomorrow_plan}</p>
                    </div>
                  )}
                </div>
              )}
            </Card>
          </>
        )}
      </motion.div>
    </div>
  );
}

export function Journal() {
  const { data: entries, refetch, loading } = useFetch<any[]>("/api/journal");
  const [page, setPage] = useState(1);
  const ITEMS_PER_PAGE = 5;

  async function createJournal(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const payload = {
      entry_date: new Date().toISOString().split("T")[0],
      title: fd.get("title"),
      notes: fd.get("notes"),
      learnings: fd.get("learnings") || null,
      challenges: fd.get("challenges") || null,
      tomorrow_plan: fd.get("tomorrow_plan") || null,
    };
    try {
      await api("/api/journal", { method: "POST", body: JSON.stringify(payload) });
      refetch();
      (e.target as HTMLFormElement).reset();
      toast.success("Journal saved! Keep building momentum.");
    } catch (err) {
      toast.error("Failed to save journal");
    }
  }

  const totalPages = Math.ceil((entries?.length || 0) / ITEMS_PER_PAGE);
  const paginatedEntries = entries?.slice((page - 1) * ITEMS_PER_PAGE, page * ITEMS_PER_PAGE);

  return (
    <div className="space-y-6">
      <Header title="Daily Journal" action={`${entries?.length || 0} total entries`} />
      <div className="grid gap-6 xl:grid-cols-2">
        <Card>
          <h2 className="text-xl font-bold flex items-center gap-2 mb-4"><BookOpen className="text-mint" /> New Entry</h2>
          <form onSubmit={createJournal} className="space-y-4">
            <input name="title" required placeholder="Entry Title" className="w-full rounded bg-white/5 border border-white/10 p-2 focus-ring" />
            <textarea name="notes" required placeholder="General notes about the day" className="w-full rounded bg-white/5 border border-white/10 p-2 min-h-[100px] focus-ring" />
            <textarea name="learnings" placeholder="What did you learn today?" className="w-full rounded bg-white/5 border border-white/10 p-2 focus-ring" />
            <textarea name="challenges" placeholder="Any challenges faced?" className="w-full rounded bg-white/5 border border-white/10 p-2 focus-ring" />
            <textarea name="tomorrow_plan" placeholder="Plan for tomorrow" className="w-full rounded bg-white/5 border border-white/10 p-2 focus-ring" />
            <button className="w-full bg-mint hover:bg-mint/90 text-ink font-bold py-2 rounded focus-ring transition-colors">Save Entry</button>
          </form>
        </Card>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold">Past Entries</h2>
          </div>
          {loading ? <Spinner message="Loading Journals..." /> : (!paginatedEntries || paginatedEntries.length === 0) ? (
            <p className="text-white/50">{getRandomMotivation()}</p>
          ) : (
            <>
              {paginatedEntries.map((entry) => (
                <Card key={entry.id}>
                  <p className="text-xs text-mint uppercase tracking-wide">{entry.date}</p>
                  <h3 className="text-lg font-bold mt-1">{entry.title}</h3>
                  <p className="mt-2 text-sm text-white/70 whitespace-pre-wrap">{entry.notes}</p>
                  {entry.tomorrow_plan && (
                    <div className="mt-3 bg-white/5 border border-white/10 rounded p-2">
                      <span className="text-xs text-white/50 uppercase tracking-widest block mb-1">Tomorrow's Plan</span>
                      <p className="text-sm text-mint">{entry.tomorrow_plan}</p>
                    </div>
                  )}
                </Card>
              ))}
              {totalPages > 1 && (
                <div className="flex justify-center items-center gap-4 mt-6">
                  <button disabled={page === 1} onClick={() => setPage(p => p - 1)} className="px-3 py-1 bg-white/5 border border-white/10 rounded disabled:opacity-30">Previous</button>
                  <span className="text-sm text-white/50">Page {page} of {totalPages}</span>
                  <button disabled={page === totalPages} onClick={() => setPage(p => p + 1)} className="px-3 py-1 bg-white/5 border border-white/10 rounded disabled:opacity-30">Next</button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export function Pomodoro() {
  const { 
    timeLeft, isRunning, mode, isBreak, workMinutes, breakMinutes, 
    startTimer, pauseTimer, resetTimer, setMode, setCustom,
    showLogForm, setShowLogForm
  } = usePomodoro();

  const [customWork, setCustomWork] = useState(25);
  const [customBreak, setCustomBreak] = useState(5);
  const { data: analytics, refetch: refetchAnalytics } = useFetch<any>("/api/analytics");

  const mins = Math.floor(timeLeft / 60).toString().padStart(2, '0');
  const secs = (timeLeft % 60).toString().padStart(2, '0');

  async function logSession(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const payload = {
      log_date: new Date().toISOString().split("T")[0],
      study_hours: Number(fd.get("study_hours")),
      work_hours: 0,
      practice_hours: 0,
      tasks_completed: 0,
      notes: fd.get("notes") || ""
    };
    try {
      await api("/api/study-logs", { method: "POST", body: JSON.stringify(payload) });
      setShowLogForm(false);
      resetTimer();
      refetchAnalytics();
      toast.success("Study session logged!");
    } catch (err) { toast.error("Failed to log session"); }
  }

  function handleCustomChange(w: number, b: number) {
    setCustomWork(w);
    setCustomBreak(b);
    if (mode === 'custom') setCustom(w, b);
  }

  const recentLogs = analytics?.daily_study_hours?.slice(-5).reverse() || [];

  return (
    <div className="space-y-6">
      <Header title="Pomodoro" action={isBreak ? "Break Time" : "Focus Session"} />
      <div className="grid gap-6 xl:grid-cols-2">
        <div className="space-y-6">
          <Card className="grid place-items-center py-14 text-center">
            <div className="flex gap-2 mb-6">
              {(['25/5', '50/10', 'custom'] as const).map((m) => (
                <button key={m} onClick={() => { if (m === 'custom') setCustom(customWork, customBreak); else setMode(m); }} className={`px-4 py-2 rounded-lg text-sm font-bold transition-colors ${mode === m ? 'bg-mint text-ink' : 'border border-white/14 text-white/70 hover:text-white'}`}>{m === 'custom' ? 'Custom' : m}</button>
              ))}
            </div>
            {mode === 'custom' && (
              <div className="flex gap-3 mb-6">
                <div>
                  <label className="block text-xs text-white/50 mb-1">Work (min)</label>
                  <input type="number" min={1} value={customWork} onChange={(e) => handleCustomChange(Number(e.target.value), customBreak)} className="w-20 rounded bg-white/5 border border-white/10 p-2 text-center focus-ring" />
                </div>
                <div>
                  <label className="block text-xs text-white/50 mb-1">Break (min)</label>
                  <input type="number" min={1} value={customBreak} onChange={(e) => handleCustomChange(customWork, Number(e.target.value))} className="w-20 rounded bg-white/5 border border-white/10 p-2 text-center focus-ring" />
                </div>
              </div>
            )}
            {isBreak && <p className="text-sm text-amber mb-2 animate-pulse">☕ Break</p>}
            <p className="text-7xl font-black text-mint tabular-nums">{mins}:{secs}</p>
            <div className="mt-8 flex gap-3">
              <button onClick={() => {
                if (isRunning) pauseTimer();
                else {
                  startTimer();
                  if ('speechSynthesis' in window) {
                    window.speechSynthesis.speak(new SpeechSynthesisUtterance("Timer started."));
                  }
                }
              }} className="focus-ring rounded-lg bg-mint hover:bg-mint/90 px-5 py-3 font-bold text-ink w-32 transition-colors">
                {isRunning ? "Pause" : "Start"}
              </button>
              <button onClick={resetTimer} className="focus-ring rounded-lg border border-white/14 hover:border-white/30 px-5 py-3 transition-colors"><RotateCcw /></button>
            </div>
            {!isRunning && timeLeft < workMinutes * 60 && !showLogForm && !isBreak && (
              <button onClick={() => setShowLogForm(true)} className="mt-4 text-sm text-mint hover:underline">Log Session Early</button>
            )}
          </Card>
          {showLogForm && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
              <Card>
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2"><Flame className="text-mint" /> Log Study Session</h2>
                <form onSubmit={logSession} className="space-y-4">
                  <div>
                    <label className="block text-sm text-white/60 mb-1">Hours Logged</label>
                    <input name="study_hours" type="number" step="0.25" defaultValue={(workMinutes / 60).toFixed(2)} className="w-full rounded bg-white/5 border border-white/10 p-2 focus-ring" />
                  </div>
                  <div>
                    <label className="block text-sm text-white/60 mb-1">Notes</label>
                    <textarea name="notes" className="w-full rounded bg-white/5 border border-white/10 p-2 focus-ring h-24" placeholder="What did you focus on?" />
                  </div>
                  <button className="w-full bg-mint hover:bg-mint/90 text-ink font-bold py-2 rounded transition-colors focus-ring">Save Session</button>
                </form>
              </Card>
            </motion.div>
          )}
        </div>
        
        <Card>
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2"><BookOpen className="text-mint" /> Recent Study Logs</h2>
          {recentLogs.length === 0 ? (
            <div className="py-10 text-center">
              <p className="text-white/50 text-sm mb-2">No recent study logs.</p>
              <p className="text-mint font-bold text-sm italic">"{getRandomMotivation()}"</p>
            </div>
          ) : (
            <div className="space-y-3">
              {recentLogs.map((log: any, i: number) => (
                <div key={i} className="flex justify-between items-center p-3 bg-white/5 border border-white/10 rounded-lg">
                  <span className="text-sm font-bold text-white/70">{new Date(log.date).toLocaleDateString()}</span>
                  <span className="text-sm bg-mint/10 text-mint px-3 py-1 rounded-full">{log.hours} hrs</span>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

export function ResetPassword() {
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");

  async function submit(e: FormEvent) {
    e.preventDefault();
    try {
      const res = await api<{message: string}>("/api/auth/reset-password", {
        method: "POST",
        body: JSON.stringify({ token, new_password: password })
      });
      setMsg(res.message);
    } catch (e: any) { setMsg(e.message); }
  }

  return (
    <div className="min-h-screen bg-ink text-white flex flex-col items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <h2 className="text-2xl font-black mb-6 text-mint">Reset Password</h2>
        <form onSubmit={submit} className="space-y-4">
          <input type="password" required value={password} onChange={e=>setPassword(e.target.value)} placeholder="New Password" className="w-full bg-white/5 border border-white/10 rounded p-3 focus-ring" />
          <button className="w-full bg-mint text-ink font-bold py-3 rounded">Reset Password</button>
        </form>
        {msg && <p className="mt-4 text-center text-sm text-mint">{msg}</p>}
        <div className="mt-6 text-center"><Link to="/login" className="text-white/50 hover:text-white">Back to login</Link></div>
      </Card>
    </div>
  );
}

export function VerifyEmail() {
  const [msg, setMsg] = useState("Verifying...");
  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");

  useEffect(() => {
    api(`/api/auth/verify-email?token=${token}`, { method: "POST" })
      .then(res => setMsg("Email verified successfully!"))
      .catch(e => setMsg("Verification failed."));
  }, [token]);

  return (
    <div className="min-h-screen bg-ink text-white flex flex-col items-center justify-center p-4">
      <Card className="w-full max-w-md text-center py-10">
        <h2 className="text-2xl font-black mb-4 text-mint">{msg}</h2>
        <Link to="/login" className="text-white/50 hover:text-white underline">Go to Login</Link>
      </Card>
    </div>
  );
}

export function Guide() {
  return (
    <div className="space-y-6 max-w-3xl">
      <Header title="Guide" action="How to build momentum" />
      <Card className="prose prose-invert max-w-none">
        <h2 className="text-mint font-black">Welcome to Momentum.</h2>
        <p>This is a high-performance system for staying consistent. Unlike regular to-do apps, Momentum is strictly about accountability.</p>
        
        <h3 className="text-sky-400 font-bold mt-6">1. Goals & Roadmaps</h3>
        <p>Define your main objectives. Generate AI roadmaps to break down complex goals into a 6-week syllabus. Use the milestones as <strong>Concepts</strong> when adding Daily Tasks.</p>
        
        <h3 className="text-amber font-bold mt-6">2. Daily Tasks</h3>
        <p>Plan your focus for the day. Link tasks to your roadmap concepts. Complete them to build your Accountability Score.</p>
        
        <h3 className="text-coral font-bold mt-6">3. Pomodoro & Study Logs</h3>
        <p>Execution matters. Use the Pomodoro timer to focus. After a session, save a Study Log. Study logs are what maintain your <strong>Streak</strong>.</p>

        <h3 className="text-mint font-bold mt-6">4. Heatmap & Journal</h3>
        <p>Reflect on your progress. The Calendar Heatmap visualizes your intensity. Use the Journal to document learnings, vent challenges, and plan tomorrow.</p>
      </Card>
    </div>
  );
}

export function Header({ title, action }: { title: string; action?: ReactNode }) {
  return (
    <header className="mb-4 sm:mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-2 sm:gap-4">
      <h1 className="text-2xl sm:text-4xl font-black tracking-tight">{title}</h1>
      {action && <div className="text-xs sm:text-sm font-bold uppercase tracking-widest text-white/50 bg-white/5 px-3 py-1.5 sm:px-4 sm:py-2 rounded-full border border-white/10 truncate max-w-full">{action}</div>}
    </header>
  );
}

export function Achievements() {
  const { data: achievements } = useFetch<any[]>("/api/achievements");
  return (
    <div className="space-y-6">
      <Header title="Achievements" action="Gamification" />
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {badges.map(b => {
          const unlocked = achievements?.find(a => a.title === b && a.progress >= 100);
          return (
            <Card key={b} className={`transition-all ${unlocked ? 'border-mint/50 bg-mint/5' : 'opacity-50 grayscale'}`}>
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded-full ${unlocked ? 'bg-mint/20 text-mint' : 'bg-white/10 text-white/50'}`}><Trophy size={24} /></div>
                <div><h3 className="font-bold">{b}</h3><p className="text-xs text-white/50 mt-1">{unlocked ? `Unlocked ${new Date(unlocked.unlocked_at).toLocaleDateString()}` : 'Locked'}</p></div>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

export function Notifications() {
  const { data: notifications, refetch, loading } = useFetch<any[]>("/api/notifications");
  async function markRead(id: number) {
    try {
      await api(`/api/notifications/${id}/read`, { method: "PATCH" });
      refetch();
    } catch (e) {}
  }
  return (
    <div className="space-y-6">
      <Header title="Notifications" action={`${notifications?.filter(n => !n.is_read).length || 0} Unread`} />
      <Card>
        {loading ? <Spinner message="Loading Notifications..." /> : !notifications || notifications.length === 0 ? (
          <div className="py-10 text-center">
            <Bell className="mx-auto text-white/20 mb-4" size={32} />
            <p className="text-white/50 mb-2">You're all caught up!</p>
            <p className="text-mint text-sm font-bold italic">"{getRandomMotivation()}"</p>
          </div>
        ) : (
          <div className="space-y-3">
            {notifications.map(n => (
              <div key={n.id} className={`p-4 rounded-lg border transition-all ${n.is_read ? 'bg-white/5 border-white/10 opacity-60' : 'bg-mint/10 border-mint/30 flex justify-between items-start'}`}>
                <div>
                  <h4 className={`font-bold ${!n.is_read ? 'text-mint' : ''}`}>{n.title}</h4>
                  <p className="text-sm text-white/70 mt-1">{n.message}</p>
                </div>
                {!n.is_read && <button onClick={() => markRead(n.id)} className="text-xs text-mint font-bold hover:underline">Mark Read</button>}
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}

export function Settings() {
  const { data: settings, refetch: refetchSettings } = useFetch<any>("/api/settings");
  const { data: profile, refetch: refetchProfile } = useFetch<any>("/api/me");
  
  async function toggleSetting(field: string, val: boolean) {
    try {
      await api("/api/settings", { method: "PUT", body: JSON.stringify({ [field]: val }) });
      refetchSettings();
    } catch (e) {}
  }

    async function updateProfile(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    try {
      await api("/api/me", { 
        method: "PUT", 
        body: JSON.stringify({ 
          full_name: fd.get("full_name"), 
          daily_target_hours: Number(fd.get("daily_target_hours")) 
        }) 
      });
      refetchProfile();
      toast.success("Profile updated successfully!");
    } catch (e) { toast.error("Failed to update profile"); }
  }

  function logout() {
    localStorage.removeItem('momentum_token');
    window.location.href = '/login';
  }

  return (
    <div className="space-y-6">
      <Header title="Settings" action="Preferences" />
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2"><SettingsIcon className="text-mint" /> Profile</h2>
          {profile ? (
            <form onSubmit={updateProfile} className="space-y-4">
              <div>
                <label className="block text-xs text-white/50 uppercase tracking-widest mb-1">Full Name</label>
                <input name="full_name" defaultValue={profile.full_name} className="w-full bg-white/5 border border-white/10 rounded p-2 focus-ring" />
              </div>
              <div>
                <label className="block text-xs text-white/50 uppercase tracking-widest mb-1">Email</label>
                <input type="email" name="email" defaultValue={profile.email} disabled className="w-full bg-white/5 border border-white/10 rounded p-2 opacity-50 cursor-not-allowed" />
              </div>
              <div>
                <label className="block text-xs text-white/50 uppercase tracking-widest mb-1">Daily Target (Hours)</label>
                <input name="daily_target_hours" type="number" step="0.5" defaultValue={profile.daily_target_hours} className="w-full bg-white/5 border border-white/10 rounded p-2 focus-ring" />
              </div>
              <div className="pt-2">
                <button type="submit" className="bg-mint text-ink font-bold px-4 py-2 rounded focus-ring">Save Profile</button>
              </div>
            </form>
          ) : (
            <Spinner />
          )}
        </Card>

        <div className="space-y-6">
          <Card>
            <h2 className="text-xl font-bold mb-6 flex items-center gap-2"><Bell className="text-mint" /> Preferences</h2>
            <div className="space-y-4">
              {['email_reminders', 'push_notifications', 'weekly_summary'].map((k) => (
                <div key={k} className="flex items-center justify-between p-4 bg-white/5 rounded-lg border border-white/10">
                  <span className="capitalize text-sm font-bold text-white/80">{k.replace('_', ' ')}</span>
                  <button 
                    onClick={() => settings && toggleSetting(k, !settings[k])} 
                    className={`w-12 h-6 rounded-full transition-colors focus-ring ${settings?.[k] ? 'bg-mint' : 'bg-white/20'} relative`}
                  >
                    <div className={`absolute top-1 bg-white w-4 h-4 rounded-full transition-transform ${settings?.[k] ? 'left-7 bg-ink' : 'left-1'}`} />
                  </button>
                </div>
              ))}
            </div>
          </Card>

          <Card className="border-coral/30 bg-coral/5">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-coral"><Shield size={20} /> Account Actions</h2>
            <button onClick={logout} className="flex items-center gap-2 bg-coral text-ink font-bold px-4 py-2 rounded hover:bg-coral/80 transition-colors focus-ring">
              <LogOut size={16} /> Logout
            </button>
          </Card>
        </div>
      </div>
    </div>
  );
}
