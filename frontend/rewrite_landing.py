import re

pages_path = 'src/pages/Pages.tsx'

with open(pages_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
import_lucide = r'import \{ (.*?) \} from "lucide-react";'
match = re.search(import_lucide, content)
if match:
    existing_icons = match.group(1).split(', ')
    new_icons = ['ChevronRight', 'Activity', 'Target', 'Zap', 'Clock', 'ShieldCheck']
    combined = sorted(list(set(existing_icons + new_icons)))
    content = content.replace(match.group(0), f'import {{ {", ".join(combined)} }} from "lucide-react";')

# 2. Update Landing Component
landing_replacement = '''export function Landing() {
  const navigate = useNavigate();

  return (
    <main className="min-h-screen bg-ink text-white selection:bg-mint/30 selection:text-white">
      {/* Dynamic Background */}
      <div className="fixed inset-0 z-0 bg-[radial-gradient(circle_at_20%_20%,rgba(94,243,179,.15),transparent_35%),radial-gradient(circle_at_80%_30%,rgba(125,211,252,.12),transparent_35%),linear-gradient(135deg,#070a12,#111827_55%,#07120f)]" />

      {/* Floating Header */}
      <header className="fixed top-0 left-0 right-0 z-50 px-6 py-4">
        <motion.div 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className="mx-auto max-w-7xl flex items-center justify-between glass px-6 py-3 rounded-2xl border border-white/10 shadow-2xl backdrop-blur-xl"
        >
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-xl bg-mint text-ink font-black text-lg shadow-[0_0_15px_rgba(94,243,179,0.5)]">M</div>
            <span className="text-xl font-bold tracking-tight">Momentum</span>
          </div>
          <div className="flex items-center gap-4">
            <Link to="/login" className="text-sm font-bold text-white/70 hover:text-white transition-colors">Login</Link>
            <Link to="/login" onClick={() => localStorage.setItem('auth_mode', 'register')} className="text-sm font-bold bg-white text-ink px-5 py-2 rounded-lg hover:bg-white/90 transition-all hover:scale-105 active:scale-95 shadow-[0_0_20px_rgba(255,255,255,0.2)]">Register</Link>
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
}'''

landing_pattern = r'export function Landing\(\) \{.*?(?=export function Login\(\) \{)'
content = re.sub(landing_pattern, landing_replacement + '\n\n', content, flags=re.DOTALL)

# 3. Update Login mode hook logic
login_replacement = '''export function Login() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<"login" | "register" | "forgot">("register");

  useEffect(() => {
    const savedMode = localStorage.getItem('auth_mode');
    if (savedMode === 'register' || savedMode === 'login') {
      setMode(savedMode as any);
      localStorage.removeItem('auth_mode');
    }
  }, []);'''
login_pattern = r'export function Login\(\) \{\n\s*const navigate = useNavigate\(\);\n\s*const \[mode, setMode\] = useState<"login" \| "register" \| "forgot">\("register"\);'
content = re.sub(login_pattern, login_replacement, content)

# 4. Update Dashboard Streak stat card to include 🔥 emoji
streak_pattern = r'<StatCard label="Current streak" value={`\$\{analytics\?\.streak\?\.current \|\| 0\} days`} />'
streak_replacement = r'<StatCard label="Current streak 🔥" value={`${analytics?.streak?.current || 0} days`} />'
content = content.replace('<StatCard label="Current streak" value={`${analytics?.streak?.current || 0} days`} />', '<StatCard label="Current streak 🔥" value={`${analytics?.streak?.current || 0} days`} />')

with open(pages_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Landing page rewritten and streak updated.")
