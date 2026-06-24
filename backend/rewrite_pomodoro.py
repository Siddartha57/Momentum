import re

with open('../frontend/src/pages/Pages.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

pomodoro_replacement = '''export function Pomodoro() {
  const { 
    timeLeft, isRunning, mode, isBreak, workMinutes, breakMinutes, 
    startTimer, pauseTimer, resetTimer, setMode, setCustom,
    showLogForm, setShowLogForm
  } = usePomodoro();

  const [customWork, setCustomWork] = useState(25);
  const [customBreak, setCustomBreak] = useState(5);

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
      toast.success("Study session logged!");
    } catch (err) { toast.error("Failed to log session"); }
  }

  function handleCustomChange(w: number, b: number) {
    setCustomWork(w);
    setCustomBreak(b);
    if (mode === 'custom') setCustom(w, b);
  }

  return (
    <div className="space-y-6">
      <Header title="Pomodoro" action={isBreak ? "Break Time" : "Focus Session"} />
      <div className="grid gap-6 xl:grid-cols-2">
        <Card className="grid place-items-center py-14 text-center">
          <div className="flex gap-2 mb-6">
            {(['25/5', '50/10', 'custom'] as const).map((m) => (
              <button key={m} onClick={() => { if (m === 'custom') setCustom(customWork, customBreak); else setMode(m); }} className={`px-4 py-2 rounded-lg text-sm font-bold ${mode === m ? 'bg-mint text-ink' : 'border border-white/14 text-white/70'}`}>{m === 'custom' ? 'Custom' : m}</button>
            ))}
          </div>
          {mode === 'custom' && (
            <div className="flex gap-3 mb-6">
              <div>
                <label className="block text-xs text-white/50 mb-1">Work (min)</label>
                <input type="number" min={1} value={customWork} onChange={(e) => handleCustomChange(Number(e.target.value), customBreak)} className="w-20 rounded bg-white/5 border border-white/10 p-2 text-center" />
              </div>
              <div>
                <label className="block text-xs text-white/50 mb-1">Break (min)</label>
                <input type="number" min={1} value={customBreak} onChange={(e) => handleCustomChange(customWork, Number(e.target.value))} className="w-20 rounded bg-white/5 border border-white/10 p-2 text-center" />
              </div>
            </div>
          )}
          {isBreak && <p className="text-sm text-amber mb-2">☕ Break</p>}
          <p className="text-7xl font-black text-mint">{mins}:{secs}</p>
          <div className="mt-8 flex gap-3">
            <button onClick={() => isRunning ? pauseTimer() : startTimer()} className="focus-ring rounded-lg bg-mint px-5 py-3 font-bold text-ink w-32">{isRunning ? "Pause" : "Start"}</button>
            <button onClick={resetTimer} className="focus-ring rounded-lg border border-white/14 px-5 py-3"><RotateCcw /></button>
          </div>
          {!isRunning && timeLeft < workMinutes * 60 && !showLogForm && !isBreak && (
            <button onClick={() => setShowLogForm(true)} className="mt-4 text-sm text-mint hover:underline">Log Session Early</button>
          )}
        </Card>
        {showLogForm && (
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
              <button className="w-full bg-mint text-ink font-bold py-2 rounded">Save Session</button>
            </form>
          </Card>
        )}
      </div>
    </div>
  );
}'''

pomodoro_match = re.search(r'export function Pomodoro\(\) \{.*?(?=export function ResetPassword\(\) \{)', content, re.DOTALL)
if pomodoro_match:
    content = content.replace(pomodoro_match.group(0), pomodoro_replacement + '\n\n')

# need to import usePomodoro in Pages.tsx
if 'import { usePomodoro }' not in content:
    content = content.replace('import { toast } from "react-hot-toast";', 'import { toast } from "react-hot-toast";\nimport { usePomodoro } from "../context/PomodoroContext";')

with open('../frontend/src/pages/Pages.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
