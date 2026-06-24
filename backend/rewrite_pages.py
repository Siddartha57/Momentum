import re

with open('../frontend/src/pages/Pages.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

import_replacement = '''import { ArrowRight, Bell, Check, Edit3, Flame, LogOut, Play, Plus, RotateCcw, Shield, Sparkles, Trash2, Trophy, BookOpen, ListTodo, Settings as SettingsIcon, HelpCircle, Upload, X } from "lucide-react";
import { toast } from "react-hot-toast";
'''
content = content.replace('import { ArrowRight, Bell, Check, Edit3, Flame, LogOut, Play, Plus, RotateCcw, Shield, Sparkles, Trash2, Trophy, BookOpen, ListTodo, Settings as SettingsIcon, HelpCircle } from "lucide-react";', import_replacement)

goals_replacement = '''export function Goals() {
  const { data: goals, refetch: refetchGoals } = useFetch<any[]>("/api/goals");
  const [selectedGoal, setSelectedGoal] = useState<number | null>(null);
  const { data: roadmap, refetch: refetchRoadmap } = useFetch<any>(selectedGoal ? `/api/roadmaps/${selectedGoal}` : "");
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
    const concepts = conceptsInput.split('\\n').map(c => c.trim()).filter(c => c);
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
            <div className="grid grid-cols-3 gap-4">
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
            <button className="w-full bg-mint text-ink font-bold py-2 rounded">Create Goal</button>
          </form>
        </Card>
        <div className="space-y-6">
          <Card>
            <h2 className="text-xl font-bold mb-4">Your Goals</h2>
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
                    <div className="grid grid-cols-3 gap-3">
                      <input name="daily_study_time" type="number" step="0.5" defaultValue={g.daily_study_time} required className="w-full rounded bg-white/5 border border-white/10 p-2" />
                      <select name="weekly_off_day" defaultValue={g.weekly_off_day} className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                        {["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"].map(d => <option key={d} value={d}>{d}</option>)}
                      </select>
                      <select name="difficulty" defaultValue={g.difficulty} className="w-full rounded bg-white/5 border border-white/10 p-2 text-white">
                        <option value="easy">Easy</option>
                        <option value="medium">Medium</option>
                        <option value="hard">Hard</option>
                      </select>
                    </div>
                    <div className="flex gap-2">
                      <button className="flex-1 bg-mint text-ink font-bold py-2 rounded">Save</button>
                      <button type="button" onClick={() => setEditingGoal(null)} className="flex-1 border border-white/10 py-2 rounded">Cancel</button>
                    </div>
                  </form>
                ) : (
                  <div className={`p-3 mb-2 rounded border transition-colors cursor-pointer flex justify-between items-center ${selectedGoal === g.id ? "bg-white/10 border-mint" : "bg-white/5 border-white/10"}`} onClick={() => setSelectedGoal(g.id)}>
                    <div>
                      <h3 className="font-bold">{g.name}</h3>
                      <p className="text-xs text-white/50">{g.start_date} to {g.end_date}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`text-xs px-2 py-1 rounded ${g.status === 'active' ? 'bg-mint/20 text-mint' : 'bg-white/10'}`}>{g.status}</span>
                      {g.status === 'active' && <button onClick={(e) => { e.stopPropagation(); updateStatus(g.id, 'paused'); }} className="text-xs bg-amber/20 text-amber px-2 py-1 rounded">Pause</button>}
                      {g.status === 'paused' && <button onClick={(e) => { e.stopPropagation(); updateStatus(g.id, 'active'); }} className="text-xs bg-sky/20 text-sky px-2 py-1 rounded">Resume</button>}
                      <button onClick={(e) => { e.stopPropagation(); updateStatus(g.id, 'completed'); }} className="text-xs bg-mint text-ink px-2 py-1 rounded"><Check size={14}/></button>
                      <button onClick={(e) => { e.stopPropagation(); setEditingGoal(g); }} className="text-xs bg-sky/20 text-sky px-2 py-1 rounded"><Edit3 size={14}/></button>
                      <button onClick={(e) => { e.stopPropagation(); deleteGoal(g.id); }} className="text-xs bg-coral/20 text-coral px-2 py-1 rounded"><Trash2 size={14}/></button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </Card>
          {selectedGoal && !roadmap && (
            <Card>
              <h2 className="text-xl font-bold mb-2 text-mint">Build Roadmap</h2>
              <p className="text-sm text-white/70 mb-4">Break your goal down into core concepts or milestones. Enter one per line.</p>
              <form onSubmit={generateRoadmap}>
                <textarea 
                  value={conceptsInput} 
                  onChange={e => setConceptsInput(e.target.value)} 
                  placeholder="E.g.\nDatabase Design\nAPI Routing\nAuthentication"
                  className="w-full h-32 rounded bg-white/5 border border-white/10 p-3 text-white mb-4 focus-ring"
                  required
                />
                <button disabled={isGenerating} className="w-full bg-mint text-ink font-bold py-2 rounded flex items-center justify-center gap-2">
                  {isGenerating ? "Generating..." : <><Sparkles size={16}/> Generate Animated Roadmap</>}
                </button>
              </form>
            </Card>
          )}

          {selectedGoal && roadmap && (
            <Card>
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-xl font-bold">Roadmap Journey</h2>
                  <p className="text-sm text-white/70">{roadmap.overview}</p>
                </div>
                <div className="bg-mint/20 text-mint text-xs px-3 py-1 rounded-full font-bold uppercase tracking-widest">Active</div>
              </div>
              <div className="relative border-l-2 border-mint/20 ml-3 space-y-8 pb-4 pt-2">
                {JSON.parse(roadmap.milestones_json).map((m: any, i: number) => (
                  <motion.div 
                    initial={{ opacity: 0, x: -20 }} 
                    animate={{ opacity: 1, x: 0 }} 
                    transition={{ delay: i * 0.1 }}
                    key={i} 
                    className="relative pl-8 group"
                  >
                    <div className="absolute -left-[9px] top-1.5 h-4 w-4 rounded-full bg-ink border-2 border-mint shadow-[0_0_12px_rgba(94,243,179,0.5)] group-hover:bg-mint transition-colors" />
                    <div className="bg-white/5 p-4 rounded-lg border border-white/10 group-hover:border-mint/50 transition-all hover:bg-white/10">
                      <span className="text-xs font-bold text-mint uppercase tracking-wider mb-1 block">Step {m.week}</span>
                      <h4 className="font-bold text-lg text-white/90">{m.focus}</h4>
                    </div>
                  </motion.div>
                ))}
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}'''

tasks_replacement = '''export function Tasks() {
  const [filterDate, setFilterDate] = useState<string>(new Date().toISOString().split("T")[0]);
  const { data: tasks, refetch } = useFetch<any[]>(`/api/tasks?day=${filterDate}`);
  const [completingTask, setCompletingTask] = useState<number | null>(null);
  const [attachment, setAttachment] = useState<string | null>(null);

  async function completeTaskFlow(e: FormEvent) {
    e.preventDefault();
    if (!completingTask) return;
    try {
      await api(`/api/tasks/${completingTask}/complete`, { 
        method: "PATCH",
        body: JSON.stringify({ attachment_data: attachment })
      });
      refetch();
      setCompletingTask(null);
      setAttachment(null);
      toast.success("Task completed! Momentum +1");
    } catch (e) { toast.error("Failed to complete task"); }
  }

  async function deleteTask(id: number) {
    try {
      await api(`/api/tasks/${id}`, { method: "DELETE" });
      refetch();
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
      refetch();
      (e.target as HTMLFormElement).reset();
      toast.success("Task added!");
    } catch (e) { toast.error("Failed to add task"); }
  }

  function handleFile(e: any) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => setAttachment(event.target?.result as string);
    reader.readAsDataURL(file);
  }

  // Group tasks by concept
  const groupedTasks = (tasks || []).reduce((acc: any, task: any) => {
    const concept = task.concept || "General";
    if (!acc[concept]) acc[concept] = [];
    acc[concept].push(task);
    return acc;
  }, {});

  return (
    <div className="space-y-6 relative">
      <Header title="Tasks" action="Session overview" />
      <Card>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold flex items-center gap-2"><ListTodo className="text-mint" /> Daily Tasks</h2>
          <input type="date" value={filterDate} onChange={(e) => setFilterDate(e.target.value)} className="bg-white/5 border border-white/10 rounded p-2 text-sm focus-ring" />
        </div>
        <form onSubmit={createTask} className="flex gap-3 mb-6 p-3 rounded-lg bg-white/5 border border-white/10 flex-wrap">
          <input name="name" required placeholder="Task name" className="flex-1 min-w-[200px] rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
          <input name="concept" placeholder="Concept (optional)" className="w-40 rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
          <input name="date" type="date" required defaultValue={filterDate} className="rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
          <input name="estimated_duration" type="number" step="0.25" defaultValue="1" required placeholder="Hours" className="w-24 rounded bg-white/5 border border-white/10 px-3 py-2 text-sm focus-ring" />
          <button className="bg-mint text-ink font-bold px-4 py-2 rounded text-sm flex items-center gap-1 hover:bg-mint/80 transition-colors"><Plus size={16} /> Add</button>
        </form>

        {(!tasks || tasks.length === 0) ? (
          <p className="text-white/50 py-4 text-center">No tasks for this date.</p>
        ) : (
          <div className="space-y-6">
            {Object.entries(groupedTasks).map(([concept, conceptTasks]: [string, any]) => (
              <div key={concept}>
                <h3 className="text-sm font-bold text-white/60 uppercase tracking-widest mb-3 flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-mint"></div> {concept}
                </h3>
                <div className="space-y-3">
                  {conceptTasks.map((t: any) => (
                    <div key={t.id} className={`flex items-center justify-between p-4 rounded-lg bg-white/5 border border-white/10 transition-opacity ${t.status === 'completed' ? 'opacity-40' : ''}`}>
                      <div className="flex items-center gap-4">
                        <button onClick={() => t.status !== 'completed' && setCompletingTask(t.id)} className={`grid h-6 w-6 place-items-center rounded-full border transition-colors ${t.status === 'completed' ? 'border-mint bg-mint text-ink' : 'border-white/20 hover:border-mint'}`}>
                          {t.status === 'completed' && <Check size={14} />}
                        </button>
                        <div>
                          <p className={`font-bold ${t.status === 'completed' ? 'line-through text-white/50' : ''}`}>{t.name}</p>
                          <div className="flex items-center gap-3 text-xs text-white/50">
                            <span>Est: {t.estimated_duration}h</span>
                            {t.attachment_data && <span className="flex items-center gap-1 text-sky"><Upload size={12}/> Attached</span>}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs px-2 py-1 rounded bg-white/10 uppercase tracking-wide">{t.status}</span>
                        <button onClick={() => deleteTask(t.id)} className="text-xs bg-coral/20 text-coral px-2 py-1 rounded hover:bg-coral/30"><Trash2 size={14} /></button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      {completingTask && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="bg-ink border border-white/10 p-6 rounded-xl w-full max-w-md shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">Complete Task</h3>
              <button onClick={() => { setCompletingTask(null); setAttachment(null); }} className="text-white/50 hover:text-white"><X size={20}/></button>
            </div>
            <p className="text-white/70 mb-6">Great job! Would you like to upload any files or evidence for this task before completing?</p>
            <form onSubmit={completeTaskFlow} className="space-y-4">
              <div className="border-2 border-dashed border-white/20 rounded-lg p-6 text-center hover:border-mint/50 transition-colors cursor-pointer relative">
                <input type="file" onChange={handleFile} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
                <Upload className="mx-auto text-white/40 mb-2" />
                <p className="text-sm text-white/70">{attachment ? "File selected (Base64 ready)" : "Click or drag file to attach (optional)"}</p>
              </div>
              <button className="w-full bg-mint text-ink font-bold py-3 rounded-lg flex items-center justify-center gap-2 hover:bg-mint/90">
                <Check size={18}/> Mark as Completed
              </button>
            </form>
          </motion.div>
        </div>
      )}
    </div>
  );
}'''

goals_match = re.search(r'export function Goals\(\) \{.*?(?=export function Tasks\(\) \{)', content, re.DOTALL)
if goals_match:
    content = content.replace(goals_match.group(0), goals_replacement + '\n\n')

tasks_match = re.search(r'export function Tasks\(\) \{.*?(?=export function Analytics\(\) \{)', content, re.DOTALL)
if tasks_match:
    content = content.replace(tasks_match.group(0), tasks_replacement + '\n\n')

with open('../frontend/src/pages/Pages.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
